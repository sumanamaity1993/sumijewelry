from django.core.management.base import BaseCommand
from shop.models import TeamMember

class Command(BaseCommand):
    help = 'Delete all team members from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all team members',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL team members. Use --confirm to proceed.'
                )
            )
            return

        # Delete all existing team members
        count = TeamMember.objects.count()
        TeamMember.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} team members!')
        ) 