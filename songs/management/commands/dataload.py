from django.core.management.base import BaseCommand, CommandError
from songs.models import ServiceName

import text2torah
import text2haftarah
import text2service

class Command(BaseCommand):
    help = 'Load data after a migration.'
    
    def add_arguments(self, parser):
        # Positional arguments
        # parser.add_argument('poll_id', nargs='+', type=int)
        parser.add_argument(
            '--services',
            action='store_true',
            dest='services',
            default=False,
            help='Load the services into the database.',
        )

        # Named (optional) arguments
        parser.add_argument(
            '--torah',
            action='store_true',
            dest='torah',
            default=False,
            help='Load the torah readings into the database.',
        )
       
        parser.add_argument(
            '--haftarah',
            action='store_true',
            dest='haftarah',
            default=False,
            help='Load the haftarah readings into the database.',
        )
        
    def handle(self, *args, **options):
            
        if options['torah']:
            self.stdout.write("loading the torah readings...")
            text2torah.text2db()
        elif options['haftarah']:
            self.stdout.write("loading the haftarah readings...")
            text2haftarah.text2db()
        elif options['services']:
            self.stdout.write("loading the services...")
            text2service.text2db()
        else:
            self.stdout.write("nothing to do...")





