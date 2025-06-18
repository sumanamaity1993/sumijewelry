import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sumi_jewelry_store.settings')
django.setup()

from shop.models import TeamMember
from django.core.files import File
from django.conf import settings
import shutil

def add_team_members():
    # Create team directory if it doesn't exist
    team_dir = os.path.join(settings.MEDIA_ROOT, 'team')
    os.makedirs(team_dir, exist_ok=True)

    # Add CEO
    ceo = TeamMember.objects.create(
        name="Sumana Maity",
        position="CEO & Founder",
        bio="Passionate about bringing exquisite jewelry to our customers. With years of experience in the jewelry industry, I founded Sumi Jewelry to create beautiful, high-quality pieces that tell unique stories.",
        order=1,
        is_active=True
    )

    # Add Developer
    developer = TeamMember.objects.create(
        name="Tapas",
        position="Lead Developer",
        bio="Expert in web/backend development and e-commerce solutions. Dedicated to creating seamless online shopping experiences and maintaining the technical excellence of Sumi Jewelry's digital presence.",
        order=2,
        is_active=True
    )

    print("Team members added successfully!")

if __name__ == '__main__':
    add_team_members() 