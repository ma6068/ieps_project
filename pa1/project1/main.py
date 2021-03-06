import urllib.request
from bs4 import BeautifulSoup

f = urllib.request.urlopen('http://www.gov.si')

page = f.read().decode('utf-8')

links = ['http://www.gov.si', 'http://www.evem.gov.si', 'http://www.e-uprava.gov.si', 'http://www.e-prostor.gov.si']

soup = BeautifulSoup(page)

linkovi = soup.find_all('a', href=True)

for lnk in linkovi[1:10]:
    print(lnk)