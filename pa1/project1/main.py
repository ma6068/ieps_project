from pip._vendor.distlib.compat import raw_input

from crawler import MainCrawler
from frontier import Frontier
import database.db as database
import sys

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
    crawler = MainCrawler(db, fr, robotPages, i) # na mestoto od main prajme instanca na novata klasa kaj so ke e crawlerot
    threads.append(crawler)
    crawler.mainFunction()

while True:
    crawlersRunning = False

    for i in threads:
        crawlersRunning = i.thread.is_alive()
        if crawlersRunning:
            break

    if not crawlersRunning:
        break
