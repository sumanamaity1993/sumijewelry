from django.core.management.base import BaseCommand
from shop.models import TeamMember
from django.core.files import File
from django.conf import settings
import os
import shutil

class Command(BaseCommand):
    help = 'Add default team members to the database'

    def handle(self, *args, **options):
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

        self.stdout.write(
            self.style.SUCCESS('Team members added successfully!')
        ) 