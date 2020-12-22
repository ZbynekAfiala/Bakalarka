from myproject.users.forms import LoginForm, RegistrationForm, UpdateUserForm
from flask import Blueprint, render_template, redirect, url_for, flash,request
from flask_login import login_user,current_user, logout_user, login_required
from myproject import db
from myproject.models import User, Zajezd
from myproject.users.picture_handler import add_profile_pic
from werkzeug.security import generate_password_hash, check_password_hash


users = Blueprint('users',__name__)

@users.route('/logout')
def logout():
    logout_user()
    #built in function
    return redirect(url_for("core.index"))

@users.route('/register',methods=["GET","POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
        password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Úspěšně jste se registrovali !')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)

@users.route('/login',methods=["GET","POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                flash('Úspěšně jste se přihlásili !')

                next = request.args.get('next')

                if next == None or not next[0]=='/':
                    next=url_for('core.index')

                    return redirect(next)

    return render_template("login.html", form=form)

@users.route('/account',methods=["GET","POST"])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Účet byl aktualizován')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename="profile_pics/"+current_user.profile_image)

    return render_template('account.html', profile_image = profile_image, form=form)

@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    zajezdy = Zajezd.query.filter_by(author=user).order_by(Zajezd.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_zajezdy_posts.html',zajezdy=zajezdy,user=user)
    #když jdeš na jednotlivýho uživatele ukážete to přímo zájezdy od něj.
