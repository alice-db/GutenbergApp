from mygutenberg.models import Jaccard
from mygutenberg.serializers import JaccardSerializer
from django.db.models import Q
from django.conf import settings
import csv
import random


def floydWarshall(ids, dico):
	paths = [ [0] * len(ids) ] * len(ids)

	for i in range(len(paths)):
		for j in range(len(paths)):
			paths[i][j] = i

	dist = [ [float('inf')] * len(ids) ] * len(ids)
	
	for book1 in range (len(paths)):
		i = ids[book1]
		new_distance = []
		for book2 in range (len(paths)):
			j = ids[book2]
			if book1 == book2 :
				distance = 0.0
			elif i < j :
				key = str(i)+";"+str(j)
				distance = float(dico[key])
			else : 
				key = str(j)+";"+str(i)
				distance = float(dico[key])
			new_distance.append(distance)
		dist[book1] = new_distance

	for k in range(len(paths)):
		for i in range(len(paths)):
			for j in range(len(paths)):
				if dist[i][j]>dist[i][k] + dist[k][j]:
					dist[i][j]=dist[i][k] + dist[k][j]
	return dist

def calculCloseness(distance, ids):
	new_ids = []
	cpt = 0
	
	copy_ids = ids.copy()
	while len(copy_ids) > 0:
		id_vainqueur = -1
		max_closeness = float('inf')
		for i in range(len(copy_ids)):
			dist = 0.0
			for j in range(len(ids)):
				dist += distance[i][j]
			closeness = (len(ids)-1)/dist
			if closeness < max_closeness:
				id_vainqueur = copy_ids[i]
				max_closeness = closeness
		copy_ids.remove(id_vainqueur)
		new_ids.append(id_vainqueur)

	return new_ids



def closenessCentrality(ids):
	dict_from_csv = {}
	with open(settings.DATABASES_DIR+'/jaccard.csv', mode='r') as inp:
		reader = csv.reader(inp)
		dict_from_csv = {str(rows[2])+";"+str(rows[3]):rows[4] for rows in reader}

	distances = floydWarshall(ids, dict_from_csv)
	return calculCloseness(distances, ids)