from user import User
from question import Question
from answer import Answer

class StackOverflow:
    def __init__(self):
        self.users = {}
        self.questions = {}
        self.answers = {}
        self.tags = {}
    
    def create_user(self, username, email):
        user_id = len(self.users) + 1
        user = User(email=email, username=username)
        self.users[user_id] = user
        return user
    
    def ask_question(self, user:User, title, content, tags):
        question = user.ask_question(title, content, tags)
        self.questions[question.id] = question
        for tag in question.tags:
            self.tags.setdefault(tag.name, tag)
        return question

    def answer_question(self, user, question, content):
        answer = user.answer_question(question, content)
        self.answers[answer.id] = answer
        return answer

    def add_comment(self, user:User, commentable, content):
        return user.comment_on(commentable, content)

    def vote_question(self, user:User, question: Question, value):
        question.vote(user, value)

    def vote_answer(self, user:User, answer:Answer, value):
        answer.vote(user, value)

    def accept_answer(self, answer:Answer):
        answer.accept()
    
    def search_questions(self, query):
        return [q for q in self.questions.values() if 
                query.lower() in q.title.lower() or
                query.lower() in q.content.lower() or
                any(query.lower() == tag.name.lower() for tag in q.tags)]

    def get_questions_by_user(self, user: User):
        return user.question

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_question(self, question_id):
        return self.questions.get(question_id)

    def get_answer(self, answer_id):
        return self.answers.get(answer_id)

    def get_tag(self, name: str):
        return self.tags.get(name)
