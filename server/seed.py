from models import User, Shop, Product, Order, OrderItem, Review, ProductsImages
from config import app, db


with app.app_context():
    print('Clearing database...')
    User.query.delete()
    Shop.query.delete()
    Product.query.delete()
    ProductsImages.query.delete()
    db.session.commit()

    print('Seeding user...')
    rob = User(username="robbins", email="rob@gmail.com", location="", contact="" ,role="seller")
    rob.password_hash = "strong"
    db.session.add(rob)

    print('Seeding shop...')
    shop1 = Shop(name="Shoe Store", description="Sells high quality shoes", logo_image_url="https://i.pinimg.com/736x/29/df/c6/29dfc6f05b80804c18913851a79c5140.jpg", banner_image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPXVdWLD9aHeFLG5UWdmM8XdkNgr_ZENfeFIh7Tv-ZkKMJgiz1hAi5OUj9gQbPlprtBGw&usqp=CAU", seller_id="1")
    db.session.add(shop1)

    print('Seeding products...')
    lamp = Product(name="lamp", description="Brigt lamp to illuminate your working space.", price="300", quantity_available="1", category="Home decor", shop_id="1") 
    painting = Product(name="painting", description="Masterpiece by a young artist leaving his heart on the canvas.", price="10000", quantity_available="2", category="Home decor", shop_id="1")
    tv = Product(name="tv", description="60 inch with OLED display.", price="60000", quantity_available="3", category="Appliances", shop_id="1")
    microwave = Product(name="microwave", description="10 power levels for all your heating needs.", price="7000", quantity_available="4", category="Appliances", shop_id="1")
    lawnmower = Product(name="lawnmower", description="3 power settings to cur all your grass in all terrain.", price="12000", quantity_available="5", category="Tools and Hardware", shop_id="1")
    hammer = Product(name="hammer", description="Stainless steel free of rust and study for all your household needs.", price="800", quantity_available="6", category="Tools and Hardware", shop_id="1")
    dress = Product(name="dress", description="Flowing dresses to bring out your inner beauty.", price="2200", quantity_available="7", category="Clothing", shop_id="1")
    shoe = Product(name="shoe", description="White with laces.", price="1000", quantity_available="8", category="Clothing", shop_id="1")
    watch = Product(name="watch", description="Handmade and state of the art technology.", price="5000", quantity_available="9", category="Accessories", shop_id="1")
    ring  = Product(name="ring", description="Diamond to show how much your love persists.", price="250", quantity_available="10", category="Accessories", shop_id="1")
    lipstick = Product(name="lipstick", description="Wear your courage boldly!", price="1000", quantity_available="11", category="Beauty and Skincare", shop_id="1")
    mascara = Product(name="mascara", description="They'll all stare.", price="1200", quantity_available="12", category="Beauty and Skincare", shop_id="1")
    boots = Product(name="boots", description="Thick soles perfect for hiking.", price="1500", quantity_available="13", category="Outdoor Gear", shop_id="1")
    rope = Product(name="rope", description="For your clothes, your patches and outdoor activites.", price="350", quantity_available="14", category="Outdoor Gear", shop_id="1")
    phone = Product(name="phone", description="Clear display with storage upto 1TB.", price="98000", quantity_available="15", category="Electronics", shop_id="1")
    laptop = Product(name="laptop", description="Running an M4 chip at speeds you never imagined.", price="40000", quantity_available="16", category="Electronics", shop_id="1")
    medicine = Product(name="medicine", description="Drink your cold away.", price="900", quantity_available="17", category="Health and Wellness", shop_id="1")
    bandage = Product(name="bandage", description="For the quick fix from the unfortunate accident.", price="1700", quantity_available="18", category="Health and Wellness", shop_id="1")
    playstation = Product(name="playstation", description="Bring your imagination to life with immersive games and unlimited storage.", price="45000", quantity_available="19", category="Toys and Games", shop_id="1")
    monopoly = Product(name="monopoly", description="Learn your finances while beating your friends.", price="1000", quantity_available="20", category="Toys and Games", shop_id="1")
    book  = Product(name="book", description="Time to upskill your software skills using well descrbed examples.", price="910", quantity_available="21", category="Books and Stationary", shop_id="1")
    potter = Product(name="potter", description="Follow Harry Potter through Hogwarts as he faces he who must not be mentioned.", price="1300", quantity_available="22", category="Books and Stationary", shop_id="1")
    burgers = Product(name="burgers", description="You've worked so hard. Feel the cheese drip down your lips.", price="750", quantity_available="23", category="Food and Beverages", shop_id="1")
    smoothie = Product(name="smoothie", description="Healthy drinks to get you through your day.", price="600", quantity_available="24", category="Food and Beverages", shop_id="1")
    products = [lamp, painting, tv, microwave, lawnmower, hammer, dress, shoe, watch, ring, lipstick, mascara, boots, rope, phone, laptop, medicine, bandage, playstation, monopoly, book, potter, burgers, smoothie]
    db.session.add_all(products)

    print("Seeding images...")
    shoe_image = ProductsImages(image_url="https://media.istockphoto.com/id/1417090656/photo/white-leather-sneaker.jpg?s=1024x1024&w=is&k=20&c=y5ER4LvqG_PNwF9s8DgPJdMwULhualEKRSpJCL1QXHA=", product_id="8")
    db.session.add(shoe_image)

    db.session.commit()
