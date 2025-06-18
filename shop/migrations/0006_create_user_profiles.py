from django.db import migrations

def create_profiles_for_existing_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('shop', 'UserProfile')
    
    # Create profiles for all users that don't have one
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)

def reverse_create_profiles(apps, schema_editor):
    UserProfile = apps.get_model('shop', 'UserProfile')
    UserProfile.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0005_add_earring_products'),
    ]

    operations = [
        migrations.RunPython(create_profiles_for_existing_users, reverse_create_profiles),
    ] 