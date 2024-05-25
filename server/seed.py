from models import User, Shop, Product, Order, OrderItem, Review, ProductsImages, LikedProduct, Transaction
from config import app, db
import datetime


with app.app_context():
    print('Clearing database...')
    Transaction.query.delete()
    LikedProduct.query.delete()
    OrderItem.query.delete()
    Order.query.delete()
    Review.query.delete()
    ProductsImages.query.delete()
    db.session.commit()
    Product.query.delete()
    db.session.commit()
    Shop.query.delete()
    db.session.commit()
    User.query.delete()
    db.session.commit()

    
    print('Seeding user...')
    # sellers
    rob = User(username="robins", email="rob@gmail.com", location="Nairobi", contact="12345" ,role="seller")
    rob.password_hash = "seller"
    ndanu = User(username="ndanu", email="ndanu@gmail.com", location="Kisumu", contact="12345", role="seller")
    ndanu.password_hash = "seller2"
    john = User(username="john", email="john@gmail.com", location="Nakuru", contact="12345", role="seller")
    john.password_hash = "seller3"

    # buyers
    mike = User(username="michael", email="mikemumo333@gmail.com", location="Nairobi", contact="0700000000", role="buyer")
    mike.password_hash = "buyer"
    michelle = User(username="michelle", email="michelle@gmail.com", location="Kisumu", contact="0700000001", role="buyer")
    michelle.password_hash = "buyer2"
    james = User(username="james", email="james@gmail.com", location="Nakuru", contact="0700000002", role="buyer")
    james.password_hash = "buyer3"

    # devlivery
    vic = User(username="victor", email="victor@gmail.com", location="Nairobi", contact="0700000004", role="delivery", is_banda_delivery=True)
    vic.password_hash = "bolt"
    sam = User(username="boda", email="sam@gmail.com", location="Kisumu", contact="0700000005", role="delivery", is_banda_delivery=True)
    sam.password_hash = "bolt2"
    kevin = User(username="kevin", email="kevin@gmail.com", location="Nakuru", contact="0700000006", role="delivery", is_banda_delivery=True)
    kevin.password_hash = "bolt3"

    # admin
    kinsi = User(username="kinsi", email="kinsi@gmail.com", location="Nairobi", contact="0710101010", role="admin", is_banda_admin=True)
    kinsi.password_hash = "admin"
    
    # super admin
    super_admin = User(username="superadmin", email="superadmin@gmail.com", location="Nairobi", contact="0711111111", role="banda_admin", is_banda_admin=True)
    super_admin.password_hash = "superadmin"

    

    users = [rob, ndanu, john,
            mike, michelle, james, 
            vic, sam, kevin,
            kinsi, super_admin]
    db.session.add_all(users)
    db.session.commit()

    print('Seeding shop...')
    shop1 = Shop(name="Shoe Store", 
                 description="Sells high quality shoes", 
                 logo_image_url="https://i.pinimg.com/564x/c2/09/69/c20969c7c0e5b5c6f0f74d64395dadd4.jpg", 
                 banner_image_url="https://i.pinimg.com/564x/0d/8a/3a/0d8a3a79902c2460f0b163147293445c.jpg",
                 location="Nairobi",
                 contact="0700000000",
                 seller=rob)
    shop2 = Shop(name="Electronic Store", 
                 description="Good electronics", 
                 logo_image_url="https://i.pinimg.com/564x/43/ae/10/43ae10daf5a34ca7409a1abccc189e94.jpg", 
                 banner_image_url="https://i.pinimg.com/564x/33/11/5a/33115a1961b4b4415af899e8565b951e.jpg",
                 location="Kisumu",
                 contact="0700000001",
                 seller=ndanu)
    shop3 = Shop(name="foodies", 
                 description="sweet food", 
                 logo_image_url="https://i.pinimg.com/736x/c0/80/32/c08032a93c896fe253588ee9c0bb6f97.jpg", 
                 banner_image_url="https://i.pinimg.com/736x/c7/31/23/c7312307e19b84d78f914da20dfef7b1.jpg",
                 location="Nakuru",
                 contact="0700000002",
                 seller=john)
    shops = [shop1, shop2, shop3]
    db.session.add_all(shops)
    db.session.commit()

    print('Seeding products...')
    lamp = Product(name="lamp", description="Bright lamp to illuminate your working space.", price="300", quantity_available="1", category="Home decor", tag="hot", shop=shop1) 
    painting = Product(name="painting", description="Masterpiece by a young artist leaving his heart on the canvas.", price="10000", quantity_available="2", category="Home decor", tag="popular", shop=shop1)
    tv = Product(name="tv", description="60 inch with OLED display.", price="60000", quantity_available="3", category="Appliances", tag="new", shop=shop2)
    microwave = Product(name="microwave", description="10 power levels for all your heating needs.", price="7000", quantity_available="4", category="Appliances", tag="hot", shop=shop2)
    lawnmower = Product(name="lawnmower", description="3 power settings to cur all your grass in all terrain.", price="12000", quantity_available="5", category="Tools and Hardware", tag="popular", shop=shop3)
    hammer = Product(name="hammer", description="Stainless steel free of rust and study for all your household needs.", price="800", quantity_available="6", category="Tools and Hardware", tag="new", shop=shop3)
    dress = Product(name="dress", description="Flowing dresses to bring out your inner beauty.", price="2200", quantity_available="7", category="Clothing", tag="hot", shop=shop1)
    shoe = Product(name="shoe", description="White with laces.", price="1000", quantity_available="8", category="Clothing", tag="popular", shop=shop1)
    watch = Product(name="watch", description="Handmade and state of the art technology.", price="5000", quantity_available="9", category="Accessories", tag="new", shop=shop2)
    ring  = Product(name="ring", description="Diamond to show how much your love persists.", price="250", quantity_available="10", category="Accessories", tag="hot", shop=shop2)
    lipstick = Product(name="lipstick", description="Wear your courage boldly!", price="1000", quantity_available="11", category="Beauty and Skincare", tag="popular", shop=shop3)
    mascara = Product(name="mascara", description="They'll all stare.", price="1200", quantity_available="12", category="Beauty and Skincare", tag="new", shop=shop3)
    boots = Product(name="boots", description="Thick soles perfect for hiking.", price="1500", quantity_available="13", category="Outdoor Gear", tag="hot", shop=shop1)
    rope = Product(name="rope", description="For your clothes, your patches and outdoor activites.", price="350", quantity_available="14", category="Outdoor Gear", tag="popular", shop=shop1)
    phone = Product(name="phone", description="Clear display with storage upto 1TB.", price="98000", quantity_available="15", category="Electronics", tag="new", shop=shop1)
    laptop = Product(name="laptop", description="Running an M4 chip at speeds you never imagined.", price="40000", quantity_available="16", category="Electronics",tag="hot", shop=shop1)
    medicine = Product(name="medicine", description="Drink your cold away.", price="900", quantity_available="17", category="Health and Wellness", tag="popular", shop=shop2)
    bandage = Product(name="bandage", description="For the quick fix from the unfortunate accident.", price="1700", quantity_available="18", category="Health and Wellness", tag="new", shop=shop2)
    playstation = Product(name="playstation", description="Bring your imagination to life with immersive games and unlimited storage.", price="45000", quantity_available="19", category="Toys and Games", tag="hot", shop=shop3)
    monopoly = Product(name="monopoly", description="Learn your finances while beating your friends.", price="1000", quantity_available="20", category="Toys and Games", tag="popular", shop=shop3)
    book  = Product(name="book", description="Time to upskill your software skills using well descrbed examples.", price="910", quantity_available="21", category="Books and Stationary", tag="new", shop=shop1)
    potter = Product(name="potter", description="Follow Harry Potter through Hogwarts as he faces he who must not be mentioned.", price="1300", quantity_available="22", category="Books and Stationary", tag="hot", shop=shop1)
    burgers = Product(name="burgers", description="You've worked so hard. Feel the cheese drip down your lips.", price="750", quantity_available="23", category="Food and Beverages", tag="popular", shop=shop2)
    smoothie = Product(name="smoothie", description="Healthy drinks to get you through your day.", price="600", quantity_available="24", category="Food and Beverages", tag="new", shop=shop2)
    products = [lamp, painting, tv, microwave, lawnmower, hammer, dress, shoe, watch, ring, lipstick, mascara, boots, rope, phone, laptop, medicine, bandage, playstation, monopoly, book, potter, burgers, smoothie]
    db.session.add_all(products)
    db.session.commit()

    print("Seeding images...")
    lamp_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/23/9c/9a/239c9ae19bfe38378ccf36f2d3bff901.jpg", product=lamp)
    lamp_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/ef/3a/fd/ef3afd60fd6d329efa2114e8f7324177.jpg", product=lamp)
    painting_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/88/6c/2d/886c2dd9632df00ec675fdcf6d2fac92.jpg", product=painting)
    painting_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/03/a5/41/03a541999a8a071c3988c5ec66f5ffaf.jpg", product=painting)
    tv_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/19/de/fa/19defa028495d1c736e1664d3320c3d9.jpg", product=tv)
    tv_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/e1/de/02/e1de02f7da8004c15abef83490fa35e8.jpg", product=tv)
    microwave_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/7c/64/9a/7c649a0d09c4179a68c6f0a32b9284d3.jpg", product=microwave)
    microwave_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/b4/4b/27/b44b2773a08de3710cbd44a072b9029d.jpg", product=microwave)
    lawnmower_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/90/a8/d6/90a8d6f3555288eadae33f9de8c7fd25.jpg", product=lawnmower)
    lawnmower_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/30/42/30/3042304e5bcc7c33d3885f7c834eec64.jpg", product=lawnmower)
    hammer_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/79/39/ce/7939cec1d117cfa290636e0843d4085b.jpg", product=hammer)
    hammer_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/7d/d4/16/7dd4161cc3f81ad6621a8405e6889a1f.jpg", product=hammer)
    dress_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/43/30/43/43304353703693f1684dc6d2d3ac6d3b.jpg", product=dress)
    dress_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/a4/1a/71/a41a71cc235276c8fb09309c8c0ef57b.jpg", product=dress)
    shoe_image1 = ProductsImages(image_url="https://media.istockphoto.com/id/1417090656/photo/white-leather-sneaker.jpg?s=1024x1024&w=is&k=20&c=y5ER4LvqG_PNwF9s8DgPJdMwULhualEKRSpJCL1QXHA=", product=shoe)
    shoe_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/38/35/d7/3835d78455d62cfc7a3740963c3adaa6.jpg", product=shoe)
    watch_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/1a/d2/91/1ad291099701d4db295f7f2245b63eff.jpg", product=watch)
    watch_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/f8/0b/88/f80b88f9f381b420abf285c9731db135.jpg", product=watch)
    ring_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/52/2f/57/522f57c7668bb16f4364df4577f63867.jpg", product=ring)
    ring_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/79/27/92/792792386ecaa4c7be8c7c600bd0876c.jpg", product=ring)
    lipstick_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/54/3e/2a/543e2ab0d0df02f24ec311a8227647e3.jpg", product=lipstick)
    lipstick_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/a3/af/e1/a3afe1c2cb803c4911cb71d64d268b0d.jpg", product=lipstick)
    mascara_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/c6/81/56/c68156b7c29809beb6ad95c6d49176e4.jpg", product=mascara)
    mascara_image2 = ProductsImages(image_url="https://i.pinimg.com/474x/64/42/1d/64421decb6d49e74eab3883db9aab02d.jpg", product=mascara)
    boots_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/9c/d7/9d/9cd79d2c25582487798003720371b319.jpg", product=boots)
    boots_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/6c/13/69/6c1369cd17a054db642d8166d16959cc.jpg", product=boots)
    rope_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/67/d8/d6/67d8d65166f61ccfe0373aaffd40c44d.jpg", product=rope)
    rope_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/1a/87/b3/1a87b3ecb185d04b8b19e158e384c70c.jpg", product=rope)
    phone_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/d5/95/e4/d595e4530aaa0fcdf4ff8e7bc17f4d86.jpg", product=phone)
    phone_image2 = ProductsImages(image_url="https://i.pinimg.com/474x/95/ec/76/95ec76c86e850e4d92dde39053154718.jpg", product=phone)
    laptop_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/78/bf/a8/78bfa893270a0b531705b1c56f25674d.jpg", product=laptop)
    laptop_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/46/82/07/46820717c03eb4f359f46ea9caa1e1df.jpg", product=laptop)
    medicine_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/43/bb/22/43bb22a50aec7c9e67856ed4699ef33b.jpg", product=medicine)
    medicine_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/c0/a4/eb/c0a4ebf10e4972e9ae5fc434ffde5903.jpg", product=medicine)
    bandage_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/8e/34/c0/8e34c0cfcd6379ca80c9df19b84cffc0.jpg", product=bandage)
    bandage_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/8e/c0/09/8ec0099d50b7d6cd36c20fafd5d2128a.jpg", product=bandage)
    playstation_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/76/47/bd/7647bd8094eafac2b391351f6799098e.jpg", product=playstation)
    playstation_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/c1/75/ca/c175ca7fe7834248973f025a00945606.jpg", product=playstation)
    monopoly_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/40/a9/b0/40a9b0851b2bbf6d6000f6f0cd189065.jpg", product=monopoly)
    monopoly_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/6e/42/5c/6e425c90bed8d9ead384bc236abed6af.jpg", product=monopoly)
    book_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/b4/e3/51/b4e3510960b0d967e157e9494b08575d.jpg", product=book)
    book_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/69/9a/a6/699aa65083fe769632afa2efb9f0a47e.jpg", product=book)
    potter_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/03/73/1a/03731ae5faf3a20a3ec48390b32a7eeb.jpg", product=potter)
    potter_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/78/4e/63/784e63771eeca049c18436037b71cb42.jpg", product=potter)
    burgers_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/3c/1d/12/3c1d12d43ea6aeca59fd2321c4f15b8d.jpg", product=burgers)
    burgers_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/e2/5a/2e/e25a2e633611adc93e0340fd98241711.jpg", product=burgers)
    smoothie_image1 = ProductsImages(image_url="https://i.pinimg.com/236x/a1/53/36/a1533638301b09d54c4a6a48078e0c03.jpg", product=smoothie)
    smoothie_image2 = ProductsImages(image_url="https://i.pinimg.com/236x/7c/4c/40/7c4c40263b2ce90ca0f338be6bb6ae09.jpg", product=smoothie)
    images = [lamp_image1,lamp_image2, 
              painting_image1,painting_image2, 
              tv_image1, tv_image2, 
              microwave_image1, microwave_image2, 
              lawnmower_image1, lawnmower_image2, 
              hammer_image1, hammer_image2, 
              dress_image1, dress_image2, 
              shoe_image1, shoe_image2, 
              watch_image1, watch_image2, 
              ring_image1, ring_image2, 
              lipstick_image1, lipstick_image2, 
              mascara_image1, mascara_image2, 
              boots_image1, boots_image2, 
              rope_image1, rope_image2, 
              phone_image1, phone_image2, 
              laptop_image1, laptop_image2, 
              medicine_image1, medicine_image2, 
              bandage_image1, bandage_image2, 
              playstation_image1, playstation_image2, 
              monopoly_image1, monopoly_image2,   
              book_image1, book_image2, 
              potter_image1, potter_image2, 
              burgers_image1, burgers_image2, 
              smoothie_image1, smoothie_image2]
    db.session.add_all(images)
    db.session.commit()

    print("Seeding reviews...")
    lamp_review_1 = Review(content='The lighting is perfect for the bedside. Great customer service too.', rating=5, buyer=mike, seller=rob, product=lamp, date=str(datetime.datetime.now()))
    lamp_review_2 = Review(content='The actual product is nothing like the image shown. The buyer has also been frustrating on getting my refund.', rating=1, buyer=mike, seller=rob, product=lamp, date=str(datetime.datetime.now()))
    lamp_review_3 = Review(content='Meeh. Does the lighting, but it\'s not all that.', rating=3, buyer=mike, seller=rob, product=lamp, date=str(datetime.datetime.now()))
    laptop_review_1 = Review(content='Wonderful. I\'ve had it for 5 years and still works like brand new.', rating=5, buyer=mike, seller=rob, product=laptop, date=str(datetime.datetime.now()))
    laptop_review_2 = Review(content='I am still waiting for over a year now to get my laptop delivered after paying. Scammer!!!!!', rating=1, buyer=mike, seller=rob, product=laptop, date=str(datetime.datetime.now()))
    laptop_review_3 = Review(content='Great for the price. A bit laggy though.', rating=3, buyer=mike, seller=rob, product=laptop, date=str(datetime.datetime.now()))
    reviews = [lamp_review_1, lamp_review_2, lamp_review_3, laptop_review_1, laptop_review_2, laptop_review_3]
    db.session.add_all(reviews)
    db.session.commit()

    print("Seeding order...")
    order_1 = Order(total_price=1000, status='pending', delivery_fee=100, buyer=mike, delivery_person=vic)
    order_2 = Order(total_price=2000, status='pending', delivery_fee=350, buyer=michelle, delivery_person=sam)
    order_3 = Order(total_price=3000, status='pending', delivery_fee=700, buyer=james, delivery_person=kevin)
    orderz = [order_1, order_2, order_3]
    db.session.add_all(orderz)
    db.session.commit()

    print("Seeding order items...")
    lamp_order_1= OrderItem(quantity=1, order=order_1, product=lamp)
    painting_order_1= OrderItem(quantity=2, order=order_1, product=painting)
    tv_order_1= OrderItem(quantity=3, order=order_2, product=tv)
    laptop_order_1= OrderItem(quantity=4, order=order_3, product=laptop)
    playstation_order= OrderItem(quantity=2, order=order_2, product=playstation)
    orders = [lamp_order_1, painting_order_1, tv_order_1, laptop_order_1, playstation_order]
    db.session.add_all(orders)
    db.session.commit()

    print("Liking products...")
    like1 = LikedProduct(buyer=mike, product=lamp)
    like2 = LikedProduct(buyer=mike, product=painting)
    like3 = LikedProduct(buyer=mike, product=tv)
    like4 = LikedProduct(buyer=mike, product=laptop)
    likes = [like1, like2, like3, like4]
    db.session.add_all(likes)
    db.session.commit()
    
    
    
    # def create_super_admin():
    #     username = 'BandaAdmin'
    #     email = 'superadmin@gmail.com'
    #     password = 'superadmin@gmail.com'
        
    #     # Checking if the super admin already exists
    #     super_user = User.query.filter_by(email=email).first()
    #     if super_user:
    #         print('Super admin already exists.')
    #     else:
    #         # Creating the super admin if it doesn't exist
    #         super_admin = User(username=username, email=email, is_banda_admin=True)
    #         super_admin.password_hash = password
    #         db.session.add(super_admin)
    #         db.session.commit()
    #         print('Super admin created successfully.')
                # create_super_admin()

    
    
    
    
    
    
    

   