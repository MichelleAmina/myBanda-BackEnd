from models import User, Product, ProductsImages, Shop, Order, Review, OrderItem, Transaction, LikedProduct, Specification
# from seed import seed_database
from config import app, db, Flask, request, jsonify, Resource, api, make_response, JWTManager, create_access_token, jwt_required, session,datetime, timezone, timedelta, mpesa_api, mail, Message, url_for, sender_email, sender_password, photos, reqparse, os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import cross_origin
# from flask_uploads import UploadNotAllowed
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename




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

            return {'message': 'User created successfully', 'user': user.to_dict()}, 201
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
            return {'message': 'Login successful', 'access_token': access_token, 'role': user.role, 'isNewSeller': user.is_new_seller}, 200
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
        specs = data.get('specs')


        product = Product(name=name, description=description, price=price, quantity_available=quantity_available, category=category, shop_id=shop_id, tag=tag) 
        db.session.add(product)
        db.session.commit()
        image = ProductsImages(image_url=image_url, product=product)
        db.session.add(image)
        db.session.commit()
        for spec in specs:
            specification = Specification(spec=spec, product=product)
            db.session.add(specification)
            db.session.commit()

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
 



class CreateProduct(Resource):
    @jwt_required()
    def post(self):
        seller_id = get_jwt_identity()

        # Retrieve shop for the seller
        shop = Shop.query.filter_by(seller_id=seller_id).first()
        if not shop:
            return {'error': 'No shop found for the seller'}, 404

        data = request.form

        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        quantity_available = data.get('quantity_available')
        category = data.get('category')
        tag = data.get('tag')

        if not all([name, description, price, quantity_available, category]):
            return {'error': 'Missing required fields'}, 400

        product = Product(
            name=name,
            description=description,
            price=float(price),
            quantity_available=int(quantity_available),
            category=category,
            tag=tag,
            shop_id=shop.id
        )

        db.session.add(product)
        db.session.commit()

        # Handling image upload
        if 'images' not in request.files:
            return {'error': 'No images uploaded'}, 400

        files = request.files.getlist('images')

        for file in files:
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
                file.save(file_path)
                image_url = photos.url(filename)

                product_image = ProductsImages(image_url=image_url, product_id=product.id)
                db.session.add(product_image)

        db.session.commit()

        return {'message': 'Product created and images uploaded successfully', 'product_id': product.id}, 201

    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





class ShopResource(Resource):
    @jwt_required()
    def post(self):
        seller_id = get_jwt_identity()

        # Checking if the user already has a shop
        existing_shop = Shop.query.filter_by(seller_id=seller_id).first()
        if existing_shop:
            # Updating existing shop details if it already exists
            return self.update_shop(existing_shop)

        # Creating a new shop if the user doesn't have one
        return self.create_shop(seller_id)

    def create_shop(self, seller_id):
        data = request.form

        name = data.get('name')
        description = data.get('description')
        location = data.get('location')
        contact = data.get('contact')

        # print(f"Name: {name}")
        # print(f"Description: {description}")
        # print(f"Location: {location}")
        # print(f"Contact: {contact}")

        if not all([name, description, location, contact]):
            return {'error': 'Missing required fields'}, 400

        # Handling logo image upload
        if 'logo_image' not in request.files:
            return {'error': 'No logo image uploaded'}, 400

        logo_file = request.files['logo_image']
        if not logo_file or not self.allowed_file(logo_file.filename):
            return {'error': 'Invalid logo image file'}, 400

        logo_filename = secure_filename(logo_file.filename)
        logo_file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], logo_filename)
        logo_file.save(logo_file_path)
        logo_image_url = photos.url(logo_filename)

        # Handling banner image upload
        if 'banner_image' not in request.files:
            return {'error': 'No banner image uploaded'}, 400

        banner_file = request.files['banner_image']
        if not banner_file or not self.allowed_file(banner_file.filename):
            return {'error': 'Invalid banner image file'}, 400

        banner_filename = secure_filename(banner_file.filename)
        banner_file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], banner_filename)
        banner_file.save(banner_file_path)
        banner_image_url = photos.url(banner_filename)

        shop = Shop(
            name=name,
            description=description,
            location=location,
            contact=contact,
            logo_image_url=logo_image_url,
            banner_image_url=banner_image_url,
            seller_id=seller_id
        )

        db.session.add(shop)
        db.session.commit()

        return {'message': 'Shop created successfully', 'shop_id': shop.id}, 201

    def update_shop(self, shop):
        data = request.form

        name = data.get('name')
        description = data.get('description')
        location = data.get('location')
        contact = data.get('contact')

        # Updating the shop details if provided
        if name:
            shop.name = name
        if description:
            shop.description = description
        if location:
            shop.location = location
        if contact:
            shop.contact = contact

        # Handling logo image upload if provided
        if 'logo_image' in request.files:
            logo_file = request.files['logo_image']
            if logo_file and self.allowed_file(logo_file.filename):
                logo_filename = secure_filename(logo_file.filename)
                logo_file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], logo_filename)
                logo_file.save(logo_file_path)
                logo_image_url = photos.url(logo_filename)
                shop.logo_image_url = logo_image_url

        # Handling banner image upload if provided
        if 'banner_image' in request.files:
            banner_file = request.files['banner_image']
            if banner_file and self.allowed_file(banner_file.filename):
                banner_filename = secure_filename(banner_file.filename)
                banner_file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], banner_filename)
                banner_file.save(banner_file_path)
                banner_image_url = photos.url(banner_filename)
                shop.banner_image_url = banner_image_url

        db.session.commit()

        return {'message': 'Shop updated successfully'}, 200

    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




  
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

            seller = User.query.filter(User.id == seller_id).first()
            seller.is_new_seller = False
            db.session.commit()

            return make_response(
                shop.to_dict(),
                200
            )
        
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
        
        
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
            user_id_posted = data.get('user_id')
            delivery_fee = data.get('delivery_fee')
            delivery_address = data.get('delivery_address')
            contact = data.get('contact')
            name = data.get('name')
            country = data.get('country')
            city = data.get('city')
            delivery_id = data.get('delivery_persons')
            created_at = datetime.now(timezone.utc)

            # if None in [total_price, status, delivery_fee, delivery_address]:
            #     return {'message': 'Required field(s) missing'}, 400

            # Getting the current time
            

            order = Order(buyers_id=user_id, total_price=total_price, status=status, delivery_fee=delivery_fee, delivery_address=delivery_address, created_at=created_at, contact=contact, name=name, country=country, city=city, delivery_id=delivery_id)
            db.session.add(order)
            db.session.commit()


            for item in data['items']:
                orderitem = OrderItem(order_id=order.id, product_id=item['id'], quantity=item['quantity'])
                db.session.add(orderitem)
                db.session.commit()

            if data['mpesa_contact']:
                
                number = data['mpesa_contact']
                amount = data['total_price']

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
                # return resp,200


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
            specification = data.get('specification')

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

            order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity, specification=specification)
            db.session.add(order_item)
            db.session.commit()

            return make_response(order_item.to_dict(), 201)
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
        # print(f"Received ID: {id}")  
        try:
            user_id = get_jwt_identity()
            # print(f"User ID from JWT: {user_id}") 

            # print(f"User ID from JWT: {user_id}") 

            if not user_id:
                return {'message': 'User not logged in'}, 401

            data = request.get_json()
            new_status = data.get('status')
            # print(f"New status from request: {new_status}") 

            # if not new_status:
            #     return {'message': 'New status not provided'}, 400

            print(f"Querying order with ID: {id} and buyers_id: {user_id}")  
            order = Order.query.filter_by(id=order_id).first()
            # print(f"Found order: {order}") 
            if not order:
                return {'message': 'Order not found'}, 404

            order.status = new_status
            db.session.commit()
            # print(f"Order status updated to: {order.status}")  

            return make_response(order.to_dict(), 200)
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500


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
            rating = data.get('rating') # 1 to 5
            buyer_id = user_id  # the logged-in user is the buyer
            product_id = data.get('product_id')
            seller_id = Product.query.filter(Product.id == product_id).first().to_dict()['shop']['seller_id']
            print("this is the seller id:", seller_id)

            date = datetime.now(timezone.utc)


            if None in [content, rating, seller_id, product_id]:
                return {'message': 'Required field(s) missing'}, 400

            # Checking if the seller and product exist before adding them
            seller = User.query.get(seller_id)
            product = Product.query.get(product_id)
            buyer = User.query.get(buyer_id)
            if not seller or not product:
                return {'message': 'Seller or product does not exist'}, 404

            review = Review(content=content, rating=rating, buyer=buyer, seller=seller, product=product, date=date)
            db.session.add(review)
            db.session.commit()

            return make_response(review.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return {"message": str(e)}, 500
        

class Prompt(Resource):
    def post(self):
        number = request.get_json()['contact']
        amount = request.get_json()['amount']

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
            return {"message": "No liked products"}, 404
        
        return make_response(
            liked,
            200
        )
    
    @jwt_required()
    def post(self):
        data = request.get_json()

        product_id = data["product_id"]
        buyers_id = get_jwt_identity()


        if None in [buyers_id, product_id]:
                return {'message': 'Required field(s) missing'}, 400
        
        # Checking if the product exists
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product does not exist'}, 404
        
        buyer = User.query.get(buyers_id)
        if not buyer:
            return {'message': 'Buyer does not exist'}, 404
        
        exists = LikedProduct.query.filter(LikedProduct.buyers_id == buyers_id, LikedProduct.product_id == product_id).first()
        if exists:
            return {'message': 'Product already liked'}, 400
        
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
api.add_resource(OrderIndex, '/order/<int:order_id>')
api.add_resource(Reviews, '/review')
api.add_resource(LikedProducts, '/like')
api.add_resource(DeleteUser, '/del_user/<int:user_id>')
api.add_resource(ResetPassword, '/reset-password')
api.add_resource(ReciveToken, '/reset-password/<token>')
api.add_resource(ChangePassword, '/change-password')
api.add_resource(CreateProduct, '/upload_image/product')
api.add_resource(ShopResource, '/shop/uploads/images')
# api.add_resource(Admin, '/admin/users')
# api.add_resource(UserDetailsAdmin, '/admin/users/<int:user_id>')





if __name__ == '__main__':
    # create_super_admin()
    app.run(port=5555, debug=True)
