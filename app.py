
from flask import Flask
from config import Config
from models import  db
from clientes.routes import clients_bp
from users.routes import users_bp
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(clients_bp)
app.register_blueprint(users_bp)

