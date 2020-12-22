from flask import render_template,url_for,flash,request,redirect,Blueprint
from flask_login import current_user,login_required
from myproject import db
from myproject.models import Zajezd
from myproject.zajezdy.forms import ZajezdForm

zajezdy = Blueprint('zajezdy',__name__)

#create

@zajezdy.route("/create",methods=["GET","POST"])
@login_required
def create_post():
    form=ZajezdForm()

    if form.validate_on_submit():
        post = Zajezd(
        title=form.title.data,
        price=form.price.data,
        destination = form.destination.data,
        date_of_activity=form.date_of_activity.data,
        user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("core.index"))

    return render_template("create_post.html", form=form)

#view

@zajezdy.route('/<int:zajezd_id>')
def post(zajezd_id):
    zajezd = Zajezd.query.get_or_404(zajezd_id)
    return render_template('post.html',title=zajezd.title, date=zajezd.date,
    destination=zajezd.destination,price=zajezd.price,
    date_of_activity=zajezd.date_of_activity,post=zajezd)

#update
@zajezdy.route("/<int:zajezd_id>/update",methods=["GET","POST"])
@login_required
def update(zajezd_id):
    zajezd = Zajezd.query.get_or_404(zajezd_id)

    if zajezd.author != current_user:
        abort(403)
        #abort --> calls for error
    form = ZajezdForm()

    if form.validate_on_submit():

        zajezd.title = form.title.data
        zajezd.price = form.price.data
        zajezd.destination = form.destination.data
        zajezd.date_of_activity = form.date_of_activity.data

        db.session.commit()
        flash('Zajezd byl upraven!')
        return redirect(url_for('zajezdy.post',zajezd_id=zajezd.id))

    elif request.method == "GET":
        form.title.data = zajezd.title
        form.price.data = zajezd.price
        form.destination.data = zajezd.destination
        form.date_of_activity.data = zajezd.date_of_activity

    return render_template('create_post.html',title='Updating', form=form)

#delete
@zajezdy.route('/<int:zajezd_id>/delete',methods=["GET","POST"])
@login_required
def delete_post(zajezd_id):
    zajezd = Zajezd.query.get_or_404(zajezd_id)

    if zajezd.author != current_user:
        abort(403)

    db.session.delete(zajezd)
    db.session.commit()
    flash('Zájezd byl smazán !')
    return redirect(url_for('core.index'))

#view pro přihlašeného uživatele --> s kontaktem na vlastníka zájezdu
@zajezdy.route('/<int:zajezd_id>/show_contact')
@login_required
def view_email(zajezd_id):
    zajezd = Zajezd.query.get_or_404(zajezd_id)
    return render_template('view_post_with_email.html',title=zajezd.title, date=zajezd.date,
    destination=zajezd.destination,price=zajezd.price,date_of_activity=zajezd.date_of_activity,
    post=zajezd)
