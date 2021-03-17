import requests
from rest_framework.views import APIView
from rest_framework.response import Response

from mygutenberg.models import LivresEnFrancais
from mygutenberg.serializers import LivresEnFrancaisSerializer
from mygutenberg.models import LivresEnAnglais
from mygutenberg.serializers import LivresEnAnglaisSerializer
from mygutenberg.models import Livres
from mygutenberg.serializers import LivresSerializer
import json
import os

from mygutenberg import util
from django.conf import settings

from django.http import Http404
from django.http import JsonResponse


# Create your views here.
class RedirectionListeDesLivres(APIView):
    def get(self, request, format=None):
        res = []
        for livre in Livres.objects.all():
            serializer = LivresSerializer(livre)
            book_path = os.path.join(settings.CATALOG_RDF_DIR, str(serializer.data["livreID"]),
                                     'pg' + str(serializer.data["livreID"]) + '.rdf')
            book = util.get_book(str(serializer.data["livreID"]), book_path)
            res.append(book)
        return JsonResponse(res, safe=False)

class LivreImageRandomDetail(APIView):
    def get(self, pk):
        try:
            response = requests.get("http://127.0.0.1:8000/myBook/"+str(pk)+'/image/')
            jsondata = response.json()
            return Response(jsondata)
        except:
            raise Http404

class LivreCoverImageDetail(APIView):
    def get(self, pk):
        try:
            response = requests.get("http://127.0.0.1:8000/myBook/"+str(pk)+'/cover/')
            jsondata = response.json()
            return Response(jsondata)
        except:
            raise Http404

class LivreImageDetail(APIView):
    def get(self, pk, ipk):
        try:
            response = requests.get("http://127.0.0.1:8000/myBook/"+str(pk)+'/image/'+str(ipk))
            jsondata = response.json()
            return Response(jsondata)
        except:
            raise Http404

class LivreDetail(APIView):
    def get_object(self, pk):
        try:
            return Livres.objects.get(pk=pk)
        except Livres.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        livre = self.get_object(pk)
        serializer = LivresSerializer(livre)
        book_path = os.path.join(settings.CATALOG_RDF_DIR, str(serializer.data["livreID"]),
                                 'pg' + str(serializer.data["livreID"]) + '.rdf')
        book = util.get_book(str(serializer.data["livreID"]), book_path)
        return Response(book)

class LivresEnFrancaisList(APIView):
    def get(self, request, format=None):
        res = []
        for livre in LivresEnFrancais.objects.all():
            serializer = LivresEnFrancaisSerializer(livre)
            book_path = os.path.join(settings.CATALOG_RDF_DIR,str(serializer.data["livreID"]),'pg' + str(serializer.data["livreID"]) + '.rdf')
            book = util.get_book(str(serializer.data["livreID"]), book_path)
            res.append(book)
        return JsonResponse(res, safe=False)

class LivreEnFrancaisDetail(APIView):
    def get_object(self, pk):
        try:
            return LivresEnFrancais.objects.get(pk=pk)
        except LivresEnFrancais.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        livre = self.get_object(pk)
        serializer = LivresEnFrancaisSerializer(livre)
        book_path = os.path.join(settings.CATALOG_RDF_DIR, str(serializer.data["livreID"]),
                                 'pg' + str(serializer.data["livreID"]) + '.rdf')
        book = util.get_book(str(serializer.data["livreID"]), book_path)
        return Response(book)

class LivresEnAnglaisList(APIView):
    def get(self, request, format=None):
        res = []
        for livre in LivresEnAnglais.objects.all():
            serializer = LivresEnAnglaisSerializer(livre)
            book_path = os.path.join(settings.CATALOG_RDF_DIR,str(serializer.data["livreID"]),'pg' + str(serializer.data["livreID"]) + '.rdf')
            book = util.get_book(str(serializer.data["livreID"]), book_path)
            res.append(book)
        return JsonResponse(res, safe=False)

class LivreEnAnglaisDetail(APIView):
    def get_object(self, pk):
        try:
            return LivresEnAnglais.objects.get(pk=pk)
        except LivresEnAnglais.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        livre = self.get_object(pk)
        serializer = LivresEnAnglaisSerializer(livre)
        book_path = os.path.join(settings.CATALOG_RDF_DIR, str(serializer.data["livreID"]),
                                 'pg' + str(serializer.data["livreID"]) + '.rdf')
        book = util.get_book(str(serializer.data["livreID"]), book_path)
        return Response(book)