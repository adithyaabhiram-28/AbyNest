from smtplib import SMTPAuthenticationError
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flaskblog import bcrypt, db
from flaskblog.models import Post, User
from flaskblog.users.forms import LoginForm, RegistrationForm, ResetForm, ResetPasswordForm, UpdateForm
from flaskblog.users.utils import delete_picture, save_picture, send_email

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(uname=form.uname.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully! Login to continue", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and  bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful", "danger")
    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.uname = form.uname.data
        current_user.email = form.email.data
        if form.picture.data:
            # old_picture = current_user.image
            # pic_file = save_picture(form.picture.data)
            # current_user.image = pic_file
            # delete_picture(old_picture)
            if current_user.image_public_id:
                delete_picture(current_user.image_public_id)
            upload_data = save_picture(form.picture.data)
            current_user.image_url = upload_data["url"]
            current_user.image_public_id = upload_data["public_id"]
        db.session.commit()
        flash("Account updated successfully!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.uname.data = current_user.uname
        form.email.data = current_user.email
    # image = url_for("static", filename="profile_pics/"+current_user.image)
    # image = url_for("static", filename="profile_pics/default.jpg")
    image = current_user.image_url
    return render_template("account.html", title="Account", image=image, form=form)

@users.route("/user/<string:uname>")
@login_required
def user_posts(uname):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(uname=uname).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.desc())\
        .paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user, title=f"{user.uname}'s Posts")

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            send_email(user)
        except SMTPAuthenticationError:
            flash("Email login failed. Check EMAIL_USER and use a Google App Password for EMAIL_PASS.", "danger")
            return redirect(url_for("users.reset_request"))
        # flash("Email has been sent, reset your password.", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_token(token)
    if user is None:
        flash("Invalid or Expired Token", "danger")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Password updated successfully! Login to continue", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
