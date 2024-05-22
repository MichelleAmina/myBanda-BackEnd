from flask import Flask, request, session, jsonify, make_response,url_for
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone, timedelta
import os
from flask_session import Session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_mail import Mail
from flask_mail import Message
# from jwt.exceptions import DecodeErrors

from dotenv import load_dotenv
load_dotenv()  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hbb36bh6kby45][mg]'
SECRET_KEY = app.config['SECRET_KEY'] = 'hbb36bh6kby45][mg]'   
app.config['JWT_SECRET_KEY'] = b'\x9d~\xaejx\xfe\xc5\xa1\xf6\xaa\x31\xdb\xb0k\xf7\x9d'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=72)
app.config['JWT_COOKIE_SECURE'] = False
app.config['SESSION_TYPE'] = 'filesystem' 
app.json.compact = False
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '55202118fd1a22'
app.config['MAIL_PASSWORD'] = '428503172768de'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

sender_email = os.environ.get('EMAIL')
sender_password = os.environ.get('PASSWORD')


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app)
api = Api(app)
bcrypt = Bcrypt(app)
CORS(app)
Session(app)
mail = Mail(app)




