import hashlib
import os
import time
from urllib.request import urlopen, Request
from datetime import datetime
import requests
from url_normalize import url_normalize
import database.db as database
import urllib.robotparser
from bs4 import BeautifulSoup
from frontier import Frontier
from urllib.error import HTTPError
from urllib.parse import urlparse, urlsplit, urljoin
import urllib


def timePassed(prevTime):
    return time.time() - prevTime >= 5


def canonicalUrl(url):
    splited =  '{uri.scheme}://{uri.netloc}/'.format(uri=urlsplit(url))
    return url_normalize(urljoin(splited, url))


robotPages = []
def takeAllRobotPages(robotText, domain):
    a = robotText.split("\n")[0]
    if "*" in a or "fri-wier-obidzuko" in a:
        for line in robotText.split("\n"):
            if line.startswith('Disallow'):  # this is for disallowed url
                robotPages.append('http://' + domain + line.split(': ')[1].split(' ')[0])


db = database.DB()
db.connectDB()
db.createTables()

pictures = []

fr = Frontier()
fr.addUrl('http://www.gov.si/', 0)
fr.addUrl('http://evem.gov.si/', 0)
fr.addUrl('http://e-uprava.gov.si/', 0)
fr.addUrl('http://e-prostor.gov.si/', 0)

# currentPageLink = (url, idParent)
currentPageLink = fr.getUrl()
currentTime = time.time()

while currentPageLink is not None:
    print('CURRENT PAGE: ' + currentPageLink[0])
    if timePassed(currentTime):
        time.sleep(1)

    # probaj da ja otvoris narednata strana so e na red
    try:
        f = urlopen(Request(currentPageLink[0], headers={'User-Agent': 'fri-wier-obidzuko'}), timeout=10)
        currentTime = time.time()
    except HTTPError as httperror:
        print("STATUS CODE ERROR !!!!!!")
        print(httperror.getcode())
    except Exception:
        # vo slucaj da e nekoj los link, zemame link od druga strana i odime od pocetok
        print('ERROR: THIS PAGE DOES NOT EXIST')
        currentPageLink = fr.getUrl()
        continue

    # ova mora zaradi preusmeruvanje, koga sme preusmereni proveruvame na koj link sme sega
    # ako sme preusmereni ova ce go daj tocnio, toj koj so se koristi, i se e bez problem
    currentPageLink[0] = f.url

    print('CHANGED PAGE: ' + currentPageLink[0])
    # ako e zabraneto (robots.txt) zemi naredna strana
    if currentPageLink[0] in robotPages:
        currentPageLink = fr.getUrl()
        continue

    # ovoj url veke go imame vo bazata => zemi nareden
    if db.getPageByUrl(canonicalUrl(currentPageLink[0])) is not None:
        currentPageLink = fr.getUrl()
        continue

    if '.zip' in currentPageLink[0]:
        currentPageLink = fr.getUrl()
        continue

    domain = urlparse(currentPageLink[0]).netloc # dava primer www.gov.si -> mora https://......../pomoc/
    if ".gov.si" not in domain:
        currentPageLink = fr.getUrl()
        continue
    print('DOMAIN: ' + domain)

    info = f.info()
    page_type_code = info.get_content_type()
    print(page_type_code)
    htmlStatusCode = f.getcode()
    if page_type_code == 'text/html':
        page = f.read().decode('utf-8')
        soup = BeautifulSoup(page)
        html_content = page
        hash_object = hashlib.sha256(html_content.encode())
        html_hash = hash_object.hexdigest()

        # gledame dali toj page e duplikat
        hashPageId = db.getPageByHash(html_hash)
    else:
        hashPageId = None
        html_content = None
        html_hash = None

    # gledame dali sme na istiot domain, ako ne sme => dodadi nov site
    siteID = db.getSiteByDomain(domain)
    if siteID is None:
        # procitaj go robot.txt na toj site
        robotURL = 'http://' + domain + '/robots.txt'
        robotFile = urllib.robotparser.RobotFileParser()
        robotFile.set_url(robotURL)
        robotText = None
        siteText = None
        try:
            robotFile.read()
            if robotFile.default_entry:
                robotText = str(robotFile.default_entry)
                takeAllRobotPages(robotText, domain)
                print(robotPages)
            if robotFile.site_maps():
                siteText = str("\n".join(robotFile.site_maps()))
        except Exception:
            robotText = None
            siteText = None
            print('EXCEPTION WHILE CREATING ROBOT')

        siteID = db.insertSite(domain, robotText, siteText)

    if hashPageId is None:
        if 'text/html' in page_type_code:
            page_type_code = 'HTML'
        else:
            page_type_code = 'BINARY'
            request_headers = requests.utils.default_headers()
            request_headers.update(
                {"User-Agent": "fri-wier-obidzuko"}
            )
            response = requests.head(currentPageLink[0], headers=request_headers)
            headers = response.headers
            content_type_headers = headers.get('content-type')
            content_type = "/"
            if content_type_headers == 'application/vnd.ms-powerpoint':
                content_type = 'PPT'
            elif content_type_headers == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
                content_type = 'PPTX'
            elif content_type_headers == 'application/msword':
                content_type = 'DOC'
            elif content_type_headers == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                content_type = 'DOCX'
            elif content_type_headers == 'application/pdf':
                content_type = 'PDF'
        pageID = db.insertPage(siteID, page_type_code, canonicalUrl(currentPageLink[0]), html_content,
                               htmlStatusCode, datetime.now(), html_hash)
        if currentPageLink[1] != 0:
            db.insertLink(currentPageLink[1], pageID)
        if page_type_code == 'BINARY':
            if content_type != '/':
                db.insertPageData(pageID, content_type)
            currentPageLink = fr.getUrl()
            continue
    else:
        pageID = db.insertPage(siteID, 'DUPLICATE', canonicalUrl(currentPageLink[0]), html_content,
                               htmlStatusCode, datetime.now(), html_hash)
        if currentPageLink[1] != 0:
            db.insertLink(currentPageLink[1], pageID)
        db.insertLink(pageID, hashPageId)
        currentPageLink = fr.getUrl()
        continue

    linkovi = soup.find_all('a', href=True)
    sliki = soup.find_all('img', src=True)

    # ovaj for e za linkovi
    for lnk in linkovi: ################## smeni da gi pomini site ############################
        # if the link is not empty add the link to the database
        if '.jpg' in lnk['href'] or '.png' in lnk['href'] or '.jpeg' in lnk['href'] or '.svg' in lnk['href'] \
                or '.gif' in lnk['href'] or '.avif' in lnk['href'] or '.apng' in lnk['href'] \
                or '.wbep' in lnk['href'] or '.pjp' in lnk['href'] or '.jfif' in lnk['href']:
            continue
        if lnk['href'] != '/':
            if (lnk['href']).startswith('http'):
                fr.addUrl(lnk['href'], pageID)
            else:
                # 'https://' + 'www.gov.si' + '/pomoc/
                fr.addUrl('http://' + domain + lnk['href'], pageID)

    # ovaj for e za sliki
    for sl in sliki[1:10]: ################## smeni da gi pomini site ############################
        if sl['src'] != '/': # if the img is not empty add the img to the database
            if (sl['src']).startswith('http') or (sl['src']).startswith('data'):
                pictureLink = sl['src']
            elif (sl['src']).startswith('/' + domain):
                pictureLink = 'http:/' + sl['src']
            elif not (sl['src']).startswith('/'):
                pictureLink = 'http://' + domain + '/' + sl['src']
            else:
                # 'https://' + 'www.gov.si' + '/pomoc/
                pictureLink = 'http://' + domain + sl['src']

            print(pictureLink)
            a = urlparse(pictureLink)
            filename = os.path.basename(a.path)

            content_type = "/"
            if filename.__contains__('.'):
                content_type_table = filename.split(".")
                content_type = content_type_table[len(content_type_table)-1]

            try:
                data = urlopen(pictureLink).read()
                db.insertImage(pageID, filename, content_type, data, datetime.now())
            except Exception:
                print('TIMEOUT ERROR OR SKIPPED A PICTURE WITH A BAD URL')

    currentPageLink = fr.getUrl() # ova posledno za da zemi strana od pocetoko




###################### STA NAMA OBIDZUKOVCI FALI (OSIM MOZAK I NERVE) ##########################
# 1. status code (page tabela) - ne raboti ko ce e 404 error i taka natamu  (PITAJ ASISTENT)
# 2. (luksuz) povekje roboti da rabotat istovremeno  // NE E NAPRAVENO
# 3. (luksuz) za da ne go preopteretuvame servero TIMEOUT  // VALJDA E OK
# 4. (luksuz) agent so imeto obidzuko   OK

######################## prasanja koi ne' macat ########################
# 1. Error so imame ako moze da se resi
# 2. Status code imame samo 200, dali e ok, dali treba drugite da se zacuvat?
# 3. Binary nemame seuste nikade....
# 4. Kolku roboti e pametno da se napravat koga ke se napravi konecen run
# 5. So ako dojdi zip link? Dali da se preripuva?