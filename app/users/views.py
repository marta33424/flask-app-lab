from urllib.parse import urlparse
from flask import render_template, request, redirect, url_for, flash, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
from .. import db, bcrypt
from . import users_bp
from .forms import RegistrationForm
from .models import User


@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)


@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f"Акаунт створено для {form.username.data}! Тепер можете увійти.", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form, title="Register")


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    if request.method == "POST":
        login_input = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember") in ("on", "true", "1")

        user = User.query.filter(
            (User.username == login_input) | (User.email == login_input)
        ).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash(f"Вітаю, {user.username}! Вхід успішний.", "success")

            next_page = request.args.get("next")
            if next_page and urlparse(next_page).netloc == "":
                return redirect(next_page)
            return redirect(url_for("users.account"))
        else:
            flash("Wrong data! Try again!", "error")
            return redirect(url_for("users.login"))

    return render_template("login.html", title="Login")


@users_bp.route("/account")
@login_required
def account():
    return render_template(
        "account.html",
        title="Account",
        username=current_user.username,
        user=current_user,
    )


@users_bp.route("/users-list")
@login_required
def users_list():
    users = User.query.order_by(User.id).all()
    return render_template(
        "users_list.html",
        title="Users",
        users=users,
        users_count=len(users),
    )


@users_bp.route("/profile")
def profile():
    if not current_user.is_authenticated:
        flash("Будь ласка, спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

    current_theme = request.cookies.get("theme", "light")
    return render_template(
        "profile.html",
        username=current_user.username,
        cookies=request.cookies,
        theme=current_theme,
    )


@users_bp.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/cookies/add", methods=["POST"])
def add_cookie():
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    max_age = request.form.get("max_age", "").strip()

    if not key:
        flash("Ключ кукі не може бути порожнім!", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    try:
        max_age_val = int(max_age) if max_age else None
    except ValueError:
        max_age_val = None

    response.set_cookie(key, value, max_age=max_age_val)
    flash(f"Кукі '{key}' успішно додано!", "success")
    return response


@users_bp.route("/cookies/delete", methods=["POST"])
def delete_cookie():
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    if not key:
        flash("Вкажіть ключ кукі для видалення!", "error")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)
    flash(f"Кукі '{key}' успішно видалено!", "info")
    return response


@users_bp.route("/cookies/delete_all", methods=["POST"])
def delete_all_cookies():
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))

    response = make_response(redirect(url_for("users.profile")))
    for key in request.cookies.keys():
        if key != "session":
            response.delete_cookie(key)

    flash("Всі додані кукі успішно видалено!", "info")
    return response


@users_bp.route("/change-theme/<string:theme_name>")
def change_theme(theme_name):
    if not current_user.is_authenticated:
        return redirect(url_for("users.login"))

    if theme_name not in ["light", "dark"]:
        theme_name = "light"

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("theme", theme_name, max_age=30 * 24 * 60 * 60)
    flash(f"Тему змінено на {theme_name}!", "info")
    return response