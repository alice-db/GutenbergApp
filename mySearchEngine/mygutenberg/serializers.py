from rest_framework.serializers import ModelSerializer
from mygutenberg.models import BooksUrl

class BooksUrlSerializer(ModelSerializer):
	class Meta:
		model = BooksUrl
		fields = ('id','bookID', 'url')

