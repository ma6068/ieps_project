import codecs
import re
from bs4 import BeautifulSoup

path = "../WebPages/overstock.com/jewelry02.html"

page = open(path, 'rb').read()
try:
    page = str(page, "utf-8")
except (UnicodeDecodeError, AttributeError):
    try:
        page = str(page)
    except (UnicodeDecodeError, AttributeError):
        pass

title = re.findall("PROD_ID[^>]*><b>([^<]*)</b>", page)
print(title)

list_price = re.findall("List Price:</b></td><td align=\"left\" nowrap=\"nowrap\"><s>([^<]*)</s>", page)
print(list_price)

price = re.findall("Price:</b></td><td align=\"left\" nowrap=\"nowrap\"><span class=\"bigred\"><b>([^<]*)</b>", page)
print(price)

you_save = re.findall("You Save:</b></td><td align=\"left\" nowrap=\"nowrap\"><span class=\"littleorange\">([^<]*) ([^<]*)</span>", page)
saving = []
saving_percent = []
for el in you_save:
    saving.append(el[0])
    saving_percent.append(el[1])
print(saving)
print(saving_percent)

content = re.findall("class=\"normal\">([^<]*)<br>", page)
print(content)
