from django.core.management.base import BaseCommand, CommandError
from mygutenberg.models import Livres
from mygutenberg.serializers import LivresSerializer
from django.conf import settings
import json
import time

class Command(BaseCommand):
    help = 'Refresh the list of books.'

    def handle(self, *args, **options):
        self.stdout.write('['+time.ctime()+'] Refreshing data...')
        with open(settings.BASE_CATALOG_DIR+"/catalog.json") as json_file:
            jsondata = json.load(json_file)
        Livres.objects.all().delete()
        for livre in jsondata:
            serializer = LivresSerializer(data={'livreID': str(livre['id'])})
            if serializer.is_valid():
                serializer.save()
                self.stdout.write(self.style.SUCCESS(
                            '[' + time.ctime() + '] Successfully added book id="%s"' % livre['id']))
        self.stdout.write('[' + time.ctime() + '] Data refresh terminated.')

