from django.core.management.base import BaseCommand
from shop.models import Product

class Command(BaseCommand):
    help = 'Updates product prices to appropriate rupee values'

    def handle(self, *args, **kwargs):
        # Update prices (multiply by 75 to convert from USD to INR approximately)
        products = Product.objects.all()
        for product in products:
            # Convert price to rupees (multiply by 75)
            new_price = float(product.price) * 75
            product.price = new_price
            product.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated price for {product.name} to ₹{new_price:,.2f}')
            ) 