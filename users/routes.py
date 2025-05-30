from flask import jsonify, redirect, render_template, request, url_for, Blueprint
from models import User, db

users_bp = Blueprint("users", __name__)


@users_bp.route("/api/users")
def get_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@users_bp.route("/api/user/register", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        new_user = User(
            username=request.form.get("username"), password=request.form.get("password")
        )
        db.session.add(new_user)
        db.session.commit()
        print(new_user)
        return redirect(url_for("users.get_users"))


@users_bp.route("/api/user/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username, password = request.form.get("username"), request.form.get("password")
        find_user = User.query.filter_by(username=username).first()
        if not find_user:
            return "Not found"
        else:
            if not password == find_user.password:
                return redirect(url_for("users.login"))
            else:
                return redirect(url_for("clients.create_client"))
