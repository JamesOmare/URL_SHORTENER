from datetime import datetime
from ..utils import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.Text(), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    bookmarks = db.relationship(
        'Bookmark', 
        backref= 'user'
    )
    
    def __repr__(self) -> str:
        return f'User>>> {self.username}'


