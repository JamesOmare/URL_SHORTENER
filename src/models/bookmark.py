from datetime import datetime
import random
from ..utils import db
import string



class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text, nullable = True)
    url = db.Column(db.Text, nullable = False)
    short_url = db.Column(db.String(3), nullable = True)
    visits = db.Column(db.Integer, default = 0)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def generate_short_characters(self):
        #string.digits = [0-9], string.ascii_letters=[a-z]
        #you can use regex
        characters = string.digits+string.ascii_letters
        #the k=3 means 3characters 
        picked_chars = ''.join(random.choices(characters, k=3))
        link = self.query.filter_by(short_url=picked_chars).first()

        if link:
            self.generate_short_characters()
        else:
            return picked_chars


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    def __repr__(self) -> str:
        return f'Bookmark>>> {self.url}'

    @classmethod
    def get_short_url(cls, short_url):
        return cls.query.filter_by(short_url = short_url).first_or_404()
