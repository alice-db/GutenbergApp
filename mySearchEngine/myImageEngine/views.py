from django.shortcuts import render
from django.http import Http404
from myImageEngine.models import ImageEngine
from rest_framework.views import APIView
from myImageEngine.serializers import ImageEngineSerializer
from rest_framework.response import Response

# Create your views here.
class ImageEngine(APIView):
    def get(self, request, name, format=None):
    	recherches = name.split("1664")
    	res=[]
    	for i in range (len(recherches)):
    		image = ImageEngine.objects.filter(name=recherches[i])
    		serializer = ImageEngineSerializer(image)
    		res.append({'url': serializer.data['url']})
    	return Response(res)

class ImageRandom(APIView):
	def get(self, book_id, format=None):
		images = ImageEngine.objects.all()
		image = secrets.choice(images)
		serializer = ImageEngineSerializer(image)
		try:
			return Response({'url': serializer.data['url']})
		except:
			raise Http404

class ImageCover(APIView):
	def get(self, book_id, format=None):
		image = ImageEngine.objects.filter(name="cover.jpg", book_id=book_id)
		serializer = ImageEngineSerializer(image)
		try:
			return Response({'url': serializer.data['url']})
		except:
			raise Http404

class ImageBook(APIView):
	def get(self,book_id,image_id, format=None):
		image = ImageEngine.objects.filter(image_id=cover, book_id=book_id)
		serializer = ImageEngineSerializer(image)
		try:
			return Response({'url': serializer.data['url']})
		except:
			raise Http404