import hashlib
import os
import threading
import time
from urllib.request import urlopen, Request
from datetime import datetime
import requests
from url_normalize import url_normalize

import urllib.robotparser
from bs4 import BeautifulSoup

from urllib.error import HTTPError
from urllib.parse import urlparse, urlsplit, urljoin
import urllib


class MainCrawler:

    def __init__(self, db=None, fr=None, robotPages=None, thisIsCrawlerNumber=None):
        self.db = db
        self.fr = fr
        self.robotPages = robotPages
        self.thisIsCrawlerNumber = thisIsCrawlerNumber

    def startThread(self):
        self.thread = threading.Thread(target=self.mainFunction)
        self.thread.setDaemon(True)
        self.thread.start()
        return self.thread

    def timePassed(self, prevTime):
        return time.time() - prevTime >= 5

    def canonicalUrl(self, url):
        splited = '{uri.scheme}://{uri.netloc}/'.format(uri=urlsplit(url))
        return url_normalize(urljoin(splited, url))

    def takeAllRobotPages(self, robotText, domain):
        a = robotText.split("\n")[0]
        if "*" in a or "fri-wier-obidzuko" in a:
            for line in robotText.split("\n"):
                if line.startswith('Disallow'):  # this is for disallowed url
                    self.robotPages.append('http://' + domain + line.split(': ')[1].split(' ')[0])

    def mainFunction(self):
        currentPageLink = self.fr.getUrl()
        currentTime = time.time()

        while currentPageLink is not None:
            print(str(self.thisIsCrawlerNumber) + ', CURRENT PAGE: ' + currentPageLink[0])
            if self.timePassed(currentTime):
                time.sleep(1)

            # probaj da ja otvoris narednata strana so e na red
            try:
                f = urlopen(Request(currentPageLink[0], headers={'User-Agent': 'fri-wier-obidzuko'}), timeout=10)
                currentTime = time.time()
            except HTTPError as httperror:
                print(str(self.thisIsCrawlerNumber) + ', STATUS CODE ERROR !!!!!!')
                print(str(self.thisIsCrawlerNumber) + str(httperror.getcode()))
                pageId = self.db.insertPage(None, None, currentPageLink[0], None, httperror.getcode(), datetime.now(), None)
                self.db.insertLink(currentPageLink[1], pageId)
                currentPageLink = self.fr.getUrl()
                continue
            except Exception:
                # vo slucaj da e nekoj los link, zemame link od druga strana i odime od pocetok
                print(str(self.thisIsCrawlerNumber) + ', ERROR: THIS PAGE DOES NOT EXIST')
                currentPageLink = self.fr.getUrl()
                continue

            # ova mora zaradi preusmeruvanje, koga sme preusmereni proveruvame na koj link sme sega
            # ako sme preusmereni ova ce go daj tocnio, toj koj so se koristi, i se e bez problem
            currentPageLink[0] = f.url

            print(str(self.thisIsCrawlerNumber) + ', CHANGED PAGE: ' + currentPageLink[0])
            # ako e zabraneto (robots.txt) zemi naredna strana
            if currentPageLink[0] in self.robotPages:
                currentPageLink = self.fr.getUrl()
                continue

            # ovoj url veke go imame vo bazata => zemi nareden
            if self.db.getPageByUrl(self.canonicalUrl(currentPageLink[0])) is not None:
                currentPageLink = self.fr.getUrl()
                continue

            if '.zip' in currentPageLink[0]:
                currentPageLink = self.fr.getUrl()
                continue

            domain = urlparse(currentPageLink[0]).netloc # dava primer www.gov.si -> mora https://......../pomoc/
            if ".gov.si" not in domain:
                currentPageLink = self.fr.getUrl()
                continue
            print(str(self.thisIsCrawlerNumber) + ', DOMAIN: ' + domain)

            info = f.info()
            page_type_code = info.get_content_type()
            print(str(self.thisIsCrawlerNumber) + page_type_code)
            htmlStatusCode = f.getcode()
            if page_type_code == 'text/html':
                page = f.read().decode('utf-8')
                soup = BeautifulSoup(page)
                html_content = page
                hash_object = hashlib.sha256(html_content.encode())
                html_hash = hash_object.hexdigest()

                # gledame dali toj page e duplikat
                hashPageId = self.db.getPageByHash(html_hash)
            else:
                hashPageId = None
                html_content = None
                html_hash = None

            # gledame dali sme na istiot domain, ako ne sme => dodadi nov site
            siteID = self.db.getSiteByDomain(domain)
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
                        self.takeAllRobotPages(robotText, domain)
                        print(str(self.thisIsCrawlerNumber) + self.robotPages)
                    if robotFile.site_maps():
                        siteText = str("\n".join(robotFile.site_maps()))
                except Exception:
                    robotText = None
                    siteText = None
                    print(str(self.thisIsCrawlerNumber) + ', EXCEPTION WHILE CREATING ROBOT')

                siteID = self.db.insertSite(domain, robotText, siteText)

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
                pageID = self.db.insertPage(siteID, page_type_code, self.canonicalUrl(currentPageLink[0]), html_content,
                                       htmlStatusCode, datetime.now(), html_hash)
                if currentPageLink[1] != 0:
                    self.db.insertLink(currentPageLink[1], pageID)
                if page_type_code == 'BINARY':
                    if content_type != '/':
                        self.db.insertPageData(pageID, content_type)
                    currentPageLink = self.fr.getUrl()
                    continue
            else:
                pageID = self.db.insertPage(siteID, 'DUPLICATE', self.canonicalUrl(currentPageLink[0]), html_content,
                                       htmlStatusCode, datetime.now(), html_hash)
                if currentPageLink[1] != 0:
                    self.db.insertLink(currentPageLink[1], pageID)
                self.db.insertLink(pageID, hashPageId)
                currentPageLink = self.fr.getUrl()
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
                        self.fr.addUrl(lnk['href'], pageID)
                    else:
                        # 'https://' + 'www.gov.si' + '/pomoc/
                        self.fr.addUrl('http://' + domain + lnk['href'], pageID)

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

                    print(str(self.thisIsCrawlerNumber) + pictureLink)
                    a = urlparse(pictureLink)
                    filename = os.path.basename(a.path)

                    content_type = "/"
                    if filename.__contains__('.'):
                        content_type_table = filename.split(".")
                        content_type = content_type_table[len(content_type_table)-1]

                    try:
                        data = urlopen(pictureLink).read()
                        self.db.insertImage(pageID, filename, content_type, data, datetime.now())
                    except Exception:
                        print(str(self.thisIsCrawlerNumber) + ', TIMEOUT ERROR OR SKIPPED A PICTURE WITH A BAD URL')

            currentPageLink = self.fr.getUrl() # ova posledno za da zemi strana od pocetoko




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