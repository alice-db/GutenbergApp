import requests
from rest_framework.views import APIView
from rest_framework.response import Response

import json
import os

from mygutenberg.models import BooksUrl
from mygutenberg.serializers import BooksUrlSerializer
from mygutenberg import util
from django.conf import settings

from django.http import Http404
from django.http import JsonResponse

# Create your views here.
class RedirectionListeDesLivres(APIView):
	def get(self, request, format=None):
		res = []
		for livre in BooksUrl.objects.all():
				serializer = BooksUrlSerializer(livre)
				res.append(serializer.data)
		return JsonResponse(res, safe=False)

class LivreDetail(APIView):
    def get_object(self, pk):
        try:
            return BooksUrl.objects.get(pk=pk)
        except BooksUrl.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        livre = self.get_object(pk)
        serializer = BooksUrlSerializer(livre)
        return JsonResponse(serializer.data)
