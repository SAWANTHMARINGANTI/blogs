from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm,UpdateProfile,BlogForm,CommentForm,SubscribeForm
from ..models import User,Comment,Blog,Subscribe
from flask_login import login_required,current_user
from .. import db

@main.route('/')
def index():
    
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Blog about it !'
    blog = Blog.query.all()
    return render_template('index.html', title = title,blog = blog)

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

@main.route('/blog/new', methods=['GET','POST'])
@login_required
def create_blogs():
    form = BlogForm()

    if form.validate_on_submit():
        title=form.title.data
        blog=form.blog.data

        new_blog=Blog(blog = blog,title = title,user= current_user)

        db.session.add(new_blog)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('blog.html',form = form,user= current_user)    

@main.route('/comment/new/<int:id>', methods=['GET','POST'])
def create_comments(id):

    form = CommentForm()

    if form.validate_on_submit():
        usernames=form.usernames.data
        comment=form.comment.data

        new_comment= Comment(comment= comment,usernames = usernames,blog_id = id,user= current_user)
        db.session.add(new_comment)
        db.session.commit()

    comment = Comment.query.filter_by(blog_id=id).all()
        

    return render_template('comment.html',comment = comment, form = form)        

@main.route('/subs/new/', methods=['GET','POST'])    
def Subscribe():
    form=SubscribeForm()

    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
    
        new_subscribe = Subscribe( name = name, email = email)
        db.session.add(new_subscribe)
        db.session.commit()

        flash('subscription complete')
        return redirect(url_for('main.index'))



    return render_template('subscribe.html',form = form,user= current_user)     
