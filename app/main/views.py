from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm,UpdateProfile,CreatePitches,CommentForm
from ..models import User,Pitch,Comment
from flask_login import login_required,current_user
from .. import db

@main.route('/')
def index():
    
    '''
    View root page function that returns the index page and its data
    '''
    title = '60sec-Pitch'
    pitch = Pitch.query.all()
    return render_template('index.html', title = title,pitch = pitch)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/pitch/new', methods=['GET','POST'])
@login_required
def create_pitches():
    form = CreatePitches()

    if form.validate_on_submit():

        pitch=form.pitch.data

        new_pitch=Pitch(pitch = pitch,user= current_user)

        db.session.add(new_pitch)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('pitches.html',form = form)    

@main.route('/comment/new/<int:id>', methods=['GET','POST'])
@login_required
def create_comments(id):

    form = CommentForm()

    if form.validate_on_submit():

        comment=form.comment.data

        new_comment= Comment(comment= comment,pitches_id = id,user= current_user)
        db.session.add(new_comment)
        db.session.commit()

    comment = Comment.query.filter_by(pitches_id=id).all()
        

    return render_template('comment.html',comment = comment, form = form)        


        
