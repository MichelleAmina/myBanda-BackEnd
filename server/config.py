from flask import Flask, request, session, jsonify, make_response, url_for
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import datetime, timezone, timedelta
import os
from flask_session import Session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_mpesa import MpesaAPI
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_mail import Mail
from flask_mail import Message
# from flask_uploads import configure_uploads, IMAGES, UploadSet


# from jwt.exceptions import DecodeErrors

from dotenv import load_dotenv
load_dotenv()  

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://coin_sage_database_3def_user:c9aCoVrgAeDnCu3djBLqzSwxPHZWsGuk@dpg-cpepmo7109ks73fi5dh0-a.oregon-postgres.render.com/my_banda_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hbb36bh6kby45][mg]'
SECRET_KEY = app.config['SECRET_KEY'] = 'hbb36bh6kby45][mg]' 
app.config['JWT_SECRET_KEY'] = b'\x9d~\xaejx\xfe\xc5\xa1\xf6\xaa\x31\xdb\xb0k\xf7\x9d'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=72)
app.config['JWT_COOKIE_SECURE'] = False
app.config['SESSION_TYPE'] = 'filesystem' 
app.json.compact = False
app.config["API_ENVIRONMENT"] = "sandbox"
app.config["APP_KEY"] = "KaDetUGGhUCIlhHqmmvGfKFDSHXsL4GpvAsbR3s0Z6VjdOS8"
app.config["APP_SECRET"] = "CfUuAoAi3exAyAF0yju9P9zSaAzLAYtIfgHjsMnAVoad5ASGnqqRyDbJGRDtykX8"
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '55202118fd1a22'
app.config['MAIL_PASSWORD'] = '428503172768de'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

import cloudinary
          
# cloudinary.config( 
#   cloud_name = os.getenv('cloud_name'),
#   api_key = os.getenv('api_key'),
#   api_secret = os.getenv('api_secret')
# )

cloudinary.config( 
  cloud_name = 'dol3eg0to',
  api_key = '843678846326154',
  api_secret = 'qWeEH2FpH50S8ctME2xpv-tLKtI'
)

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
mpesa_api = MpesaAPI(app)
mail = Mail(app)
CORS(app)
Session(app)


# Initializing UploadSet
# photos = UploadSet('photos', IMAGES)

# # Defining the upload folder
# # app.config['UPLOAD_FOLDER'] = './server/uploads' 
# app.config['UPLOAD_FOLDER'] = '../server/uploads' 
# app.config['UPLOADED_PHOTOS_DEST'] = app.config['UPLOAD_FOLDER']

# # Creating the upload folder if it doesn't exist
# if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     os.makedirs(app.config['UPLOAD_FOLDER'])
#     print(f"Upload folder '{app.config['UPLOAD_FOLDER']}' created successfully.")
# else:
#     print(f"Upload folder '{app.config['UPLOAD_FOLDER']}' already exists.")

# # Configuring uploads
# configure_uploads(app, photos)
