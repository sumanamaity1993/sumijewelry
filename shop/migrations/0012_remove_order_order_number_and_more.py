# Generated by Django 5.2.3 on 2025-06-15 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_order_notes_order_order_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
    ]
