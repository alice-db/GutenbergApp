import requests
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response

import json
import os
import threading

from mygutenberg.models import BooksUrl
from mygutenberg.models import TermesUrl
from mygutenberg.serializers import BooksUrlSerializer
from mygutenberg.serializers import TermesUrlSerializer
from mygutenberg.utils import closeness
from mygutenberg import util
from mygutenberg import suggestion
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

class RechercheSimple(APIView):
    def get(self, request,regex,format=None):
        res = []
        for livre in TermesUrl.objects.filter(terme=str(regex)):
            serializer = TermesUrlSerializer(livre)
            ids = serializer.data['ids'].split(";")
            for id in ids:
                book = BooksUrl.objects.get(bookID = int(id))
                serial = BooksUrlSerializer(book)
                res.append(serial.data['bookID'])
        res.sort()
        result = closeness.closenessCentrality(res)
        
        return JsonResponse(result, safe = False)

class RechercheRegEx(APIView):
    def __init__ (self):
        self.ids = []

    def printBooks(self, debut, fin,regex):
        print(debut,fin)
        for livre in BooksUrl.objects.all()[debut:fin]:
            serializer = BooksUrlSerializer(livre)
            returned_research = str(0)
            try:
                returned_research = subprocess.check_output('java -jar RegExSearch-app-1.0-jar-with-dependencies.jar "'+str(regex)+'" '+str(serializer.data['bookID']), shell=True,universal_newlines=True)
                if int(returned_research) > 0:
                    self.ids.append(serializer.data['bookID'])
            except:
                print("Une erreur inconnue pour le bookID: "+str(serializer.data['bookID']))

    def get(self, request,regex,format=None):
        res = []
        regex.lower()
        threads = list()
        for i in range (0,BooksUrl.objects.all().count()+1,250):
            if i+249 > BooksUrl.objects.all().count() :
                maxi = BooksUrl.objects.all().count() 
            else :
                maxi = i+249
            x = threading.Thread(target=self.printBooks, args=(i,maxi,regex,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()
        res = self.ids
        res.sort()
        result = closeness.closenessCentrality(res)
        return JsonResponse(result, safe = False)
