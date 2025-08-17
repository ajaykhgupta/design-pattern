from question import Question
from answer import Answer
from comment import Comment

class User:

    def __init__(self, username, email):
        self.id = id(self)
        self.username = username
        self.email = email
        self.reputation = 0
        self.question = []
        self.answer = []
        self.comments = []


    def ask_question(self, title, content, tags):
        question = Question(author=self, title=title, content=content, tag_names=tags)
        self.question.append(question)
        self.update_reputation(5)
        return question

    def answer_question(self, question: Question, content):
        answer = Answer(author=self, content=content, question=question)
        self.answer.append(answer)
        question.add_answer(answer)
        self.update_reputation(10)
        return answer

    def comment_on(self, commentable, content):
        comment = Comment(self, content)
        self.comments.append(comment)
        commentable.add_comment(comment)
        self.update_reputation(2)  # Gain 2 reputation for commenting
        return comment



    def update_reputation(self, val):
        self.reputation += val
