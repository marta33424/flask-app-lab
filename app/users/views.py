from flask import render_template, request, redirect, url_for, flash, session
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

    return render_template("profile.html", username=session["username"])

@users_bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("username", None)
    flash("Ви успішно вийшли з системи.", "info")
    return redirect(url_for("users.login"))