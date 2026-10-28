from flask import render_template, request, redirect, url_for, flash, session, make_response
from . import users_bp

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)

VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Wrong data! Try again!", "error")
            return redirect(url_for("users.login"))

    return render_template("login.html")

@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Будь ласка, спочатку увійдіть у систему.", "error")
        return redirect(url_for("users.login"))

    return render_template("profile.html", username=session["username"], cookies=request.cookies)

@users_bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("username", None)
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for("users.login"))

@users_bp.route("/cookies/add", methods=["POST"])
def add_cookie():
    if "username" not in session:
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
    if "username" not in session:
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
    if "username" not in session:
        return redirect(url_for("users.login"))

    response = make_response(redirect(url_for("users.profile")))
    for key in request.cookies.keys():
        if key != "session":
            response.delete_cookie(key)

    flash("Всі додані кукі успішно видалено!", "info")
    return response