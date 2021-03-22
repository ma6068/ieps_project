import hashlib
import sys
from pip._vendor import requests
import database.db as database
import urllib.robotparser

######## HTML CONTENT #########
url = 'https://www.gov.si/'
r = requests.get(url)
a = r.text
#print(a)
hash_object = hashlib.sha256(a.encode())
hex_dig = hash_object.hexdigest()
########### end ##############


############### HASH ####################
#hash_object = hashlib.sha256(a.encode())
#hex_dig = hash_object.hexdigest()
#print(hex_dig)
############## end ###############


############### ARGUMENTI ####################
#crawders = (sys.argv[1])
#if int(crawders) < 1:
#    crawders = 1
#print(crawders)
############## end ###############


############### BAZA PROVERIKA ####################
#db = database.DB()
#db.connectDB()
#db.createTables()
#site_id = db.insertSite('www.facebook.com', None, None)
#db.insertPage(site_id, 'DUPLICATE', 'www.insta.com', 'htlm<>blabla', '123', None)
############## end ###############


