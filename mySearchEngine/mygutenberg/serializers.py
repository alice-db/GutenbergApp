from rest_framework.serializers import ModelSerializer
from mygutenberg.models import BooksUrl
from mygutenberg.models import TermesUrl

class BooksUrlSerializer(ModelSerializer):
	class Meta:
		model = BooksUrl
		fields = ('id','bookID', 'url','cover','auteurs')

class TermesUrlSerializer(ModelSerializer):
	class Meta:
		model = TermesUrl
		fields = ('id','terme', 'urls')

