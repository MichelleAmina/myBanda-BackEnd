from faker import Faker
from models import User, Shop, Product, Order, OrderItem, Review
from config import app, db


fake = Faker()

# Function to generate fake data for users
def generate_users(num_users):
    users = []
    roles = ['seller/shop', 'client/customer', 'banda_admin', 'delivery']
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            role=fake.random_element(roles)
        )
        users.append(user)
    return users

# Function to generate fake data for shops
def generate_shops(users):
    shops = []
    for user in users:
        shop = Shop(
            name=fake.company(),
            description=fake.text(),
            logo_image_url=fake.image_url(),
            banner_image_url=fake.image_url(),
            seller=user
        )
        shops.append(shop)
    return shops

# Function to generate fake data for products
def generate_products(users, shops, num_products_per_shop):
    products = []
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Toys']
    for shop in shops:
        for _ in range(num_products_per_shop):
            seller = fake.random_element(users)
            product = Product(
                name=fake.product_name(),
                description=fake.text(),
                price=fake.random_number(digits=3),
                image_url=fake.image_url(),
                quantity_available=fake.random_number(digits=2),
                category=fake.random_element(categories),
                seller=seller,
                shop=shop
            )
            products.append(product)
    return products

# Function to generate fake data for orders
def generate_orders(users, num_orders):
    orders = []
    statuses = ['pending', 'shipped', 'delivered']
    for _ in range(num_orders):
        user = fake.random_element(users)
        order = Order(
            user=user,
            total_price=fake.random_number(digits=4),
            status=fake.random_element(statuses),
            delivery_address=fake.address()
        )
        orders.append(order)
    return orders

# Function to generate fake data for order items
def generate_order_items(products, orders):
    order_items = []
    for order in orders:
        num_items = fake.random_number(digits=1)
        order_products = fake.random_elements(products, length=num_items, unique=True)
        for product in order_products:
            order_item = OrderItem(
                quantity=fake.random_number(digits=1),
                order=order,
                product=product
            )
            order_items.append(order_item)
    return order_items

# Function to generate fake data for reviews
def generate_reviews(users, products, num_reviews_per_product):
    reviews = []
    for product in products:
        for _ in range(num_reviews_per_product):
            buyer = fake.random_element(users)
            seller = product.seller
            review = Review(
                content=fake.text(),
                buyer=buyer,
                seller=seller,
                product=product
            )
            reviews.append(review)
    return reviews

# Function to seed the database with fake data
def seed_database(num_users, num_shops, num_products_per_shop, num_orders, num_reviews_per_product):
    users = generate_users(num_users)
    db.session.add_all(users)
    db.session.commit()

    shops = generate_shops(users[:num_shops])
    db.session.add_all(shops)
    db.session.commit()

    products = generate_products(users, shops, num_products_per_shop)
    db.session.add_all(products)
    db.session.commit()

    orders = generate_orders(users, num_orders)
    db.session.add_all(orders)
    db.session.commit()

    order_items = generate_order_items(products, orders)
    db.session.add_all(order_items)
    db.session.commit()

    reviews = generate_reviews(users, products, num_reviews_per_product)
    db.session.add_all(reviews)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_database(
            num_users=10,
            num_shops=5,
            num_products_per_shop=10,
            num_orders=20,
            num_reviews_per_product=3
        )
