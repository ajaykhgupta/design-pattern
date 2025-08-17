from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Tuple

class Symbol(Enum):
    EMPTY = " "
    X = "X"
    O = "O"

@dataclass(frozen=True)
class Move:
    row: int
    col: int

class Board:
    def __init__(self, size: int = 3) -> None:
        self.size = size
        self.grid: List[List[Symbol]] = [[Symbol.EMPTY for _ in range(size)] for _ in range(size)]

    def get(self, r: int, c: int) -> Symbol:
        return self.grid[r][c]

    def set(self, r: int, c: int, symbol: Symbol) -> None:
        self.grid[r][c] = symbol

    def is_empty(self, r: int, c: int) -> bool:
        return self.get(r, c) == Symbol.EMPTY

    def is_full(self) -> bool:
        return all(cell != Symbol.EMPTY for row in self.grid for cell in row)

    def reset(self) -> None:
        for r in range(self.size):
            for c in range(self.size):
                self.grid[r][c] = Symbol.EMPTY

    def get_lines(self) -> List[List[Tuple[int, int]]]:
        """Return all winning lines as lists of (r,c) tuples."""
        n = self.size
        lines = []
        # Rows and columns
        for i in range(n):
            lines.append([(i, j) for j in range(n)])
            lines.append([(j, i) for j in range(n)])
        # Diagonals
        lines.append([(i, i) for i in range(n)])
        lines.append([(i, n - 1 - i) for i in range(n)])
        return lines

class MoveValidator:
    def validate(self, board: Board, move: Move) -> Optional[str]:
        n = board.size
        if not (0 <= move.row < n and 0 <= move.col < n):
            return f"Move out of bounds. Enter row/col between 1 and {n}."
        if not board.is_empty(move.row, move.col):
            return "Cell is already occupied. Choose another."
        return None

class Referee:
    def check_winner(self, board: Board) -> Optional[Symbol]:
        # returns winning symbol either X or O
        for line in board.get_lines():
            symbols = [board.get(r, c) for (r, c) in line]
            if symbols[0] != Symbol.EMPTY and all(s == symbols[0] for s in symbols):
                return symbols[0]
        return None

    def is_draw(self, board: Board) -> bool:
        return board.is_full() and self.check_winner(board) is None

class UI:
    def render(self, board: Board) -> None:
        n = board.size
        print("\n  " + "   ".join(str(i + 1) for i in range(n)))
        print("  " + "—" * (4 * n - 1))
        for r in range(n):
            row_symbols = " | ".join(board.get(r, c).value for c in range(n))
            print(f"{r + 1} {row_symbols}")
            if r < n - 1:
                print("  " + "-" * (4 * n - 1))
        print()

    def prompt_move(self, player: "Player") -> Move:
        while True:
            raw = input(f"{player.name} ({player.symbol.value}) enter move as row,col (e.g., 1,3): ").strip()
            try:
                r_str, c_str = raw.split(",")
                r = int(r_str) - 1
                c = int(c_str) - 1
                return Move(r, c)
            except Exception:
                print("Invalid format. Please use row,col with numbers (e.g., 2,2).")

    def show_error(self, message: str) -> None:
        print(f"\n[!] {message}\n")

    def announce_winner(self, player: "Player") -> None:
        print(f"🎉 {player.name} wins as {player.symbol.value}!\n")

    def announce_draw(self) -> None:
        print("It\'s a draw! No more moves left.\n")

@dataclass
class Player:
    name: str
    symbol: Symbol

    def get_move(self, ui: UI) -> Move:
        return ui.prompt_move(self)

class TicTacToeGame:
    def __init__(self, player1: Player, player2: Player, ui: UI | None = None) -> None:
        self.board = Board()
        self.players = [player1, player2]
        self.current = 0  # index into self.players
        self.validator = MoveValidator()
        self.referee = Referee()
        self.ui = ui or UI()

    def switch_turn(self) -> None:
        self.current = 1 - self.current

    def play_turn(self) -> Optional[Player]:
        player = self.players[self.current]
        while True:
            move = player.get_move(self.ui)
            error = self.validator.validate(self.board, move)
            if error:
                self.ui.show_error(error)
                continue
            self.board.set(move.row, move.col, player.symbol)
            break
        import pdb
        pdb.set_trace()
        winner_symbol = self.referee.check_winner(self.board)
        if winner_symbol is not None:
            # Map symbol -> player
            winner = next(p for p in self.players if p.symbol == winner_symbol)
            return winner
        return None

    def run(self) -> None:
        self.board.reset()
        while True:
            self.ui.render(self.board)
            winner = self.play_turn()
            if winner is not None:
                self.ui.render(self.board)
                self.ui.announce_winner(winner)
                return
            if self.referee.is_draw(self.board):
                self.ui.render(self.board)
                self.ui.announce_draw()
                return
            self.switch_turn()

if __name__ == "__main__":
    print("Welcome to Tic‑Tac‑Toe!\n")
    # Ask user to select symbols
    while True:
        choice = input("Player 1, choose your symbol (X/O): ").strip().upper()
        if choice in ("X", "O"):
            p1_symbol = Symbol.X if choice == "X" else Symbol.O
            p2_symbol = Symbol.O if p1_symbol == Symbol.X else Symbol.X
            break
        else:
            print("Invalid choice. Please select X or O.")
    # Setup players (can be extended to prompt names)
    p1 = Player(name="Player 1", symbol=p1_symbol)
    p2 = Player(name="Player 2", symbol=p2_symbol)
    game = TicTacToeGame(p1, p2)
    game.run()