import requests
from subprocess import call
import json
import os
import shutil
import time
from time import strftime
import sys
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from mygutenberg import util

from mygutenberg.models import BooksUrl
from mygutenberg.serializers import BooksUrlSerializer
#from books.models import *


TEMP_PATH = settings.CATALOG_TEMP_DIR

URL = 'https://gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2'
DOWNLOAD_PATH = os.path.join(TEMP_PATH, 'catalog.tar.bz2')

MOVE_SOURCE_PATH = os.path.join(TEMP_PATH, 'cache/epub')
MOVE_TARGET_PATH = settings.CATALOG_RDF_DIR

LOG_DIRECTORY = settings.CATALOG_LOG_DIR
LOG_FILE_NAME = strftime('%Y-%m-%d_%H%M%S') + '.txt'
LOG_PATH = os.path.join(LOG_DIRECTORY, LOG_FILE_NAME)


# This gives a set of the names of the subdirectories in the given file path.
def get_directory_set(path):
    directory_set = set()
    for directory_item in os.listdir(path):
        item_path = os.path.join(path, directory_item)
        if os.path.isdir(item_path):
            directory_set.add(directory_item)
    return directory_set


def log(*args):
    print(*args)
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)
    with open(LOG_PATH, 'a') as log_file:
        text = ' '.join(args) + '\n'
        log_file.write(text)


def put_catalog_in_db(self):
    book_ids = []
    for directory_item in os.listdir(settings.CATALOG_RDF_DIR):
        item_path = os.path.join(settings.CATALOG_RDF_DIR, directory_item)
        if os.path.isdir(item_path):
            try:
                book_id = int(directory_item)
            except ValueError:
                # Ignore the item if it's not a book ID number.
                pass
            else:
                book_ids.append(book_id)
    book_ids.sort()
    books = BooksUrl.objects.all()
    for b in books:
        serializer = BooksUrlSerializer(b)
        id = int(serializer.data['bookID'])

        if (id > 0) and (id % 500 == 0):
            log('%d' % id)

        book_path = os.path.join(
            settings.CATALOG_RDF_DIR,
            str(serializer.data['bookID']),
            'pg' + str(serializer.data['bookID']) + '.rdf'
        )
        book = util.get_book(id, book_path)
        try:
            BooksUrl.objects.filter(pk=b.pk).update(cover=book['cover'])
            BooksUrl.objects.filter(pk=b.pk).update(auteurs=book['auteurs'])
            b.refresh_from_db()
            print("Update success")
        except:
            print("Update fail")

class Command(BaseCommand):
    help = 'This replaces the catalog files with the latest ones.'

    def handle(self, *args, **options):
        try:
            log('Start')
            put_catalog_in_db(self)
            log('Done!\n')
        except Exception as error:
            error_message = str(error)
            log('Error:', error_message)
            log('')
            shutil.rmtree(TEMP_PATH)