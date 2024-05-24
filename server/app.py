from models import User, Product, ProductsImages, Shop, Order, Review, OrderItem, Transaction, LikedProduct
# from seed import seed_database
from config import app, db, Flask, request, jsonify, Resource, api, make_response, JWTManager, create_access_token, jwt_required, session,datetime, timezone, timedelta, mpesa_api, mail, Message, url_for, sender_email, sender_password
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

class SignUp(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            location = data.get('location')
            contact = data.get('contact')
            role = data.get('role')

            # Validating the email format
            try:
                valid = validate_email(email)
                email = valid.email  
            except EmailNotValidError as e:
                return {'message': str(e)}, 400 

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {'message': 'User with this email already exists'}, 400

            user = User(username=username, email=email, location=location, contact=contact, role=role)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()

            return {'message': 'User created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            user = User.query.filter_by(email=email).first()
            if not user or not user.authenticate(password):
                return {'message': 'Invalid email or password'}, 401
            
            # session['user_id'] = user.id
            access_token = create_access_token(identity=user.id)
            return {'message': 'Login successful', 'access_token': access_token, 'role': user.role}, 200
        except Exception as e:
            return {'message': str(e)}, 500
        

class Users(Resource):
    def get(self):
        
        users = [user.to_dict() for user in User.query.all()]

        if not users:
            return {"message":"No users to display!"}, 404

        return make_response(
            users,
            200
        )

class UserIndex(Resource):
    def get(self, id):

        user = User.query.filter(User.id == id).first()

        if not user:
            return {"message":"User does not exist!"}, 404

        return make_response(
            user.to_dict(),
            200
        )
        
class DeleteUser(Resource):
    @jwt_required()
    def delete(self, user_id):
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user or current_user.role != 'banda_admin':
                return {'message': 'Admin privileges required'}, 403
            
            user = User.query.get(user_id)
            
            if not user:
                return {'message': 'User not found'}, 404

            Review.query.filter_by(buyer_id=user_id).delete()
            Review.query.filter_by(seller_id=user_id).delete()
            
            Order.query.filter_by(buyers_id=user_id).delete()
            Order.query.filter_by(delivery_id=user_id).delete()

            db.session.delete(user)
            db.session.commit()
            return {'message': 'User and related data deleted successfully'}, 200
        
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500


class ProductIndex(Resource):
    def get(self, id):
        try:
            product = Product.query.filter_by(id=id).first()
            if not product:
                return {"message": "Product not found"}, 404
            return product.to_dict(), 200
        except Exception as e:
            return {"message": str(e)}, 500
    
    def patch(self, id):
        try:
            data = request.get_json()
            product = Product.query.filter_by(id=id).first()
            if not product:
                return {"message": "Product not found"}, 404

            for key, value in data.items():
                setattr(product, key, value)
            db.session.commit()

            return product.to_dict(), 200
        except Exception as e:
            return {"message": str(e)}, 500

class Products(Resource):
    def get(self):
        try:
            products = [product.to_dict() for product in Product.query.all()]

            if not products:
                return {"message": "Add products!"}, 404

            return make_response(
                products,
                200
            )
        except Exception as e:
            return {"message": str(e)}, 500
    
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        image_url = data.get('image_url')
        quantity_available = data.get('quantity_available')
        category = data.get('category')
        shop_id = data.get('shop_id')
        tag = data.get('get')


        product = Product(name=name, description=description, price=price, quantity_available=quantity_available, category=category, shop_id=shop_id, tag=tag) 
        db.session.add(product)
        db.session.commit()
        image = ProductsImages(image_url=image_url, product=product)
        db.session.add(image)
        db.session.commit()

        # product.image_url = json.loads(product.image_url)

        return make_response(
            product.to_dict(),
            201
        )
    
class Images(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            image_url = data.get('image_url')
            product_id = data.get('product_id')

            if not image_url or not product_id:
                return {"message": "image_url and product_id are required fields!"}, 400

            image = ProductsImages(image_url=image_url, product_id=product_id)
            db.session.add(image)
            db.session.commit()

            return make_response(
                image.to_dict(),
                201
            )
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
    
class ShopIndex(Resource):
    def get(self, id):

        shop = Shop.query.filter(Shop.id == id).first()

        return make_response(
            shop.to_dict(),
            200
        )
    
class Shops(Resource):
    def get(self):
        shops = [shops.to_dict() for shops in Shop.query.all()]

        if not shops:
            return {"message":"No shops!"}, 404

        return make_response(
            shops,
            200
        )

    def post(self):
        try:
            data = request.get_json()

            name = data.get('name')
            description = data.get('description')
            logo_image_url = data.get('logo_image_url')
            banner_image_url = data.get('banner_image_url')
            seller_id = data.get('seller_id')
            contact = data.get('contact')
            location = data.get('location')

            if not name or not seller_id:
                return {"message": "name and seller_id are required fields!"}, 400

            shop = Shop(name=name, description=description, logo_image_url=logo_image_url, banner_image_url=banner_image_url, seller_id=seller_id, contact=contact, location=location)
            db.session.add(shop)
            db.session.commit()

            return make_response(
                shop.to_dict(),
                200
            )
        
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
    
class OrderIndex(Resource):
    @jwt_required()
    def get(self, order_id):
        try:
            order = Order.query.filter_by(id=order_id).first()
            if not order:
                return {"message": "Order not found"}, 404
            return order.to_dict(), 200
        except Exception as e:
            return {"message": str(e)}, 500  
        
    
    @jwt_required()
    def patch(self, order_id):
        try:
            user_id = get_jwt_identity()
            
            if not user_id:
                return {'message': 'User not logged in'}, 401

            data = request.get_json()
            new_status = data.get('status')

            if not new_status:
                return {'message': 'New status not provided'}, 400

            order = Order.query.filter_by(id=order_id, buyers_id=user_id).first()
            if not order:
                return {'message': 'Order not found'}, 404

            order.status = new_status
            db.session.commit()

            return make_response(order.to_dict(), 200)
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

class Orders(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            
            if not user_id:
                return {'message': 'User not logged in'}, 401
            
            orders = [order.to_dict() for order in Order.query.all()]
            if not orders:
                return {"message": "Orders are not added"}, 404

            return make_response(
                orders, 
                200
                )
    
        except Exception as e:
            return {"message": str(e)}, 500

    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return {'message': 'User not logged in'}, 401

            data = request.get_json()
            if not data:
                return {'message': 'No data provided'}, 400

            total_price = data.get('total_price')
            status = data.get('status')
            delivery_fee = data.get('delivery_fee')
            delivery_address = data.get('delivery_address')
            contact = data.get('contact')
            name = data.get('name')
            country = data.get('country')
            city = data.get('city')
            delivery_persons = data.get('delivery_persons')

            if None in [total_price, status, delivery_fee, delivery_address]:
                return {'message': 'Required field(s) missing'}, 400

            # Getting the current time
            created_at = datetime.now(timezone.utc)

            order = Order(buyers_id=user_id, total_price=total_price, status=status, delivery_fee=delivery_fee, delivery_address=delivery_address, created_at=created_at, contact=contact, name=name, country=country, city=city, delivery_persons=delivery_persons)
            db.session.add(order)
            db.session.commit()
            return make_response(order.to_dict(), 201)
        
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500


class OrderItems(Resource):
    @jwt_required()
    def get(self):
        try:
            order_items = [order_item.to_dict() for order_item in OrderItem.query.all()]
            if not order_items:
                return {"message": "Order Items are not added"}, 404

            return make_response(order_items, 200)
        except Exception as e:
            return {"message": str(e)}, 500
    
    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return {'message': 'User not logged in'}, 401
            
            data = request.get_json()
            if not data:
                return {'message': 'No data provided'}, 400

            order_id = data.get('order_id')
            product_id = data.get('product_id')
            quantity = data.get('quantity')

            if None in [order_id, product_id, quantity]:
                return {'message': 'Required field(s) missing'}, 400

            # Checking if the order exists
            order = Order.query.get(order_id)
            if not order:
                return {'message': 'Order does not exist'}, 404

            # Checking if the product exists
            product = Product.query.get(product_id)
            if not product:
                return {'message': 'Product does not exist'}, 404

            order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
            db.session.add(order_item)
            db.session.commit()

            return make_response(order_item.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
        

class Reviews(Resource):
    @jwt_required()
    def get(self):
        try:
            reviews = [review.to_dict() for review in Review.query.all()]
            if not reviews:
                return {"message": "Reviews not yet added"}, 404

            return make_response(reviews, 200)
        except Exception as e:
            return {"message": str(e)}, 500
    
    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return {'message': 'User not logged in'}, 401

            data = request.get_json()
            if not data:
                return {'message': 'No data provided'}, 400

            content = data.get('content')
            rating = data.get('rating')
            buyer_id = user_id  # the logged-in user is the buyer
            seller_id = data.get('seller_id')
            product_id = data.get('product_id')

            if None in [content, rating, seller_id, product_id]:
                return {'message': 'Required field(s) missing'}, 400

            # Checking if the seller and product exist before adding them
            seller = User.query.get(seller_id)
            product = Product.query.get(product_id)
            if not seller or not product:
                return {'message': 'Seller or product does not exist'}, 404

            review = Review(content=content, buyer_id=buyer_id, seller_id=seller_id, product_id=product_id, rating=rating)
            db.session.add(review)
            db.session.commit()

            return make_response(review.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
        
class Prompt(Resource):
    def post(self):
        data = request.get_json()

        number = data['contact']
        amount = data['amount']
        # number = "254700622570"
        # amount = '2'

        data = {
        "business_shortcode": "174379",
        "passcode": "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",
        "amount": amount,
        "phone_number": number,
        "reference_code": "Banda",
        "callback_url": "https://mybanda-backend-88l2.onrender.com/stk",
        "description": "Reverse afterwards"
        }
        resp = mpesa_api.MpesaExpress.stk_push(**data)
        return resp,200

class STK(Resource):
    def post(self):
        json_data = request.get_json()
        result_code = json_data["Body"]["stkCallback"]["ResultCode"]
        message = {
            "ResultCode": result_code,
            "ResultDesc": "success",
            "ThirdPartyTransID": "h234k2h4krhk2"
        }

        if result_code == 0:
            amt = json_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
            code = json_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
            date = json_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]   
            num = json_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]

            transaction = Transaction(Amount=amt, MpesaReceiptNumber=code,TransactionDate=date,PhoneNumber=num)
            db.session.add(transaction)
            db.session.commit()

        return message,200
    
class Paybill(Resource):
    def get(self):
        number = "254796277018"
        amount = '1'

        reg_data={
            "shortcode": "174379",
            "response_type": "Completed",
            "validation_url": "https://mybanda-backend-88l2.onrender.com/paybill"
        }
        v = mpesa_api.C2B.register(**reg_data)

        test_data={
            "shortcode": "174379",
            "command_id": "CustomerBuyGoodsOnline",
            "amount": amount,
            "msisdn": number,
            "bill_ref_number": "Banda goods payment"
        }
        new_v = mpesa_api.C2B.simulate(**test_data)
        return jsonify(new_v), 200
    
    def post(self):
        json_data = request.get_json()

        code = json_data["TransID"]
        date = json_data["TransTime"]
        num = json_data["MSISDN"]
        amt = json_data["TransAmount"]

        transaction = Transaction(Amount=amt, MpesaReceiptNumber=code, TransactionDate=date, PhoneNumber=num)
        db.session.add(transaction)
        db.session.commit()

        return json_data, 200

class Transactions(Resource):
    def get(self):
        transaction = [transaction.to_dict() for transaction in Transaction.query.all()]
        
        if not transaction:
            return {"message": "Transactions not yet added"}, 404

        return make_response(
            transaction, 
            200
            )

class LikedProducts(Resource):
    def get(self):

        liked = [liked.to_dict() for liked in LikedProduct.query.all()]

        if not liked:
            return [], 404
        
        return make_response(
            liked,
            200
        )
    
    def post(self):

        data = request.get_json()

        product_id = data["product_id"]
        # buyers_id = session['user_id']


        buyers_id = 108

        if None in [buyers_id, product_id]:
                return {'message': 'Required field(s) missing'}, 400
        
        # Checking if the product exists
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product does not exist'}, 404

        
        buyer = User.query.get(buyers_id)
        if not buyer:
            return {'message': 'Buyer does not exist'}, 404
        
        exists = LikedProduct.query.filter(LikedProduct.product_id == product_id).first()
        if exists:
            return {'message': 'Item already on the wishlist'}, 400
        
        like = LikedProduct(product=product, buyer=buyer)
        db.session.add(like)
        db.session.commit()

        return make_response(like.to_dict(), 200)
        # return {'success': 'Liked'}, 201
        
    def delete(self):
        like_id = request.get_json()['id']

        liked = LikedProduct.query.filter(LikedProduct.id == like_id).first()
        db.session.delete(liked)
        db.session.commit()

        return {'message': 'Succesfully deleted'}, 204
    
class ResetPassword(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get('email')
            
            if not email:
                return {'message': 'Please input your email address'}, 400
            
            user = User.query.filter_by(email=email).first()
            if user:
                token = user.generate_token()
                send_reset_password_email(email, token)
            return {'message': 'If an account with that email exists, a reset token has been sent.'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

def send_reset_password_email(email, token):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = 'Password Reset Request'

    body = f'''To reset your password, visit the following link:
    http://127.0.0.1:5555/change-password?token={token}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

class ReciveToken(Resource):
    def get(self, token):
        user = User.verify_token(token)
        if not user:
            return {"message": "Invalid token"}, 401
        return {"message": "Token is valid"}, 200

class ChangePassword(Resource):
    def post(self):
        try:
            data = request.get_json()
            new_password = data.get('new_password')  
            token = request.args.get('token')  # Extract token from query parameter

            if not token or not new_password:
                return {'message': 'Token and new password are required'}, 400

            user = User.verify_token(token)
            if not user:
                return {'message': 'Invalid token'}, 401

            user.password_hash = new_password
            db.session.commit()

            return {'message': 'Password has been changed successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500



class Hello(Resource):
    def get(self):
        hello = 'Hello World!'
        return make_response(
            hello,
            200
        )


api.add_resource(Transactions, '/transactions')
api.add_resource(Paybill, '/paybill') 
api.add_resource(STK, '/stk')
api.add_resource(UserIndex, '/user/<int:id>')
api.add_resource(OrderIndex, '/order/<int:id>')
api.add_resource(Users, '/users')
api.add_resource(ProductIndex, '/product/<int:id>')
api.add_resource(ShopIndex, '/shop/<int:id>')
api.add_resource(Products, '/products')
api.add_resource(SignUp, '/signup' )
api.add_resource(Login, '/login')
api.add_resource(Hello, '/hello')
api.add_resource(Images, '/images')
api.add_resource(Shops, '/shop')
api.add_resource(Orders, '/order')
api.add_resource(OrderItems, '/orderitems')
api.add_resource(Reviews, '/review')
api.add_resource(LikedProducts, '/like')
api.add_resource(DeleteUser, '/del_user/<int:user_id>')
api.add_resource(ResetPassword, '/reset-password')
api.add_resource(ReciveToken, '/reset-password/<token>')
api.add_resource(ChangePassword, '/change-password')
api.add_resource(Prompt, '/prompt')




if __name__ == '__main__':
    app.run(port=5555, debug=True)


