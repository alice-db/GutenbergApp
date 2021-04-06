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
from decimal import Decimal

TEMP_PATH = settings.CATALOG_TEMP_DIR

class FindTermBook (threading.Thread):

	def __init__(self, content, term):
		threading.Thread.__init__(self)
		self.content = content
		self.term = TermesUrlSerializer(term).data['terme']
		self.occurrences = -1

	def run(self):
		self.occurrences = len(re.findall(self.term, self.content))
            

class Command(BaseCommand):
	help = 'Refresh the Jaccard matrix.'
	content_occurences = []

	def handle(self, *args, **options):
		books = BooksUrl.objects.all()
		self.parse_occurences_file()
		for ib1 in range(115, len(books)):
			book1 = BooksUrlSerializer(books[ib1]).data
			termes_b1 = self.find_terms_in_file(book1)
			if len(termes_b1) > 0:
				for ib2 in range(ib1 + 1, len(books)):
					book2 = BooksUrlSerializer(books[ib2]).data
					termes_b2 = self.find_terms_in_file(book2)
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

	def parse_occurences_file(self):
		f = open("occurences.txt", "r")
		content = f.read()
		f.close()
		books_occ = content.split(";;")
		for book in books_occ:
			line = book.split()
			if len(line) > 1:
				terms = {}
				for i in range(1, len(line)):
					term = line[i].split(":")
					terms.update({term[0]: float(term[1])})
				self.content_occurences.append((line[0], terms))


	# dichotomie
	def find_terms_in_file(self, book):
		bookID = book['bookID']
		inf = 0
		sup = len(self.content_occurences)
		bid = -1
		while sup > inf + 1 and bid != bookID:
			middle = inf + int((sup - inf) / 2)
			bid = int(self.content_occurences[middle][0])
			if bid < bookID:
				inf = middle
			if bid > bookID:
				sup = middle
		if bid == bookID:
			print('book ' + str(book['bookID']) + ' founded in occurences')
			return self.content_occurences[middle][1]
		print('book ' + str(book['bookID']) + ' not founded in occurences')
		return self.find_terms(book)
		

	def find_terms(self, book):
		res = {}
		threads = []
		bookID = str(book['bookID'])
		terms = TermesUrl.objects.filter(Q(ids=bookID) | Q(ids__endswith=";" + bookID) | Q(ids__startswith="" + bookID + ";") | Q(ids__contains=";" + bookID + ";"))
		DOWNLOAD_PATH = os.path.join(TEMP_PATH, 'text'+bookID+'.txt')
		try:
			urllib.request.urlretrieve(book['url'], DOWNLOAD_PATH)
			book_terms_occ = bookID + " "
			with open(DOWNLOAD_PATH, encoding="utf8") as f:
				content = f.read()
				f.close()
				for term in terms:
					threads.append(FindTermBook(content, term))
					threads[len(threads)-1].start()
				for thread in threads:
					thread.join()
					res.update({thread.term: thread.occurrences})
					book_terms_occ += thread.term + ":" + str(thread.occurrences) + " "
					if thread.occurrences == -1:
						print('err -1')
			# print to file
			if book['bookID'] == 1:
				fichier = open("occurences.txt", "a")
				fichier.write(book_terms_occ + ";;")
				print("writing done")
		except:
			print('ERROR')
		return res
