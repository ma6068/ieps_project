import urllib.request
from bs4 import BeautifulSoup

links = ['http://www.gov.si/', 'http://www.evem.gov.si/', 'http://www.e-uprava.gov.si/', 'http://www.e-prostor.gov.si/']
pictures = []

currentPageLink = links[0]
links.pop(0) # go brisime linkot na stranata koj sme go zacuvale vo "currentPageLink"
f = urllib.request.urlopen(currentPageLink)
page = f.read().decode('utf-8')
soup = BeautifulSoup(page)

linkovi = soup.find_all('a', href=True)
sliki = soup.find_all('img', src=True)

# tuka treba eden while, koj ce povikuva pajak da odi niz sekoja strana (dodeka ima strani)
# vnatre vo toj while se nadolu so ima treba da se napisi za ovie raboti konstantno da se povikuva

# ovaj for e za linkovi
for lnk in linkovi[1:10]: ################## smeni da gi pomini site ############################
    if lnk['href'] != '/': # if the link is not empty add the link to the database
        links.append(currentPageLink + (lnk['href'])[1:])

print(links)

# ovaj for e za sliki
for sl in sliki[1:10]: ################## smeni da gi pomini site ############################
    if lnk['href'] != '/': # if the img is not empty add the img to the database
        pictures.append(currentPageLink + (sl['src'])[1:])

print(pictures)