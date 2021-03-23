import hashlib
from urllib.request import urlopen, Request
from datetime import datetime
from pip._vendor import requests
from url_normalize import url_normalize
import database.db as database
import urllib.robotparser
from bs4 import BeautifulSoup
from frontier import Frontier
from urllib.error import HTTPError
from urllib.parse import urlparse, urlsplit, urljoin


def canonicalUrl(url):
    splited =  '{uri.scheme}://{uri.netloc}/'.format(uri=urlsplit(url))
    return url_normalize(urljoin(splited, url))


robotPages = []
def takeAllRobotPages(robotText):
    for line in robotText.split("\n"):
        if line.startswith('Disallow'):  # this is for disallowed url
            robotPages.append(line.split(': ')[1].split(' ')[0])


db = database.DB()
db.connectDB()
db.createTables()

pictures = []

fr = Frontier()
fr.addUrl('https://www.gov.si/', 0)
fr.addUrl('https://evem.gov.si/', 0)
fr.addUrl('https://e-uprava.gov.si/', 0)
fr.addUrl('https://e-prostor.gov.si/', 0)

# currentPageLink = (url, idParent)
currentPageLink = fr.getUrl()

while currentPageLink[0] is not None:
    # ovoj url veke go imame vo bazata => zemi nareden
    if db.getPageByUrl(canonicalUrl(currentPageLink[0])) is not None:
        currentPageLink = fr.getUrl()
        continue

    # probaj da ja otvoris narednata strana so e na red
    try:
        f = urlopen(Request(currentPageLink[0], headers={'User-Agent': 'fri-wier-obidzuko'}), timeout=10)
        htmlStatusCode = f.getcode()
    except HTTPError:
        # vo slucaj da e nekoj los link, zemame link od druga strana i odime od pocetok
        print('ERROR: THIS PAGE DOES NOT EXIST')
        currentPageLink = fr.getUrl()
        continue

    # ova mora zaradi preusmeruvanje, koga sme preusmereni proveruvame na koj link sme sega
    # ako sme preusmereni ova ce go daj tocnio, toj koj so se koristi, i se e bez problem
    currentPageLink[0] = f.url
    page = f.read().decode('utf-8')
    soup = BeautifulSoup(page)

    domain = urlparse(currentPageLink[0]).netloc # dava primer www.gov.si -> mora https://......../pomoc/
    print('DOMAIN: ' + domain)
    if ".gov.si" not in domain:
        currentPageLink[0] = fr.getUrl()
        continue

    # gledame dali sme na istiot domain, ako ne sme => dodadi nov site
    siteID = db.getSiteByDomain(domain)
    if siteID is None:
        # procitaj go robot.txt na toj site
        robotURL = 'https://' + domain + '/robots.txt'
        robotFile = urllib.robotparser.RobotFileParser()
        robotFile.set_url(robotURL)
        robotText = None
        siteText = None
        try:
            robotFile.read()
            if robotFile.default_entry:
                robotText = str(robotFile.default_entry)
                takeAllRobotPages(robotText)
                print(robotPages)
            if robotFile.site_maps():
                siteText = str("\n".join(robotFile.site_maps()))
        except Exception as exc:
            print('EXCEPTION WHILE CREATING: ')
            print(exc)

        siteID = db.insertSite(domain, robotText, siteText)

    html_content = requests.get(currentPageLink[0]).text
    hash_object = hashlib.sha256(html_content.encode())
    html_hash = hash_object.hexdigest()

    # gledame dali toj page e duplikat
    if db.getPageByHash(html_hash) is None:
        ##################### smeni page content #####################
        pageID = db.insertPage(siteID, 'HTML', canonicalUrl(currentPageLink[0]), html_content,
                               htmlStatusCode, datetime.now(), html_hash)
        if currentPageLink[1] != 0:
            db.insertLink(currentPageLink[1], pageID)
    else:
        ###################### smeni status code #####################
        pageID = db.insertPage(siteID, 'DUPLICATE', canonicalUrl(currentPageLink[0]), html_content,
                               htmlStatusCode, datetime.now(), html_hash)
        if currentPageLink[1] != 0:
            db.insertLink(currentPageLink[1], pageID)
        currentPageLink = fr.getUrl()
        continue

    linkovi = soup.find_all('a', href=True)
    sliki = soup.find_all('img', src=True)

    # ovaj for e za linkovi
    for lnk in linkovi[1:10]: ################## smeni da gi pomini site ############################
        # if the link is not empty add the link to the database
        if lnk['href'] != '/':
            if (lnk['href']).startswith('http'):
                fr.addUrl(lnk['href'], pageID)
            else:
                # 'https://' + 'www.gov.si' + '/pomoc/
                fr.addUrl('https://' + domain + lnk['href'], pageID)

    # ovaj for e za sliki
    for sl in sliki[1:10]: ################## smeni da gi pomini site ############################
        if lnk['href'] != '/': # if the img is not empty add the img to the database
            pictures.append(currentPageLink[0] + (sl['src'])[1:])

    currentPageLink = fr.getUrl() # ova posledno za da zemi strana od pocetoko




###################### STA NAMA OBIDZUKOVCI FALI (OSIM MOZAK I NERVE) ##########################
# 1. lista za robots da ne mozi da vleguva vo zabranetite
# 2. page_data treba da se sredi
# 3. page type code (page tabela) - ne razlikuvame html/binary/frontier samo za duplicate ima
# 4. slikite treba da se sreda
# 5. datatype tabela - pdf,doc,docx...
# 6. status code (page tabela) - ne raboti ko ce e 404 error i taka natamu
# 7. (luksuz) povekje roboti da rabotat istovremeno
# 8. (luksuz) za da ne go preopteretuvame servero TIMEOUT
# 9. (luksuz) agent so imeto obidzuko
# 10. za page ne proveruvame robot.txt

######################## prasanja koi ne' macat ########################
# 1.
# 2.