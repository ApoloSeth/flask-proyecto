from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user

from app import login_manager
from . import auth_bp
from .forms import SignUpForm, LoginForm
from .models import User

@auth_bp.route("/signup/", methods = ["GET", "POST"])
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
            return redirect(url_for("public.index"))
    return render_template("auth/signup_form.html", form = form, error=error)

@auth_bp.route("/login", methods=['GET','POST'])
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
            return redirect(url_for('public.index'))
    return render_template('auth/login_form.html', form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)