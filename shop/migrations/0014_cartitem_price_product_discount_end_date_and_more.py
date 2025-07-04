# Generated by Django 5.2.3 on 2025-06-18 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_teammember'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Price at the time of adding to cart', max_digits=10),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_end_date',
            field=models.DateTimeField(blank=True, help_text='End date for discount (optional)', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_percentage',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Discount percentage (0-100)', max_digits=5),
        ),
        migrations.AddField(
            model_name='product',
            name='discount_start_date',
            field=models.DateTimeField(blank=True, help_text='Start date for discount (optional)', null=True),
        ),
    ]
