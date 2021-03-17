from rest_framework.serializers import ModelSerializer
from mygutenberg.models import LivresEnFrancais
from mygutenberg.models import LivresEnAnglais
from mygutenberg.models import Livres

class LivresEnAnglaisSerializer(ModelSerializer):
    class Meta:
        model = LivresEnAnglais
        fields = ('id', 'livreID')

class LivresEnFrancaisSerializer(ModelSerializer):
    class Meta:
        model = LivresEnFrancais
        fields = ('id', 'livreID')

class LivresSerializer(ModelSerializer):
    class Meta:
        model = Livres
        fields = ('id', 'livreID')
