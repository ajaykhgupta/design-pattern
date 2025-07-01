from abc import abstractmethod, ABC

class Payment(ABC):

    @abstractmethod
    def pay(self, amount: float):
        pass
