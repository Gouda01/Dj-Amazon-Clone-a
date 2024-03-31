import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from faker import Faker
import random
from django.contrib.auth.models import User

from products.models import Product, Brand, Review, ProductImages

images = ['01.jpg','02.jpg','03.jpg','04.jpg','05.jpg','06.jpg','07.jpg','08.jpg','09.jpg','10.jpg']

def seed_brand (n):
    fake = Faker()

    for _ in range(n):
        Brand.objects.create (
            name = fake.name(),
            image = f"brand/{images[random.randint(0,9)]}"
        )
    print(f"{n} Brands was added successfuly")


def seed_products(n):
    fake = Faker()
    flag_types = ['New','Sale','Feature']
    brands = Brand.objects.all()

    for _ in range(n):
        Product.objects.create (
            name = fake.name(),
            flag = flag_types[random.randint(0,2)],
            price = round(random.uniform(20.99,99.99),2),
            image = f"product/{images[random.randint(0,9)]}",
            sku = random.randint(100,1000000),
            subtitle = fake.text(max_nb_chars=450),
            description = fake.text(max_nb_chars=4000),
            brand = brands[random.randint(0,len(brands)-1)],
            
        )
    print(f"{n} Products was added successfuly")


def seed_reviews(n):
    fake = Faker()
    users = User.objects.all()
    products = Product.objects.all()

    for _ in range(n):
        Review.objects.create (
            user = users[random.randint(0,len(users)-1)],
            product = products[random.randint(0,len(products)-1)],
            review = fake.text(max_nb_chars=200),
            rate = random.randint(1,5)
        )
    print(f"{n} Reviews was added successfuly")


def seed_product_images (n):
    fake = Faker()
    products = Product.objects.all()

    for _ in range(n):
        ProductImages.objects.create (
            product = products[random.randint(0,len(products)-1)],
            image = f"product_image/{images[random.randint(0,9)]}"
        )
    print(f"{n} Product images was added successfuly")


# seed_brand(200)
# seed_products(2000)
# seed_reviews(5000)
seed_product_images(5000)