from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


DEFAULT_IMAGE_URL='https://heatherchristenaschmidt.files.wordpress.com/2011/09/facebook_no_profile_pic2-jpg.gif'
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        """show info about user"""
        u = self
        return f'<user: id={u.id} name={u.first_name} last_name={u.last_name} image_url={u.image_url}>'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.TEXT,
                     nullable=False)

    last_name = db.Column(db.TEXT, nullable=False)

    image_url = db.Column(db.TEXT, nullable=False, default=DEFAULT_IMAGE_URL)

class Post(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        """show info about post"""
        p = self
        return f'<post: id={p.id} name={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}'
    
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)

    title=db.Column(db.Text,nullable=False)
    content=db.Column(db.Text,nullable=False)
    created_at=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    navigation=db.relationship('User',backref='post')

class Tag(db.Model):
    __tablename__ = "tags"

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.Text,unique=True)

    def __repr__(self):
        """show tag info"""
        t = self
        return f'<tag id={t.id} name={t.name}>'

    posts=db.relationship('Post',secondary='post_tags',backref='tags')

class PostTag(db.Model):
    __tablename__ = "post_tags"

    post_id=db.Column(db.Integer,db.ForeignKey('posts.id'),primary_key=True)
    tag_id=db.Column(db.Integer,db.ForeignKey('tags.id'),primary_key=True)

    def __repr__(self):
        """show post_tag info"""
        i = self
        return f'<postid post_id={i.post_id} tag_id={i.tag_id}>'



