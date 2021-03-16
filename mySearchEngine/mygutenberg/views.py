import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from mygutenberg.config import baseUrl


# Create your views here.
class BooksList(APIView):
    def get(self, request, format=None):
        response = requests.get(baseUrl+'ebooks/')
        jsondata = response.json()
        return Response(jsondata)
#    def post(self, request, format=None):
#        NO DEFITION of post --> server will return "405 NOT ALLOWED"

class BookDetail(APIView):
    def get_object(self, pk):
        try:
            response = requests.get(baseUrl+'ebooks/'+str(pk)+'/')
            jsondata = response.json()
            return Response(jsondata)
        except:
            raise Http404
    def get(self, request, pk, format=None):
        response = requests.get(baseUrl+'ebooks/'+str(pk))
        jsondata = response.json()
        return Response(jsondata)
#    def put(self, request, pk, format=None):
#        NO DEFITION of put --> server will return "405 NOT ALLOWED"
#    def delete(self, request, pk, format=None):
#        NO DEFITION of delete --> server will return "405 NOT ALLOWED"