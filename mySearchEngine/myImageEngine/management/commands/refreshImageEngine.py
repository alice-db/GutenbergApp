from django.core.management.base import BaseCommand, CommandError
from myImageEngine.models import ImageEngine
from myImageEngine.serializers import ImageEngineSerializer
from myImageBank.models import ImageUrl
from myImageBank.serializers import ImageUrlSerializer
import requests
import time

class Command(BaseCommand):
    help = 'Refresh the list of products which are on sale.'
    def handle(self, *args, **options):
        baseUrl = 'http://51.255.166.155:1352/tig/'
        self.stdout.write('['+time.ctime()+'] Refreshing data...')
        jsondata = response.json()
        ImageEngine.objects.all().delete()
        for product in jsondata:
            images = ImageUrl.objects.all()
            image = secrets.choice(images)
            serializer = ImageUrlSerializer(image)
            try:
                serializers = ImageEngineSerializer(data={'name':str(product['name']), 'url': serializer.data['url']})
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(self.style.SUCCESS('['+time.ctime()+'] Successfully added product id="%s"' % product['id']))
        self.stdout.write('['+time.ctime()+'] Data refresh terminated.')
