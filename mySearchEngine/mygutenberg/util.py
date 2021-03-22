import xml.etree.ElementTree as parser
import re
import os
import shutil
from time import strftime
import sys
import urllib.request
from django.conf import settings

LINE_BREAK_PATTERN = re.compile(r'[ \t]*[\n\r]+[ \t]*')
NAMESPACES = {
    'dc': 'http://purl.org/dc/terms/',
    'dcam': 'http://purl.org/dc/dcam/',
    'pg': 'http://www.gutenberg.org/2009/pgterms/',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
}
NS = dict(
        pg='http://www.gutenberg.org/2009/pgterms/',
        dc='http://purl.org/dc/terms/',
        dcam='http://purl.org/dc/dcam/',
        rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#')

TEMP_PATH = settings.CATALOG_TEMP_DIR

DOWNLOAD_PATH = os.path.join(TEMP_PATH, '/files')

def fix_subtitles(title):
    """
    This formats subtitles with (semi)colons instead of new lines. The first
    subtitle is introduced with a colon, and the rest are introduced with
    semicolons.
    >>> fix_subtitles(u'First Across ...\r\nThe Story of ... \r\n'
    ... 'Being an investigation into ...')
    u'First Across ...: The Story of ...; Being an investigation into ...'
    """

    new_title = LINE_BREAK_PATTERN.sub(': ', title, 1)
    return LINE_BREAK_PATTERN.sub('; ', new_title)


def get_book(id, xml_file_path):
    """ Based on https://gist.github.com/andreasvc/b3b4189120d84dec8857 """

    # Parse the XML.
    document = None
    try:
        document = parser.parse(xml_file_path)
    except:
        raise Exception('The XML file could not be parsed.')

    # Get the book node.
    root = document.getroot()
    book = root.find('{%(pg)s}ebook' % NAMESPACES)

    result = {
        'id' : int(id),
        'url': []
    }

    # formats
    formats = {file.find('{%(dc)s}format//{%(rdf)s}value' % NS).text:
            file.get('{%(rdf)s}about' % NS)
            for file in book.findall('.//{%(pg)s}file' % NS)}

    for x in formats:
        if formats[x].find('txt') != -1:
            try:
                URL = formats[x]
                DOWNLOAD_PATH = os.path.join(TEMP_PATH, 'text'+str(id)+".txt")
                urllib.request.urlretrieve(URL, DOWNLOAD_PATH)
                result['url'].append(URL)
                break
            except:
                print("ERROR")

    return result


def safe_unicode(arg, *args, **kwargs):
    """ Coerce argument to Unicode if it's not already. """
    return arg if isinstance(arg, str) else str(arg, *args, **kwargs)