from flask import render_template

from app.models import Post
from . import public_bp

@public_bp.route("/")
def index():
    posts = Post.get_all()
    return render_template("public/index.html", posts=posts)

@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    error = None
    if post is None:
        error = f'No se encontró ningún post con el título {slug}'
    return render_template("public/post_view.html", post=post, error=error)