import urllib.request
from bs4 import BeautifulSoup
from frontier import Frontier
from urllib.error import HTTPError
from urllib.parse import urlparse

pictures = []

fr = Frontier()
fr.addUrl('https://www.gov.si/')
fr.addUrl('https://evem.gov.si/')
fr.addUrl('https://e-uprava.gov.si/')
fr.addUrl('https://e-prostor.gov.si/')

currentPageLink = fr.getUrl()

while currentPageLink != None:
    print(currentPageLink)

    try:
        f = urllib.request.urlopen(currentPageLink)
    except HTTPError:
        # vo slucaj da e nekoj los link, zemame link od druga strana i odime od pocetok
        print('ERROR: THIS PAGE DOES NOT EXIST')
        currentPageLink = fr.getUrl()
        continue

    # ova mora zaradi preusmeruvanje, koga sme preusmereni proveruvame na koj link sme sega
    # ako sme preusmereni ova ce go daj tocnio, toj koj so se koristi, i se e bez problem
    currentPageLink = f.url
    page = f.read().decode('utf-8')
    soup = BeautifulSoup(page, 'html5lib')

    domain = urlparse(currentPageLink).netloc # dava primer www.gov.si -> mora https://......../pomoc/
    print('DOMAIN: ' + domain)
    ############ tuka treba da proverime dali go ima domain vo bazata, ako ne go dodavame ############

    linkovi = soup.find_all('a', href=True)
    sliki = soup.find_all('img', src=True)

    # ovaj for e za linkovi
    for lnk in linkovi[1:10]: ################## smeni da gi pomini site ############################
        # if the link is not empty add the link to the database
        if lnk['href'] != '/':
            if (lnk['href']).startswith('http'):
                fr.addUrl(lnk['href'])
            else:
                # 'https://' + 'www.gov.si' + '/pomoc/
                fr.addUrl('https://' + domain + lnk['href'])

    # ovaj for e za sliki
    for sl in sliki[1:10]: ################## smeni da gi pomini site ############################
        if lnk['href'] != '/': # if the img is not empty add the img to the database
            pictures.append(currentPageLink + (sl['src'])[1:])

    currentPageLink = fr.getUrl() # ova posledno za da zemi strana od pocetoko




# tuka treba eden while, koj ce povikuva pajak da odi niz sekoja strana (dodeka ima strani)
# vnatre vo toj while se nadolu so ima treba da se napisi za ovie raboti konstantno da se povikuva


