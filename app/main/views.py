from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import ReviewForm,UpdateProfile,BlogForm,CommentForm,SubscribeForm,UpdateForm
from ..models import User,Comment,Blog,Subscribe,Quote
from flask_login import login_required,current_user
from .. import db
from ..request import get_quote
from ..email import mail_message

@main.route('/')
def index():
    
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Blog about it !'
    quote=get_quote()
    blog = Blog.query.all()
    return render_template('index.html', title = title,quote = quote,blog = blog)

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

    
@main.route('/delete/blog,<int:id>', methods=['GET','POST'])
def delete_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    
    if blog is not None:
        blog.delete_blog()
        return redirect(url_for('main.index'))
    return render_template('index.html')

@main.route('/update/new/<int:id>', methods=['GET','POST'])
def upgrade_blogs(id):
    blogs=Blog.query.filter_by(id=id).first()

    if blogs is None:
        abort(404)

    form = UpdateForm()

    if form.validate_on_submit():

        blogs.blog=form.blog.data


        db.session.add(blogs)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('update.html',form = form,user= current_user) 

@main.route('/blog/new', methods=['GET','POST'])
def create_blogs():
    form = BlogForm()

    if form.validate_on_submit():
        title=form.title.data
        blog=form.blog.data

        new_blog=Blog(blog = blog,title = title,user= current_user)

        db.session.add(new_blog)
        db.session.commit()

        subscriber=Subscribe.query.all()
        for subscribe in subscriber:
           mail_message("New Blog Post","email/subscribe",subscribe.email,user=subscribe,blog=new_blog)

        return redirect(url_for('main.index'))

    return render_template('blog.html',form = form,user= current_user) 


@main.route('/delete/new/<int:id>', methods=['GET','POST'])
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    form = CommentForm()
    if comment is not None:
        comment.delete_comment()
        
    return render_template('comment.html', form = form)

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
def Subscribes():
    subscribeform=SubscribeForm()
    print(Subscribe.name)
    if subscribeform.validate_on_submit():
        name=subscribeform.name.data
        email=subscribeform.email.data
    
        new_sub=Subscribe(name=name,email=email)
        db.session.add(new_sub)
        db.session.commit()

        mail_message("Thank you for subscribing","email/subscriber",new_sub.email)
     
        return redirect(url_for('main.index'))

    return render_template('subscribe.html',subscribeform = subscribeform)     

