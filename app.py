
from flask import Flask
from config import Config
from models import  db
from clientes.routes import clients_bp
from auth.routes import auth_bp
from flask_jwt_extended import JWTManager
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(clients_bp)
app.register_blueprint(auth_bp)
jwt = JWTManager(app)
