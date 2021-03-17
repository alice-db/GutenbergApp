from django.core.management.base import BaseCommand, CommandError
from mygutenberg.models import LivresEnFrancais
from mygutenberg.serializers import LivresEnFrancaisSerializer
from django.conf import settings
import json
import time

class Command(BaseCommand):
    help = 'Refresh the list of french books.'

    def handle(self, *args, **options):
        self.stdout.write('['+time.ctime()+'] Refreshing data...')
        with open(settings.BASE_CATALOG_DIR+"/catalog.json") as json_file:
            jsondata = json.load(json_file)
        LivresEnFrancais.objects.all().delete()
        for livre in jsondata:
            french = False
            for lang in livre["languages"]:
                if lang == "fr":
                    french = True
            if french:
                serializer = LivresEnFrancaisSerializer(data={'livreID': str(livre['id'])})
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(self.style.SUCCESS(
                            '[' + time.ctime() + '] Successfully added book id="%s"' % livre['id']))
        self.stdout.write('[' + time.ctime() + '] Data refresh terminated.')

