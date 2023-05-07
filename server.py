from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager


db = SQLAlchemy()

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Z j,j_;f.-7dtXThf@localhost/yavayer'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.signin'
login_manager.init_app(app)

from models.user_model import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

from routes.auth_routes import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from routes.main_routes import main as main_blueprint
app.register_blueprint(main_blueprint)

from routes.lk_routes import lk as lk_blueprint
app.register_blueprint(lk_blueprint, url_prefix='/lk')

from routes.assistant_routes import assistant as assistant_blueprint
app.register_blueprint(assistant_blueprint, url_prefix='/assistant')

app.run(debug=True)
