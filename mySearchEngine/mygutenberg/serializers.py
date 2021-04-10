from rest_framework.serializers import ModelSerializer
from mygutenberg.models import BooksUrl
from mygutenberg.models import TermesUrl
from mygutenberg.models import Jaccard

class BooksUrlSerializer(ModelSerializer):
	class Meta:
		model = BooksUrl
		fields = ('id','bookID', 'url','cover','auteurs','title')

class TermesUrlSerializer(ModelSerializer):
	class Meta:
		model = TermesUrl
		fields = ('id','terme','ids')

class JaccardSerializer(ModelSerializer):
	class Meta:
		model = Jaccard
		fields = ('x_bookID','y_bookID','dist')
