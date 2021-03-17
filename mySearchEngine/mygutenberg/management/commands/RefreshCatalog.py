import requests
from subprocess import call
import json
import os
import shutil
from time import strftime
import sys
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from mygutenberg import util

from mygutenberg.models import Livres
from mygutenberg.serializers import LivresSerializer
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


def put_catalog_in_db():
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
    book_directories = [str(id) for id in book_ids]
    books = []
    cpt = 0
    for directory in book_directories:
        id = int(directory)

        if (id > 0) and (id % 500 == 0):
            log('    %d' % id)

        book_path = os.path.join(
            settings.CATALOG_RDF_DIR,
            directory,
            'pg' + directory + '.rdf'
        )

        book = util.get_book(id, book_path)
        books.append(book)
        if cpt == 1664:
            break
        cpt+=1
    with open(settings.BASE_CATALOG_DIR+"/catalog.json", "w") as write_file:
        json.dump(books, write_file)

class Command(BaseCommand):
    help = 'This replaces the catalog files with the latest ones.'

    def handle(self, *args, **options):
        try:
            date_and_time = strftime('%H:%M:%S on %B %d, %Y')
            log('Starting script at', date_and_time)

            log('  Making temporary directory...')
            if os.path.exists(TEMP_PATH):
                raise CommandError(
                    'The temporary path, `' + TEMP_PATH + '`, already exists.'
                )
            else:
                os.makedirs(TEMP_PATH)

            log('  Downloading compressed catalog...')
            urllib.request.urlretrieve(URL, DOWNLOAD_PATH)

            log('  Decompressing catalog...')
            if not os.path.exists(DOWNLOAD_PATH):
                os.makedirs(DOWNLOAD_PATH)
            with open(os.devnull, 'w') as null:
                call(
                    ['tar', 'fjvx', DOWNLOAD_PATH, '-C', TEMP_PATH],
                    stdout=null,
                    stderr=null
                )

            log('  Detecting stale directories...')
            if not os.path.exists(MOVE_TARGET_PATH):
                os.makedirs(MOVE_TARGET_PATH)
            new_directory_set = get_directory_set(MOVE_SOURCE_PATH)
            old_directory_set = get_directory_set(MOVE_TARGET_PATH)
            stale_directory_set = old_directory_set - new_directory_set

            log('  Removing stale directories and books...')
            for directory in stale_directory_set:
                try:
                    book_id = int(directory)
                except ValueError:
                    # Ignore the directory if its name isn't a book ID number.
                    continue
                path = os.path.join(MOVE_TARGET_PATH, directory)
                shutil.rmtree(path)

            log('  Replacing old catalog...')
            with open(os.devnull, 'w') as null:
                with open(LOG_PATH, 'a') as log_file:
                    call(
                        [
                            'rsync',
                            '-va',
                            '--delete-after',
                            MOVE_SOURCE_PATH + '/',
                            MOVE_TARGET_PATH
                        ],
                        stdout=null,
                        stderr=log_file
                    )

            log('  Putting the catalog in the database...')
            put_catalog_in_db()

            log('  Removing temporary files...')
            shutil.rmtree(TEMP_PATH)

            log('Done!\n')
        except Exception as error:
            error_message = str(error)
            log('Error:', error_message)
            log('')
            shutil.rmtree(TEMP_PATH)