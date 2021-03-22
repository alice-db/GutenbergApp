from django.db import models

class BooksUrl(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	bookID = models.IntegerField(default='-1')
	url = models.CharField(max_length = 1000, unique=True)

class TermesUrl(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	terme = models.CharField(max_length = 1000, unique=True)
	urls = models.CharField(max_length = 1000, unique=True)