from datetime import datetime
from vote import Vote
from votable import Votable
from commentable import Commentable

class Answer(Votable, Commentable):
    def __init__(self, content, author, question):
        self.id = id(self)
        self.content = content
        self.author = author
        self.question = question
        self.creation_date = datetime.now()
        self.votes = []
        self.comments = []
        self.is_accepted = False
    
    def vote(self, user, value):
        if value not in [-1, 1]:
            raise ValueError("Vote value must be either 1 or -1")
        self.votes = [v for v in self.votes if v.user != user]
        self.votes.append(Vote(user, value))
        self.author.update_reputation(value * 10)

    def accept(self):
        if self.is_accepted:
            raise ValueError("This answer is already accepted")
        self.is_accepted = True
        self.author.update_reputation(15)

    def get_vote_count(self) -> int:
        return sum(v.value for v in self.votes)

    def add_comment(self, comment):
        self.comments.append(comment)
    
    def get_comments(self):
        return self.comments.copy()
