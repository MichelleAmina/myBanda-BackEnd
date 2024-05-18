from models import User, Product, ProductsImages, Shop, Order, Review, OrderItem
# from seed import seed_database
from config import app, db, Flask, request, jsonify, Resource, api, make_response, JWTManager, create_access_token, jwt_required, session,datetime, timezone, timedelta
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
        
        # storing the session in the user Id
        session['user_id'] = user.id


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

class Orders(Resource):
    @jwt_required()
    def get(self):
        user_id = session.get('user_id')
        
        if not user_id:
            return {'message': 'User not logged in'}, 401
        
        orders = [order.to_dict() for order in Order.query.all()]
        if not orders:
            return {"message": "Orders are not added"}, 404

        return make_response(
            orders, 
            200
            )
    
    @jwt_required()
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'message': 'User not logged in'}, 401
        
        
        data = request.get_json()
        user_id = data.get('user_id')
        total_price = data.get('total_price')
        status = data.get('status')
        delivery_fee = data.get('delivery_fee')
        delivery_address = data.get('delivery_address')
        
        # Getting the current time
        created_at = datetime.now(timezone.utc)

        order = Order(user_id=user_id, total_price=total_price, status=status, delivery_fee=delivery_fee ,delivery_address=delivery_address, created_at=created_at)
        db.session.add(order)
        db.session.commit()

        return make_response(
            order.to_dict(), 
            201
            )


class OrderItems(Resource):
    @jwt_required()
    def get(self):
        order_items = [order_item.to_dict() for order_item in OrderItem.query.all()]
        
        if not order_items:
            return {"message": "Order Items are not added"}, 404

        return make_response(
            order_items, 
            200
            )
    
    @jwt_required()
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'message': 'User not logged in'}, 401
        
        data = request.get_json()
        order_id = data.get('order_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
        db.session.add(order_item)
        db.session.commit()

        return make_response(
            order_item.to_dict(), 
            201
            )



class Reviews(Resource):
    @jwt_required()
    def get(self):
        reviews = [review.to_dict() for review in Review.query.all()]
        
        if not reviews:
            return {"message": "Reviews not yet added"}, 404

        return make_response(
            reviews, 
            200
            )
    
    @jwt_required()
    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'message': 'User not logged in'}, 401
        
        
        
        data = request.get_json()
        content = data.get('content')
        rating = data.get('rating')
        buyer_id = data.get('buyer_id')
        seller_id = data.get('seller_id')
        product_id = data.get('product_id')

        review = Review(content=content, buyer_id=buyer_id, seller_id=seller_id, product_id=product_id, rating=rating)
        db.session.add(review)
        db.session.commit()

        return make_response(
            review.to_dict(), 
            201
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
api.add_resource(Orders, '/order')
api.add_resource(OrderItems, '/orderitems')
api.add_resource(Reviews, '/review')



if __name__ == '__main__':
    app.run(port=5555, debug=True)


