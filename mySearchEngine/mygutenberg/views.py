import requests
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
import csv
import json
import os
import threading

from mygutenberg.models import BooksUrl
from mygutenberg.models import TermesUrl
from mygutenberg.serializers import BooksUrlSerializer
from mygutenberg.serializers import TermesUrlSerializer
from mygutenberg.utils import closeness
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
    def get(self, request, regex, format=None):
        res = []
        termes = TermesUrl.objects.filter(terme=str(regex))
        for terme in termes:
            serializer = TermesUrlSerializer(terme)
            ids = serializer.data['ids'].split(";")
            for id in ids:
                book = BooksUrl.objects.get(bookID=int(id))
                serial = BooksUrlSerializer(book)
                res.append(serial.data['bookID'])
        res.sort()
        res_closeness = closeness.closenessCentrality(res)

        resultats = []
        for id_book in res_closeness:
            book = BooksUrl.objects.get(bookID = int(id_book))
            serializer = BooksUrlSerializer(book).data
            resultats.append(serializer)

        return JsonResponse(res_closeness, safe = False)

class RechercheRegEx(APIView):
    def __init__(self):
        self.books = []

    def printBooks(self, debut, fin,regex, dico):
        new_dics = {}
        print(debut,fin)
        for i in range(debut,fin+1):
            infos = dico[str(i)].split(";")
            id = int(infos[0])
            url = infos[1]
            try:
                returned_research = subprocess.check_output('java -jar RegExSearch-app-1.0-jar-with-dependencies.jar "'+str(regex)+'" "'+str(url)+'"', shell=True,universal_newlines=True)
                if int(returned_research) > 0:
                    self.ids.append(id)
            except:
                print("Une erreur inconnue pour le bookID: "+str(id))

    def get(self, request, regex, format=None):
        res = []
        regex.lower()
        dict_from_csv = {}
        with open(settings.DATABASES_DIR+'/database.csv', mode='r') as inp:
            reader = csv.reader(inp)
            dict_from_csv = {str(rows[0]):str(rows[2]+";"+rows[3]) for rows in reader}

        threads = list()
        for i in range (1,BooksUrl.objects.all().count()+1,50):
            if i+49 > BooksUrl.objects.all().count() :
                maxi = BooksUrl.objects.all().count()
            else :
                maxi = i+49
            x = threading.Thread(target=self.printBooks, args=(i,maxi,regex,dict_from_csv,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

        res = self.ids
        res.sort()
        res_closeness = closeness.closenessCentrality(res)

        resultats = []
        for id_book in res_closeness:
            book = BooksUrl.objects.get(bookID = int(id_book))
            serializer = BooksUrlSerializer(book).data
            resultats.append(serializer)

        return JsonResponse(resultats, safe = False)
