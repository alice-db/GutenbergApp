# Generated by Django 3.1.7 on 2021-03-22 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygutenberg', '0002_auto_20210322_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='booksurl',
            name='auteurs',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='booksurl',
            name='cover',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
