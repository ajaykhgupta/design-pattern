from datetime import datetime

class Comment:
    def __init__(self, content, author):
        self.id = id(self)
        self.content = content
        self.author = author
        self.creation_date = datetime.now()
