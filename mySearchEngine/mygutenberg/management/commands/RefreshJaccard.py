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
from django.db.models import Q

TEMP_PATH = settings.CATALOG_TEMP_DIR

def has_term(terms1, terms2, term):
	term1_occ = terms1.get(term)
	term2_occ = terms2.get(term)
	# test if term is not in one terms set
	# return the occurrence of the other terms set
	if term1_occ is None:
		return term2_occ
	if term2_occ is None:
		return term1_occ
	return None


def term_min_dist(terms1, terms2, term):
	term_occ = has_term(terms1, terms2, term)
	if term_occ is not None:
		return term_occ
	return min(terms1.get(term), terms2.get(term))

def term_max_dist(terms1, terms2, term):
	term_occ = has_term(terms1, terms2, term)
	if term_occ is not None:
		return term_occ
	return max(terms1.get(term), terms2.get(term))

class Command(BaseCommand):
	help = 'Refresh the Jaccard matrix.'

	def handle(self, *args, **options):
		books = BooksUrl.objects.filter(bookID__gte=1,bookID__lte=20)
		for b1 in books:
			book1 = BooksUrlSerializer(b1).data
			termes_b1 = self.find_terms(book1)
			if len(termes_b1) > 0:
				for b2 in books:
					book2 = BooksUrlSerializer(b2).data
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
				max_dist = term_max_dist(termes_b1, termes_b2, terme)
				jaccard_dist_up += max_dist - term_min_dist(termes_b1, termes_b2, terme)
				jaccard_dist_down += max_dist
		self.save_new_model({'x_bookID': int(book1['bookID']), 'y_bookID': int(book2['bookID']), 'dist': round(jaccard_dist_up / jaccard_dist_down, 4)})

	def find_terms(self, book):
		res = {}
		bookID = str(book['bookID'])
		terms = TermesUrl.objects.filter(Q(ids=bookID) | Q(ids__endswith=";" + bookID) | Q(ids__startswith="" + bookID + ";") | Q(ids__contains=";" + bookID + ";"))
		DOWNLOAD_PATH = os.path.join(TEMP_PATH, 'text'+bookID+'.txt')
		urllib.request.urlretrieve(book['url'], DOWNLOAD_PATH)
		with open(DOWNLOAD_PATH) as f:
			content = f.read()
			for term in terms:
				data = TermesUrlSerializer(term).data
				occ = re.findall(data['terme'], content)
				res.update({data['terme']: len(occ)})
		return res
