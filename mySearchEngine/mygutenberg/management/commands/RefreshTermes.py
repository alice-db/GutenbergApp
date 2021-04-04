import os
import time
import urllib.request
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from mygutenberg.models import BooksUrl
from mygutenberg.serializers import BooksUrlSerializer
from mygutenberg.models import TermesUrl
from mygutenberg.serializers import TermesUrlSerializer
import re

TEMP_PATH = settings.CATALOG_TEMP_DIR

blacklist_en = ["a","an","but", "or", "where","when","has", "and", "therefore", "or", "neither", "because", "to", "in", "by", "for","to","with","from","without","under","on","against","despite","at","among","that", "what", "which", "which", "he", "she", "they","them", "some", "such","so","I","us","you","it","yes","no","indeed","otherwise","many","the","this","there","of","here","over","all","more","are","may","be","both","old","were","one","two","is","our","his","her","out","most","into","either","if","its","do","don't","as","must","your","these","have","been","can","any","not","other","even","only","dont","just","end","each","within","without","with","we","per","way","new","than","ever","get","up","top","give","had","been","zip","tar","gz","dmg","exe","www","fr","en","com","http","https"]
blacklist_fr = ["mais","ou","où","et","donc","or","ni","car","à","dans","par","pour","en","vers","avec","de","sans","sous","sur","contre","malgré","chez","parmi","que","quoi","quoi","quel","quelle","qu'il","qu'elle","qu'ils","qu'elles","quelque","quelques","tel","telle","tellement","je","tu","nous","vous","oui","non","cas","ici"]
blacklist = blacklist_en+blacklist_fr

numbers = ["1","2","3","4","5","6","7","8","9","0"]

def preg_macth(mot):
    for l in blacklist:
        if l == mot.lower() or l == mot:
            return True
    return False

def changeCharac(mot):
    mot = re.sub('[^A-Za-z0-9]+', ' ', mot)
    return mot

class Command(BaseCommand):
    help = 'Refresh the list of english books.'

    def handle(self, *args, **options):
        livres = BooksUrl.objects.filter(bookID__gte=464,bookID__lte=1993)
        for livre in livres:
            serializer = BooksUrlSerializer(livre)
            url = serializer.data['url']
            id = serializer.data['bookID']
            print("---------------------------LIVRE",id,"-------------------------")
            try:
                URL = url
                DOWNLOAD_PATH = os.path.join(TEMP_PATH, 'text'+str(id)+".txt")
                urllib.request.urlretrieve(URL, DOWNLOAD_PATH)
                with open(DOWNLOAD_PATH) as f:
                    lines = f.readlines()
                for i in range (len(lines)):
                    sentence = lines[i].split()
                    mots = []
                    for mot in sentence:
                        mot = changeCharac(mot)
                        new_mots = mot.split()
                        for mt in new_mots:
                            mots.append(mt)
                    for mot in mots:
                        isBlacklister = preg_macth(mot)
                        mot = mot.lower()
                        if not isBlacklister and mot != "" and len(mot) > 1:
                            count_terme = TermesUrl.objects.filter(terme=str(mot)).count()
                            if count_terme == 0:
                                new_serializer = TermesUrlSerializer(data={'terme': str(mot), 'ids': str(id)})
                                if new_serializer.is_valid():
                                    try:
                                        new_serializer.save()
                                    except:
                                        print("ERROR SAVE SERIALIZER")
                                else :
                                    print("ERROR SERIALIZER")
                            else :
                                termes = TermesUrl.objects.filter(terme=str(mot))
                                for terme in termes:
                                    serial = TermesUrlSerializer(terme)
                                    id_string = serial.data['ids']
                                    ids = id_string.split(";")
                                    if str(id) not in ids:
                                        ids.append(str(id))
                                        new_ids = ";".join(ids)
                                        TermesUrl.objects.filter(pk=terme.pk).update(ids=str(new_ids))
                                        terme.refresh_from_db()
            except:
                print("ERROR")
            self.stdout.write(self.style.SUCCESS('[' + time.ctime() + '] Livre avec comme url ="%s"' % str(serializer.data['bookID'])))
