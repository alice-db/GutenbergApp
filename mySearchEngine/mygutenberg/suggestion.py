from mygutenberg.models import Jaccard
from mygutenberg.models import BooksUrl
from mygutenberg.serializers import JaccardSerializer
from mygutenberg.serializers import BooksUrlSerializer
from django.db.models import Q


def getSuggestions(results):
    if len(results) > 1:
        # keep the 2 most relevant sorted results
        return getSuggestionsForRelevantResults(results[0:2])
    else:
        return []


def getSuggestionsForRelevantResults(previousBooks):
    closeBooks = []
    res = []
    for previousBook in previousBooks:
        jaccardDistances = Jaccard.objects.filter(Q(x_bookID=previousBook['bookID']) | Q(
            y_bookID=previousBook['bookID']))
        closestJaccardDistances = getClosestJaccardEntries(
            JaccardSerializer(jaccardDistances, many=True).data)
        closeBooks += getBooksFromJaccardEntries(
            closestJaccardDistances, previousBook['bookID'])
    for book in closeBooks:
        res.append(BooksUrlSerializer(book).data)
    return res


def getClosestJaccardEntries(jaccardDistances):
    jaccards = []
    if len(jaccardDistances) > 3:
        # keep the 3 closest books for each most relevant result
        for i in range(3):
            jaccards.append(getClosestJaccardEntry(jaccardDistances))
    else:
        jaccards = jaccardDistances  # no
    return jaccards


def getClosestJaccardEntry(jaccardDistances):
    minDistJaccard = jaccardDistances[0]
    idx = 0
    for i in range(len(jaccardDistances)):
        jaccardDist = jaccardDistances[i]
        if jaccardDist['dist'] < minDistJaccard['dist']:
            minDistJaccard = jaccardDist
            idx = i
    jaccardDistances.pop(idx)
    return minDistJaccard


def getBooksFromJaccardEntries(jaccardDistances, bookID):
    books = []
    for jaccardDist in jaccardDistances:
        if jaccardDist['x_bookID'] == bookID:
            closeBookID = jaccardDist['y_bookID']
        else:
            closeBookID = jaccardDist['x_bookID']
        books.append(BooksUrl.objects.get(bookID=closeBookID))
    return books
