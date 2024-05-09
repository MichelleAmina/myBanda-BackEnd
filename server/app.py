from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import db, User
from seed import seed_database
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from jwt.exceptions import DecodeError
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'hjtvgh546h3gv4'  
jwt = JWTManager(app)
api = Api(app)  

db.init_app(app)


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'User with this email already exists'}, 400

        user = User(username=username, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(identity=user.id)
        return {'message': 'Login successful', 'access_token': access_token}, 200

api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
