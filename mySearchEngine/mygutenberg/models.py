from django.db import models

class BooksUrl(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	bookID = models.IntegerField(default='-1')
	url = models.CharField(max_length = 1000, unique=True)
	auteurs = models.CharField(max_length = 1000, default="")
	cover = models.CharField(max_length = 1000,  default="")

class TermesUrl(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	terme = models.CharField(max_length = 1000, unique=True)
	ids = models.CharField(max_length = 1000)

class Jaccard(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	x_bookID = models.IntegerField(default='-1')
	y_bookID = models.IntegerField(default='-1')
	dist = models.DecimalField(default='-1', max_digits=5, decimal_places=4)
