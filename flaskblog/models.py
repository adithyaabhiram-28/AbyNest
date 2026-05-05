from datetime import datetime, timezone
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_url = db.Column(db.String(500), nullable=False, default="https://res.cloudinary.com/ds74jszcl/image/upload/v1777964984/default_vlnm6j.jpg")
    image_public_id = db.Column(db.String(200), nullable=True)
    # image = db.Column(db.String(60), default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_token(token, expires=600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires)['user_id']
        except (BadSignature, SignatureExpired):
            return None
        return User.query.get(user_id)

    def __repr__(self):
        # return f"User('{self.uname}',{self.email}','{self.image}')"
        return f"User('{self.uname}', '{self.email}', '{self.image_url}')"

class Post(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: 
    datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date}')"
