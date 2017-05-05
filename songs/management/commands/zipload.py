from django.core.management.base import BaseCommand, CommandError
from songs.models import ServiceName

from s3 import SongsRepository
import zipTorah


class Command(BaseCommand):
    help = 'Import a zip file with new data.'
    
    def add_arguments(self, parser):
        
        # Positional arguments
        parser.add_argument('zip_file_name', nargs='+', type=str)
        
        parser.add_argument(
            '--services',
            action='store_true',
            dest='services',
            default=False,
            help='Load services from the zip file into the database and S3.',
        )

        # Named (optional) arguments
        parser.add_argument(
            '--torah',
            action='store_true',
            dest='torah',
            default=False,
            help='Load torah readings from the zip file into the database and S3.',
        )
       
        parser.add_argument(
            '--haftarah',
            action='store_true',
            dest='haftarah',
            default=False,
            help='Load haftarah readings into the database and S3.',
        )
        
    def handle(self, *args, **options):
           
        for zip_file_name in options['zip_file_name']:
            if options['torah']:
                self.stdout.write("Importing the torah readings...")
                # text2torah.text2db()
                # TODO: Put these into a transaction, try-except-clause, need some way to 
                # undo in case of errors
                zipTorah.createImagesFromPdf(zip_file_name)
                sr = SongsRepository()
                sr.upload_zip(zip_file_name)
                zipTorah.loadMetadataToDb(zip_file_name)
            elif options['haftarah']:
                self.stdout.write("Not Implemented Yet!") # Importing the haftarah readings...")
                # text2haftarah.text2db()
            elif options['services']:
                self.stdout.write("Not Implemented Yet!") # Importing the services...")
                # text2service.text2db()
            else:
                self.stdout.write("nothing to do...")
