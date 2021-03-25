from time import sleep

from pip._vendor.distlib.compat import raw_input

from crawler import MainCrawler
from frontier import Frontier
import database.db as database

db = database.DB()
db.connectDB()
db.createTables()

robotPages = []

fr = Frontier()
fr.addUrl('http://www.gov.si/', 0)
fr.addUrl('http://evem.gov.si/', 0)
fr.addUrl('http://e-uprava.gov.si/', 0)
fr.addUrl('http://e-prostor.gov.si/', 0)

txt = raw_input('Please enter the number of crawlers you would like to use simultaneously: ')
noCrawlers = int(txt)
threads = list()

for i in range(noCrawlers):
    print(i)
    crawler = MainCrawler(db=db, fr=fr, robotPages=robotPages, thisIsCrawlerNumber=i)
    threads.append(crawler)
    crawler.startThread()
    sleep(1)

while True:
    crawlersRunning = False

    for i in threads:
        crawlersRunning = i.thread.is_alive()
        if crawlersRunning:
            break

    if not crawlersRunning:
        break
