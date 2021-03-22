import hashlib
import requests
import sys
import database.db as database

######## HTML CONTENT #########
url = 'https://www.google.com/'
r = requests.get(url)
a = r.text
#print(a)
########### end ##############


############### HASH ####################
hash_object = hashlib.sha256(a.encode())
hex_dig = hash_object.hexdigest()
#print(hex_dig)
############## end ###############


############### ARGUMENTI ####################
#crawders = (sys.argv[1])
#if int(crawders) < 1:
#    crawders = 1
#print(crawders)
############## end ###############


############### BAZA PROVERIKA ####################
db = database.DB()
db.connectDB()
db.createTables()
site_id = db.insertSite('www.facebook.com', None, None)
db.insertPage(site_id, 'DUPLICATE', 'www.insta.com', 'htlm<>blabla', '123', None)
############## end ###############