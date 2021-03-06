"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(30),
                    nullable=False)
    last_name = db.Column(db.String(30),
                    nullable=False)
    image_url = db.Column(db.String(50))
    posts = db.relationship("Post",
                    backref="author",
                    cascade="all, delete-orphan")

    def __repr__(self):
        """Show user info."""
        u = self
        return f"User {u.id} {u.first_name} {u.last_name} {u.image_url}"

class Post(db.Model):
    """Blog posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    created_at = db.Column(db.DateTime,
                    nullable=False,
                    default=datetime.datetime.now)
    author_id = db.Column(db.Integer,
                    db.ForeignKey("users.id"),
                    nullable=False)
    tags = db.relationship("Tag",
                    secondary="post_tags",
                    backref="posts")
                                    
class Tag(db.Model):
    """Tags for posts"""
    
    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(20),
                    nullable=False,
                    unique=True)
    
class PostTag(db.Model):
    """Tags of posts"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                    db.ForeignKey("posts.id"),
                    primary_key=True)
    tag_id = db.Column(db.Integer,
                    db.ForeignKey("tags.id"),
                    primary_key=True)