from config import db, SQLAlchemy, validates, SerializerMixin, hybrid_property, bcrypt, datetime, timezone, timedelta, Serializer, app, SECRET_KEY
from itsdangerous import URLSafeSerializer
import jwt
<<<<<<< HEAD
=======


>>>>>>> robins

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password_hash = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(250), nullable=True)
    contact = db.Column(db.String(50), nullable=True)
<<<<<<< HEAD
    role = db.Column(db.String, nullable=False, default=False)   # 'seller/shop', 'client/customer', 'banda_admin', 'delivery'
=======
    role = db.Column(db.String, nullable=False, default=False)  # 'seller/shop', 'client/customer', 'banda_admin', 'delivery'


    ## Getting the token for reset password route


    def generate_token(self, expires_in=1800):
        exp = datetime.utcnow() + timedelta(seconds=expires_in)
        payload = {
            'user_id': self.id,
            'exp': exp
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            if not user_id:
                raise jwt.InvalidTokenError("User ID not found in token")
            return User.query.get(user_id)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


    

    def __repr__(self):
        return f'<User {self.email} of role {self.role}>'
>>>>>>> robins

    # Additional fields for Banda Admin and Delivery. Preset to false until registration / login
    is_banda_admin = db.Column(db.Boolean, default=False)
    is_banda_delivery = db.Column(db.Boolean, default=False)

    # Relationships for reviews
    reviews_given = db.relationship('Review', back_populates='buyer', foreign_keys='Review.buyer_id', lazy='select')
    reviews_received = db.relationship('Review', back_populates='seller', foreign_keys='Review.seller_id', lazy='select')

    # Order relationships
    my_orders = db.relationship("Order", back_populates='buyer', foreign_keys='Order.buyers_id', lazy='select')
    my_deliveries = db.relationship("Order", back_populates='delivery_person', foreign_keys='Order.delivery_id', lazy='select')

    # One to one relationship with shop
    shop = db.relationship('Shop', back_populates='seller', uselist=False, cascade="all, delete-orphan", lazy='select')

    #Likedproduct relatioship
    liked_products = db.relationship('LikedProduct', back_populates='buyer', cascade='all, delete-orphan')

    #Followed shops relationship
    followed_shops = db.relationship('FollowedShop', back_populates='buyer', cascade='all, delete-orphan')

    serialize_rules = ('-_password_hash', '-reviews_given.buyer', '-reviews_received.seller', '-my_orders.buyer', '-my_deliveries.delivery_person', '-shop.seller', '-liked_products.buyer', '-followed_shops.buyer')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Cannot view password')

    @password_hash.setter
    def password_hash(self, password):
        hashed_password = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = hashed_password.decode('utf-8')
        
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    
    def generate_token(self, expires_in=1800):
            exp = datetime.utcnow() + timedelta(seconds=expires_in)
            payload = {
                'user_id': self.id,
                'exp': exp
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return token

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            if not user_id:
                raise jwt.InvalidTokenError("User ID not found in token")
            return User.query.get(user_id)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


    def __repr__(self):
        return f'<User {self.email} of role {self.role}>'


class Shop(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    logo_image_url = db.Column(db.String, nullable=False)
    banner_image_url = db.Column(db.String, nullable=False)
    location = db.Column(db.String(250), nullable=True)
    contact = db.Column(db.String(50), nullable=True)

    # A shop belongs to a seller 
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller = db.relationship('User', back_populates='shop')

    # A shop can have many products 
    products = db.relationship('Product', back_populates='shop', lazy='select', cascade="all, delete-orphan")

    #People who follow the shop
    followers = db.relationship('FollowedShop', back_populates='shop', lazy='select', cascade="all, delete-orphan")

    serialize_rules = ('-products.shop', '-seller.reviews_received', '-seller.shop')

    def __repr__(self):
        return f'<Shop {self.name} owned by {self.seller_id}>'


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String, nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    tag = db.Column(db.String) #hot, popular, new

    # Relationships
    shop = db.relationship('Shop', back_populates='products')
    items = db.relationship('OrderItem', back_populates='product', lazy='select', cascade="all, delete-orphan")
    likes = db.relationship('LikedProduct', back_populates='product', lazy='select', cascade="all, delete-orphan")
    images = db.relationship('ProductsImages', back_populates='product', lazy='select', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='product', lazy='select', cascade="all, delete-orphan")

    serialize_rules = ('-shop.products', '-items', '-images.product', '-reviews.product', '-likes.product', 'reviews.buyer.liked_products')

    def __repr__(self):
        return f'<Product {self.name} from shop {self.shop_id}>'


class ProductsImages(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='images')

    serialize_rules = ('-product.images',)


class OrderItem(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship("Order", back_populates='order_items')

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship("Product", back_populates='items')

    serialize_rules = ('-order.order_items','-product.items')

    def __repr__(self):
        return f'<OrderItem {self.id}>'


class Order(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False, default="pending")  #'pending', 'assigned', 'dispatched', 'delivered'
    delivery_fee = db.Column(db.String)
    delivery_address = db.Column(db.String)
    contact = db.Column(db.String(100))
    name = db.Column(db.String(100))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    delivery_persons = db.Column(db.String(100))
<<<<<<< HEAD
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
=======
>>>>>>> robins
    
    buyers_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    buyer = db.relationship('User', back_populates='my_orders', foreign_keys=[buyers_id], lazy='joined')

    delivery_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    delivery_person = db.relationship('User', back_populates='my_deliveries', foreign_keys=[delivery_id], lazy='joined')

    order_items = db.relationship('OrderItem', back_populates='order', lazy='select', cascade="all, delete-orphan")

    serialize_rules = ('-order_items.order', '-order_items.product.reviews','-buyer.my_orders','-buyer.reviews_given', '-delivery_person.my_deliveries')


    def __repr__(self):
        return f'<Order {self.id}>'
    
    
class LikedProduct(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    buyers_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    buyer = db.relationship('User', back_populates='liked_products')

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship("Product", back_populates='likes')

    serialize_rules = ('-buyer.liked_products', '-buyer.shop','-buyer.my_orders', '-buyer.my_deliveries', '-buyer.reviews_given', '-buyer.reviews_received', '-product.likes', '-product.shop.seller', '-product.reviews', '-product.items')

    def __repr__(self):
        return f'<LikedProduct {self.id}>'

class FollowedShop(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    buyers_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    buyer = db.relationship('User', back_populates='followed_shops')

    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    shop = db.relationship("Shop", back_populates='followers')

    serialize_rules = ('-buyer.followed_shops', '-shop.followers', '-buyer.reviews_given', '-buyer.reviews_received')

    def __repr__(self):
        return f'<FollwedShop {self.id}>'


class Review(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    date = db.Column(db.String)

    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer = db.relationship('User', back_populates='reviews_given', foreign_keys=[buyer_id], lazy='joined')

    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller = db.relationship('User', back_populates='reviews_received', foreign_keys=[seller_id], lazy='joined')

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='reviews', lazy='joined')
    
    serialize_rules = ('-buyer.reviews_given','-buyer.my_orders', '-seller','-product.reviews')

    def __repr__(self):
        return f'<Review by {self.buyer_id} for {self.seller_id}\'s product {self.product_id}>'
    
    
class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    MpesaReceiptNumber = db.Column(db.String)
    Amount = db.Column(db.String)
    TransactionDate = db.Column(db.String)
    PhoneNumber = db.Column(db.String)


