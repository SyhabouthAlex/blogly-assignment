"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def redirect_to_users():
    return redirect("/users")

@app.route("/users")
def user_list():
    """List of users."""

    users = User.query.all()

    return render_template("list.html", users=users)

@app.route("/users/new")
def add_user_page():
    """Show form for adding a user."""

    return render_template("add.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """Add a new user using form submission data."""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_details(user_id):
    """Show options to edit or delete a user."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(author_id=user_id)

    return render_template("details.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Form to edit a user's information."""
    user = User.query.get_or_404(user_id)

    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit a user's information."""

    user = User.query.get(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"]
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a user's information."""

    user = User.query.filter_by(id=user_id).delete

    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def add_post_form(user_id):
    """Form to add a post for a user."""

    user = User.query.get(user_id)
    tags = Tag.query.all()

    return render_template("newpost.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add a post for a user."""

    title = request.form["title"]
    content = request.form["content"]
    user = User.query.get(user_id)
    tag_names = [tag for tag in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.name.in_(tag_names)).all()

    new_post = Post(title=title, content=content, author_id=user.id, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show a post from a user"""

    post = Post.query.get(post_id)
    tags = post.tags

    return render_template("postdetails.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Show a form to edit a post"""

    post = Post.query.get(post_id)
    tags = Tag.query.all()

    return render_template("postedit.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Edit a post using form data"""

    tag_names = [tag for tag in request.form.getlist("tags")]
    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    post.tags = Tag.query.filter(Tag.name.in_(tag_names)).all()

    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Show a form to delete a post"""

    post = Post.query.get(post_id)
    user_id = post.author_id

    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/tags")
def list_all_tags():
    """Show all tags"""

    tags = Tag.query.all()

    return render_template("tagslist.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """Show details about a tag"""

    tag = Tag.query.get(tag_id)

    return render_template("tagdetails.html", tag=tag)

@app.route("/tags/new")
def add_tag_form():
    """Show form for adding a tag"""

    return render_template("newtag.html")

@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Add a new tag using form submission data"""

    tag_name = request.form["name"]

    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """Show form for editing a tag"""

    tag = Tag.query.get(tag_id)

    return render_template("tagedit.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Edit a tag using form data"""

    tag = Tag.query.get(tag_id)
    tag.name = request.form["name"]

    db.session.commit()

    return redirect(f"/tags/{tag.id}")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag"""

    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect(f"/tags")