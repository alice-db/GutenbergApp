# Generated by Django 3.1.7 on 2021-03-30 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygutenberg', '0004_jaccard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jaccard',
            name='dist',
            field=models.DecimalField(decimal_places=4, default='-1', max_digits=5),
        ),
    ]
