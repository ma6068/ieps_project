import urllib.request
import database.db as database
import urllib.robotparser
from bs4 import BeautifulSoup
from frontier import Frontier
from urllib.error import HTTPError
from urllib.parse import urlparse

db = database.DB()
db.connectDB()
db.createTables()

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
    siteID = db.getSiteByDomain(domain)
    if siteID == None:
        # we have to read the domain's robots.txt if the site is  not yet created in our database
        robotURL = 'https://' + domain + '/robots.txt'
        robotFile = urllib.robotparser.RobotFileParser()
        robotFile.set_url(robotURL)
        robotText = None
        siteText = None
        try:
            robotFile.read()
            if robotFile.default_entry:
                robotText = str(robotFile.default_entry)
            ############################ site_maps() does not work ###################################
            #if robotFile.site_maps():
            #    siteText = "\n".join(robotFile.site_maps())
            #print('SITE: ' + siteText)
        except Exception as exc:
            print('EXCEPTION WHILE CREATING: ')
            print(exc)

        siteID = db.insertSite(domain, robotText, siteText)

    ############ ako e duplikat vrati go originalo (hashmap), ako ne togas vrati nov #################
    ############ pageID = db.getPageByURL() if page exists: true, else: false #######
    # hashmapFunkcija -> ako e vo bazata true, ako ne false
    # ako e vo bazata getSiteByDomain() vrakja -> None, ako ne napravi ID nov i vrati go.
    ############ povikuvame insertPage(), funkcijata proveruva so hashmap dali e vnatre stranata #####
    ############ ako e vnatre vo databaza ja ima page (duplikat), vrati None #############
    ############ ako ja nema stranata togas vrati novio ID #############
    #pageID = db.insertPage(siteID, 'HTML', currentPageLink, 'dasdada', '200', None)
    #if pageID == None:
    #    print('note: this page is a duplicate, skip it.')
    #    currentPageLink = fr.getUrl()
    #    continue

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