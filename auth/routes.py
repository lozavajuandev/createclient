from flask import (
    redirect,
    jsonify,
    render_template,
    request,
    url_for,
    Blueprint,
    flash,
    session,
)
from models import User, db

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/user/register", methods=["GET", "POST"])
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
        return redirect(url_for("auth.get_users"))


@auth_bp.route("/api/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username, password = request.form.get("username"), request.form.get("password")
        find_user = User.query.filter_by(username=username).first()
        if not find_user or not password == find_user.password:
            flash("Invalid credentials", "error")
            return redirect(url_for("auth.login"))
        else:
            id_user = find_user.id
            flash("Log In Exitoso", "success")
            session["user"] = id_user
            access_token = create_access_token(identity=username)
            resp = redirect(url_for("clients.form"))
            set_access_cookies(resp, access_token)

            return resp


@auth_bp.route("/api/logout")
def logout():
    session.pop("user", None)
    flash("te has deslogueado correctametne", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/api/test", methods=["GET"])
@jwt_required()
def test():
    username = get_jwt_identity()
    print(username)
    return "Secretdata"
