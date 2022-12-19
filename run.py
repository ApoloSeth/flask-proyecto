from flask import Flask, render_template, request, redirect, url_for
from forms import SignUpForm, PostForm, LoginForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:PGodrojasb852456@localhost:5432/miniblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

login_manager = LoginManager(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)
from models import User, Post

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    posts = Post.get_all()
    return render_template("index.html", posts=posts)

@app.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    error = None
    if post is None:
        error = f'No se encontró ningún post con el título {slug}'
    return render_template("show_post.html", post=post, error=error)

@app.route("/admin/post/", methods=['GET','POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>", methods=['GET','POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(user_id = current_user.id, title = title, content = content)
        post.save()
        
        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)

@app.route("/signup/", methods = ["GET", "POST"])
def signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    error = None
    if form.validate_on_submit():
        nombre = form.name.data
        email = form.email.data
        password = form.password.data
        #Comprobamos que no hay un usuario registrado con ese email
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya se encuentra registrado'
        else:
        # Creamos el objeto user y lo guardamos
            user = User(nombre=nombre, email=email)
            user.set_password(password)
            user.save()
        #Dejamos al usuario logeado
            login_user(user, remember=True)
            next = request.args.get('next',None)
            if next:
                return redirect(next)
            return redirect(url_for("index"))
    return render_template("signup_form.html", form = form, error=error)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember= form.remember_me.data)
            next_page = request.args.get('next')
            if next_page == '/admin/post/':
                next_page = 'post_form'
            if next_page:
                return redirect(url_for(next_page))
            return redirect(url_for('index'))
    return render_template('login_form.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))