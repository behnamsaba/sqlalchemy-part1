"""Blogly application."""
from flask import Flask,render_template,request,redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db,connect_db, User, Post
from datetime import date

app = Flask(__name__)
app.app_context().push()


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'project'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def users():
    users=User.query.all()
    return render_template('users.html',users=users)



@app.route('/users/new',methods=["POST","GET"])
def create():
    if request.method == "POST":
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        try:
            image_url=request.form('image_url')
            new_user=User(first_name=first_name,last_name=last_name,image_url=image_url)
        except:
            new_user=User(first_name=first_name,last_name=last_name)

        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')
        
    return render_template('add.html')

@app.route('/users/<int:users_id>')
def details(users_id):
    user = User.query.get_or_404(users_id)
    posts=Post.query.all()
    return render_template('details.html',user=user,posts=posts)
    



@app.route("/users/<int:users_id>/edit",methods=["POST","GET"])
def edit(users_id):
    user = User.query.get_or_404(users_id)
    if request.method == "POST":
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        image_url=request.form.get('image_url')
        user.first_name=first_name
        user.last_name=last_name
        user.image_url=image_url
        db.session.commit()
        flash('You were successfully added a post')
        return redirect('/users')


    return render_template('edit.html',user=user)

@app.route('/users/<int:users_id>/delete')
def delete(users_id):
    user = User.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:users_id>/posts/new',methods=['GET','POST'])
def form_post(users_id):
    user = User.query.get_or_404(users_id)
    if request.method == "POST":
        title=request.form['title']
        content=request.form['content']
        created_at=date.today()
        user_id=user.id
        new_post=Post(title=title,content=content,created_at=created_at,user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/users/{user_id}')

    return render_template('post.html',user=user)

@app.route('/posts/<int:post_id>')
def post_info(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html",post=post)

@app.route('/posts/<int:post_id>/edit',methods=['GET','POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        title=request.form['title']
        content=request.form['content']
        post.title=title
        post.content=content
        db.session.commit()
        return redirect('/users')

    return render_template('edit_post.html',post=post)

@app.route('/posts/<int:post_id>/delete')
def post_del(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted")


    return redirect('/users')