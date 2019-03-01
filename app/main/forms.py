from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required,Email

class ReviewForm(FlaskForm):

    title = StringField('Review title',validators=[Required()])
    review = TextAreaField('Movie review', validators=[Required()])
    submit = SubmitField('Submit')
    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
# class LoginForm(FlaskForm):
#     email = StringField('Your Email Address',validators=[Required(),Email()])
#     password = PasswordField('Password',validators =[Required()])
#     remember = BooleanField('Remember me')
#     submit = SubmitField('Sign In')

class BlogForm(FlaskForm):
    title = StringField('Post title',validators=[Required()])
    blog = TextAreaField('Post It !!', validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    usernames = TextAreaField('User Name', validators=[Required()])
    comment = TextAreaField('Post Of The Comment', validators=[Required()])
    submit = SubmitField('Submit')

class SubscribeForm(FlaskForm):
    name = StringField('Enter your Name',validators = [Required()])
    email = StringField('Your Email Address',validators=[Required(),Email()])
    submit = SubmitField('Submit')
   