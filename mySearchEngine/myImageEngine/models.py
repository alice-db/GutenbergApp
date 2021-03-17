from django.db import models

# Create your models here.
# Create your models here.
class ImageEngine(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length = 1000)
    url = models.CharField(max_length = 1000, unique=True)
    book_id = models.IntegerField(default='-1')
    image_id = models.IntegerField(default='-1')

    class Meta:
        ordering = ('name','book_id','image_id')