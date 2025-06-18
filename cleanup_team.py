import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sumi_jewelry_store.settings')
django.setup()

from shop.models import TeamMember

def cleanup_team():
    # Delete all existing team members
    TeamMember.objects.all().delete()
    print("All team members deleted successfully!")

if __name__ == '__main__':
    cleanup_team() 