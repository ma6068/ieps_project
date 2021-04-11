import json
import re

from lxml import html

path = "../input-extraction/overstock.com/jewelry01.html"

page = open(path, 'rb').read()
try:
    page = str(page, "utf-8")
except (UnicodeDecodeError, AttributeError):
    try:
        page = str(page)
    except (UnicodeDecodeError, AttributeError):
        pass

tree = html.fromstring(page)
title = tree.xpath(
    "//table[2]//tr[1]/td[5]/table//tr[2]/td/table//tr/td/table//tr[@bgcolor]/td[2]/a//text()")
list_price = tree.xpath(
    "//table[2]//tr[1]/td[5]/table//tr[2]/td/table//tr/td/table//tr[@bgcolor]/"
    "td[2]/table//table//tr[1]/td[2]//text()")
price = tree.xpath(
    "//table[2]//tr[1]/td[5]/table//tr[2]/td/table//tr/td/table//tr[@bgcolor]/td[2]/table//table//tr[2]/td[2]//text()")
you_save = tree.xpath(
    "//table[2]//tr[1]/td[5]/table//tr[2]/td/table//tr/td/table//tr[@bgcolor]/td[2]/table//table//tr[3]/td[2]//text()")

saving = []
saving_percent = []
for el in you_save:
    x = el.split()
    saving.append(x[0])
    saving_percent.append(x[1])

for i in range(0, len(title)):
    jsonData = dict()
    jsonData['title'] = title[i]
    jsonData['list_price'] = list_price[i]
    jsonData['price'] = price[i]
    jsonData['saving'] = saving[i]
    jsonData['saving_percent'] = saving_percent[i]
    print(json.dumps(jsonData))

