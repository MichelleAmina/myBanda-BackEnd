from models import User, Shop, Product, Order, OrderItem, Review, ProductsImages
from config import app, db

def delete_all():
    with app.app_context():

        users = User.query.all()
        shops = Shop.query.all()
        products = Product.query.all()
        images = ProductsImages.query.all()

        for user in users:
            db.session.delete(user)

        for shop in shops:
            db.session.delete(shop)

        for product in products:
            db.session.delete(product)

        for image in images:
            db.session.delete(image)

        print('Clearing database...')
        ProductsImages.query.delete()
        db.session.commit()
        Product.query.delete()
        db.session.commit()
        Shop.query.delete()
        db.session.commit()
        User.query.delete()
        db.session.commit()

if __name__ == "__main__":
    delete_all()