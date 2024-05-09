from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


db= SQLAlchemy()

# User class with details obtained on registration 
class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String, nullable=False)  # 'seller/shop', 'client/customer', 'banda_admin', 'delivery'

    # Additional fields for Banda Admin and Delivery
    # Preset to false until registration / login
    is_banda_admin = db.Column(db.Boolean, default=False)
    is_banda_delivery = db.Column(db.Boolean, default=False)

    # Relationship for shop
    # A user, specifically a seller will have a shop 
    shop = db.relationship('Shop', backref='owner', uselist=False, cascade="all, delete-orphan", lazy=True)

    # Relationships for reviews
    reviews_given = db.relationship('Review', backref='buyer', foreign_keys='Review.buyer_id', lazy=True)
    reviews_received = db.relationship('Review', backref='seller', foreign_keys='Review.seller_id', lazy=True)



    def __repr__(self):
        return f'<User {self.email} of role {self.role}>'


# When a seller is setting up their "shop", these are the input details that they'll post and will be stored in the b
# Need to decide on whether we'll be using a banner or an image 
class Shop(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    logo_image_url = db.Column(db.String, nullable=False)
    banner_image_url = db.Column(db.String, nullable=False)

    # A shop belongs to a seller 
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # A shop can have many products 
    products = db.relationship('Product', backref='shop', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Shop {self.name} owned by {self.seller_id}>'


# Table for products 
class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    # Add this column for product category
    category = db.Column(db.String, nullable=False) 

    # Additiona columns to know seller of products as well as shop associated with product
    # The shop belongs to the seller 
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)

    orders = db.relationship('OrderItem', backref='product', lazy=True, cascade="all, delete-orphan")

    # Relationship for reviews
    reviews = db.relationship('Review', backref='product', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Product {self.name} from shop {self.shop_id}>'


# Table for orders placed 
class Order(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)  # e.g., 'pending', 'shipped', 'delivered'

    # Additional field for delivery information, such as address
    delivery_address = db.Column(db.String, nullable=False)

    # Other additional fields??

    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Order {self.id}>'


# Association table between the orders and products 
class OrderItem(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.id}>'


# Review table 
class Review(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<Review by {self.buyer_id} for {self.seller_id}\'s product {self.product_id}>'