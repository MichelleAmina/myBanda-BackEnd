from models import User
from seed import seed_database
from config import app, db, Flask, request, jsonify, Resource, api, make_response
# JWTManager, create_access_token, jwt_required, DecodeError, 

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

        user = User(username=username, email=email, role=role)
        user.password_hash = password
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
    
class Hello(Resource):
    def get(self):
        hello = 'Hello World!'
        return make_response(
            hello,
            200
        )

api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Hello, '/hello')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

# from config import app, db, api, request, session, Resource
