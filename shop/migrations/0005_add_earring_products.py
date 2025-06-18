from django.db import migrations
from decimal import Decimal

def create_earring_products(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Product = apps.get_model('shop', 'Product')
    
    earrings_category = Category.objects.get(slug='earrings')
    
    # Sample earring products
    products = [
        {
            'name': 'Classic Pearl Studs',
            'slug': 'classic-pearl-studs',
            'description': 'Timeless elegance with these classic pearl stud earrings. Perfect for everyday wear or special occasions.',
            'price': Decimal('2999.00'),
            'stock': 15,
            'material': 'Silver',
            'weight': Decimal('5.20'),
            'dimensions': '8mm',
            'is_featured': True
        },
        {
            'name': 'Gold Hoop Earrings',
            'slug': 'gold-hoop-earrings',
            'description': 'Elegant gold hoop earrings that add a touch of sophistication to any outfit. Versatile design suitable for both casual and formal wear.',
            'price': Decimal('4999.00'),
            'stock': 10,
            'material': 'Gold',
            'weight': Decimal('8.50'),
            'dimensions': '25mm',
            'is_featured': True
        },
        {
            'name': 'Diamond Drop Earrings',
            'slug': 'diamond-drop-earrings',
            'description': 'Stunning diamond drop earrings that catch the light beautifully. Perfect for making a statement at special events.',
            'price': Decimal('12999.00'),
            'stock': 5,
            'material': 'Platinum',
            'weight': Decimal('12.30'),
            'dimensions': '35mm',
            'is_featured': True
        },
        {
            'name': 'Silver Leaf Earrings',
            'slug': 'silver-leaf-earrings',
            'description': 'Delicate silver leaf-shaped earrings with a modern twist. Lightweight and comfortable for all-day wear.',
            'price': Decimal('1999.00'),
            'stock': 20,
            'material': 'Silver',
            'weight': Decimal('4.80'),
            'dimensions': '15mm',
            'is_featured': False
        }
    ]
    
    for product_data in products:
        Product.objects.create(
            category=earrings_category,
            **product_data
        )

def remove_earring_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Product.objects.filter(category__slug='earrings').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0004_add_earrings_category'),
    ]

    operations = [
        migrations.RunPython(create_earring_products, remove_earring_products),
    ] 