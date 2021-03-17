from django.db import models

# Create your models here.
class LivresEnAnglais(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    livreID = models.IntegerField(default='-1')

    class Meta:
        ordering = ('livreID',)

class LivresEnFrancais(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    livreID = models.IntegerField(default='-1')

    class Meta:
        ordering = ('livreID',)

class Livres(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    livreID = models.IntegerField(default='-1')

    class Meta:
        ordering = ('livreID',)