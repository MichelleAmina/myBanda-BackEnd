from config import db, SQLAlchemy, validates, SerializerMixin, hybrid_property, bcrypt, datetime, timezone, timedelta


# User class with details obtained on registration 
class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password_hash = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(250), nullable=True )
    contact = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String, nullable=False)  # 'seller/shop', 'client/customer', 'banda_admin', 'delivery'

    # Additional fields for Banda Admin and Delivery
    # Preset to false until registration / login
    is_banda_admin = db.Column(db.Boolean, default=False)
    is_banda_delivery = db.Column(db.Boolean, default=False)

    # Relationship for shop
    # A user, specifically a seller will have a shop 
    shop = db.relationship('Shop', back_populates='seller', uselist=False, cascade="all, delete-orphan", lazy=True)

    # Relationships for reviews
    reviews_given = db.relationship('Review', backref='buyer', foreign_keys='Review.buyer_id', lazy=True)
    reviews_received = db.relationship('Review', backref='seller', foreign_keys='Review.seller_id', lazy=True)

    order = db.relationship("Order", back_populates='user')
    
    serialize_rules = ('-reviews_given.buyer', '-reviews_received.seller', '-_password_hash','-order.user')


    @hybrid_property
    def password_hash(self):
        raise Exception('Cannot view password')

    @password_hash.setter
    def password_hash(self, password):
        hashed_password = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = hashed_password.decode('utf-8')
        
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))


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
    seller = db.relationship('User', back_populates='shop')


    # A shop can have many products 
    products = db.relationship('Product', back_populates='shop', lazy=True, cascade="all, delete-orphan")
    serialize_rules = ('-products.shop', '-seller.shop')

    def __repr__(self):
        return f'<Shop {self.name} owned by {self.seller_id}>'


# Table for products 
class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    # image_url = db.Column(db.String, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    # Add this column for product category
    category = db.Column(db.String, nullable=False) 

    # Additiona columns to know seller of products as well as shop associated with product
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    shop = db.relationship('Shop', back_populates='products')

    orders = db.relationship('OrderItem', backref='product', lazy=True, cascade="all, delete-orphan")

    images = db.relationship('ProductsImages', back_populates='product', cascade="all, delete-orphan")
    serialize_rules = ('-images.product', '-shop.products', '-reviews.product')

    # Relationship for reviews
    reviews = db.relationship('Review', backref='product', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Product {self.name} from shop {self.shop_id}>'
    
class ProductsImages(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    product = db.relationship('Product', back_populates='images')


# Table for orders placed 
class Order(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)  # e.g., 'pending', 'assigned', 'dispatched', 'delivered'
    delivery_fee = db.Column(db.String)
    delivery_person = db.Column(db.Integer)
    
    # Additional field for delivery information, such as address
    delivery_address = db.Column(db.String, nullable=False)
    
    # Other additional fields??
    

    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    user = delivery = db.relationship('User', back_populates='order')

    serialize_rules = ('-order_items.order', '-user.order')

    #function to get current date and time
    def get_current_time():
        return datetime.now(timezone.utc)
    
    # Timestamp for order creation
    created_at = db.Column(db.DateTime, default=get_current_time, nullable=False)

    
    def __repr__(self):
        return f'<Order {self.id}>'


# Association table between the orders and products 
class OrderItem(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    serialize_rules = ('-order.order_items', '-product.orders')

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<OrderItem {self.id}>'


# Review table 
class Review(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    date = db.Column(db.String)

    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    serialize_rules = ('-buyer.reviews_given', '-seller.reviews_received', '-product.reviews')

    def __repr__(self):
        return f'<Review by {self.buyer_id} for {self.seller_id}\'s product {self.product_id}>'

