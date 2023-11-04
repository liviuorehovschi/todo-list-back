from datetime import datetime
from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    lists = db.relationship('List', backref='author', lazy=True)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

    def to_dict(self, recursive=True):
        list_dict = {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "tasks": [task.to_dict() for task in self.tasks],
        }
        
        return list_dict

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)  # For hierarchy
    is_complete = db.Column(db.Boolean, default=False)  # To mark tasks as complete

    children = db.relationship('Task', backref=db.backref('parent', remote_side=[id]))  # For hierarchy

    def to_dict(self, recursive=True):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "list_id": self.list_id,
            "parent_id": self.parent_id,
            "date_posted": self.date_posted.strftime('%Y-%m-%d %H:%M:%S'),  # Convert to string for serialization
            "is_complete": self.is_complete
        }
        if recursive:
            task_dict["children"] = [child.to_dict() for child in self.children]
        return task_dict
