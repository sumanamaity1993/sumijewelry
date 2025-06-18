from django.db import migrations

def create_earrings_category(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Category.objects.create(
        name='Earrings',
        slug='earrings',
        description='Discover our stunning collection of earrings, from classic studs to elegant drops. Each piece is crafted with precision and care, perfect for any occasion.'
    )

def remove_earrings_category(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Category.objects.filter(slug='earrings').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0003_userprofile'),
    ]

    operations = [
        migrations.RunPython(create_earrings_category, remove_earrings_category),
    ] 