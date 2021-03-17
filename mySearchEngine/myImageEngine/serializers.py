from rest_framework.serializers import ModelSerializer
from myImageEngine.models import ImageEngine

class ImageEngineSerializer(ModelSerializer):
    class Meta:
        model = ImageEngine
        fields = ('id', 'name', 'url')
