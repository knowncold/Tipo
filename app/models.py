from app import db
import datetime
import json

class Blog(db.Document):
    title = db.StringField()
    content = db.StringField()
    createTime = db.DateTimeField(default=datetime.datetime.now())
    createDay = db.DateTimeField(default=datetime.date.today())
    category = db.StringField(default='uncategoried')
    tag = db.ListField(db.StringField())
    pageview = db.IntField(default=0)
    month = db.StringField(default=datetime.datetime.strftime(datetime.date.today(), '%Y-%m'))

    def to_json(self):
        return {
                'title' : self.title,
                'content' : self.content,
                'createTime' : str(self.createTime),
                'createDay' : str(self.createDay),
                'category' : self.category,
                'pageview' : self.pageview,
                'tag' : self.tag
        }


class Comment(db.Document):
    name = db.StringField()
    content = db.StringField()
    createTime = db.DateTimeField(default=datetime.datetime.now())

class ErrorMessage():
    def __init__(self, status, msg):
        self.status = status
        self.msg = msg

    def __str__(self):
        return_msg = {'status':self.status, 'msg':self.msg}
        return json.dumps(return_msg)
        






