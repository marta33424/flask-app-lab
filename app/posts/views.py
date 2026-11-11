from flask import render_template, redirect, url_for, flash, request, abort, session
from app import db
from . import post_bp
from .models import Post
from .forms import PostForm


# 1. Створення поста (/post/create)
@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        author = session.get("username", "Anonymous")

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            author=author,
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.all_posts"))
    elif request.method == "POST":
        flash("Enter the correct data in the form!", "danger")

    return render_template("add_post.html", form=form, title="Create a New Post")


# 2. Список усіх активних постів за спаданням дати (/post)
@post_bp.route("", methods=["GET"])
@post_bp.route("/", methods=["GET"])
def all_posts():
    stmt = (
        db.select(Post)
        .where(Post.is_active == True)
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


# 3. Деталі конкретного поста (/post/<id>)
@post_bp.route("/<int:id>", methods=["GET"])
def detail_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)
    return render_template("detail_post.html", post=post)


# 4. Редагування поста (/post/<id>/update)
@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    form = PostForm(obj=post)

    if request.method == "GET" and post.posted:
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data
        db.session.commit()
        flash("Пост оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))
    elif request.method == "POST":
        flash("Enter the correct data in the form!", "danger")

    return render_template("add_post.html", form=form, title="Редагувати пост")


# 5. Видалення поста (/post/<id>/delete)
@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Пост успішно видалено.", "danger")
        return redirect(url_for("posts.all_posts"))

    return render_template("delete_confirm.html", post=post)