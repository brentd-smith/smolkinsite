from django.core.management.base import BaseCommand, CommandError
from songs.models import ServiceName

class Command(BaseCommand):
    help = 'Trying to create a new subcommand'
    
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete poll instead of closing it',
        )
        
    def handle(self, *args, **options):
        
        for poll_id in options['poll_id']:
            if options['delete']:
                self.stdout.write("Delete id={}".format(poll_id))
            else:
                self.stdout.write("Hello id={}".format(poll_id))
