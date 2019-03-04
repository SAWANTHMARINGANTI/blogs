from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    blog = db.relationship('Blog',backref = 'user',lazy="dynamic")
    comment = db.relationship('Comment',backref = 'user',lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    blog = db.Column(db.String(955))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship("Comment", backref="blogs", lazy = "dynamic")

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()
    

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    usernames = db.Column(db.String(255),index = True)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()


class Subscribe(db.Model):
    __tablename__ = 'subscribes'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True)

class Quote():
    '''
    class that creates the quote instance
    '''

    def __init__(self,id,author,quote):
        self.id =  id
        self.author = author
        self.quote = quote
        