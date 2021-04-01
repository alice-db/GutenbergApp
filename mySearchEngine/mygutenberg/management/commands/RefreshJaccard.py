import os
import time
import urllib.request
import json
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from mygutenberg.models import BooksUrl
from mygutenberg.serializers import BooksUrlSerializer
from mygutenberg.models import TermesUrl
from mygutenberg.serializers import TermesUrlSerializer
from mygutenberg.models import Jaccard
from mygutenberg.serializers import JaccardSerializer
import re
import threading
from django.db.models import Q

TEMP_PATH = settings.CATALOG_TEMP_DIR

class FindTermBook (threading.Thread):

	def __init__(self, content, term):
		threading.Thread.__init__(self)
		self.content = content
		self.term = term
		self.occurrences = -1

	def run(self):
        #data = TermesUrlSerializer(self.term).data
		data = TermesUrlSerializer(self.term).data
		self.occurrences = len(re.findall(data['terme'], self.content))
            

class Command(BaseCommand):
	help = 'Refresh the Jaccard matrix.'

	def handle(self, *args, **options):
		books = BooksUrl.objects.all()
		for ib1 in range(len(books)):
			book1 = BooksUrlSerializer(books[ib1]).data
			termes_b1 = self.find_terms(book1)
			if len(termes_b1) > 0:
				for ib2 in range(ib1 + 1, len(books)):
					book2 = BooksUrlSerializer(books[ib2]).data
					termes_b2 = self.find_terms(book2)
					if book1['bookID'] != book2['bookID'] and len(termes_b2) > 0:
						print("---------------------------LIVRES", book1['bookID'], book2['bookID'], "-------------------------")
						self.jaccard_distance(book1, book2, termes_b1, termes_b2)

	def save_new_model(self, data):
		new_serializer = JaccardSerializer(data=data)
		if new_serializer.is_valid():
				try:
						new_serializer.save()
						print("save model: ", data)
				except:
						print("ERROR SAVE SERIALIZER")
		else :
				print("ERROR SERIALIZER")

	def jaccard_distance(self, book1, book2, termes_b1, termes_b2):
		jaccard_dist_up = 0
		jaccard_dist_down = 0
		union_termes = dict(termes_b1)
		union_termes.update(termes_b2)
		for terme in union_termes.keys():
				max_dist = max(termes_b1.get(terme, 0), termes_b2.get(terme, 0))
				jaccard_dist_up += max_dist - min(termes_b1.get(terme, 0), termes_b2.get(terme, 0))
				jaccard_dist_down += max_dist
		self.save_new_model({'x_bookID': int(book1['bookID']), 'y_bookID': int(book2['bookID']), 'dist': round(jaccard_dist_up / jaccard_dist_down, 4)})

	def find_terms(self, book):
		res = {}
		threads = []
		bookID = str(book['bookID'])
		terms = TermesUrl.objects.filter(Q(ids=bookID) | Q(ids__endswith=";" + bookID) | Q(ids__startswith="" + bookID + ";") | Q(ids__contains=";" + bookID + ";"))
		DOWNLOAD_PATH = os.path.join(TEMP_PATH, 'text'+bookID+'.txt')
		try:
			urllib.request.urlretrieve(book['url'], DOWNLOAD_PATH)
			with open(DOWNLOAD_PATH, encoding="utf8") as f:
				content = f.read()
				for term in terms:
					threads.append(FindTermBook(content, term))
					threads[len(threads)-1].start()
				for thread in threads:
					thread.join()
					res.update({thread.term: thread.occurrences})
					if thread.occurrences == -1:
						print('err -1')
		except:
			print('ERROR')
		return res
