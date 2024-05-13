from models import User, Product, ProductsImages, Shop
# from seed import seed_database
from config import app, db, Flask, request, jsonify, Resource, api, make_response, JWTManager, create_access_token, jwt_required
import json


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        location = data.get('location')
        contact = data.get('contact')
        role = data.get('role')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'User with this email already exists'}, 400

        user = User(username=username, email=email, location=location, contact=contact ,role=role)
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
        if not user or not user.authenticate(password):
            return {'message': 'Invalid email or password'}, 401

        access_token = create_access_token(identity=user.id)
        return {'message': 'Login successful', 'access_token': access_token}, 200


class Products(Resource):
    def get(self):
        
        products = [product.to_dict() for product in Product.query.all()]

        if not products:
            return {"message":"Add products!"}, 404

        return make_response(
            products,
            200
        )
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        # image_url = data.get('image_url')
        quantity_available = data.get('quantity_available')
        category = data.get('category')
        # seller_id = data.get('seller_id')
        shop_id = data.get('shop_id')

        product = Product(name=name, description=description, price=price, quantity_available=quantity_available, category=category, shop_id=shop_id) 
        db.session.add(product)
        db.session.commit()

        response = "Added succesfully"
        # product.image_url = json.loads(product.image_url)

        return make_response(
            product.to_dict(),
            200
        )
    
class Images(Resource):
    def post(self):
        data = request.get_json()

        image_url = data.get('image_url')
        product_id = data.get('product_id')

        image = ProductsImages(image_url=image_url, product_id=product_id)
        db.session.add(image)
        db.session.commit()

        return make_response(
            image.to_dict(),
            200
        )
    
class Shops(Resource):
    def post(self):
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')
        logo_image_url = data.get('logo_image_url')
        banner_image_url = data.get('banner_image_url')
        seller_id = data.get('seller_id')

        shop = Shop(name=name, description=description, logo_image_url=logo_image_url, banner_image_url=banner_image_url, seller_id=seller_id)
        db.session.add(shop)
        db.session.commit()

        return make_response(
            shop.to_dict(),
            200
        )

class Hello(Resource):
    def get(self):
        hello = 'Hello World!'
        return make_response(
            hello,
            200
        )

api.add_resource(Products, '/products')
api.add_resource(SignUp, '/signup' )
api.add_resource(Login, '/login')
api.add_resource(Hello, '/hello')
api.add_resource(Images, '/images')
api.add_resource(Shops, '/shop')



if __name__ == '__main__':
    app.run(port=5555, debug=True)

# from config import app, db, api, request, session, Resource
