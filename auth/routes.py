from flask import (
    redirect,
    render_template,
    request,
    url_for,
    Blueprint,
    flash,
    session,
    make_response
)
from models import User, db

from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    jwt_required
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/user/register", methods=["GET", "POST"])
@jwt_required()
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
        return redirect(url_for("clients.form"))

@auth_bp.route("/api/user/delete", methods=["GET", "POST"])
@jwt_required()
def delete_user(): 
    if request.method == "GET":
        
        return render_template('delete_user.html')
    elif request.method == "POST":
        
        username = str(request.form.get('username'))
        print(type(username),username)
        user = User.query.filter_by(username=username).first()
        print (user)
        if not user:
            print(user)
            return "user not found", 404
        else:
            print(user)
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('auth.logout'))



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
@jwt_required()
def logout():
    access_token = request.cookies.get('access_token_cookie')
    print("Token en cookie:", access_token)
     
    session.pop("user", None)
    flash("te has deslogueado correctametne", "success")
    response =make_response(redirect(url_for("auth.login")))
    unset_jwt_cookies(response)
    return response
