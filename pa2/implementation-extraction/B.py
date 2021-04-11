import json
import re

from lxml import etree, html


def xpathIzrazi(path, pageType):

    page = open(path, 'rb').read()
    try:
        page = str(page, "utf-8")
    except (UnicodeDecodeError, AttributeError):
        try:
            page = str(page)
        except (UnicodeDecodeError, AttributeError):
            pass

    if pageType == 'rtv':
        tree = html.fromstring(page)
        author = tree.xpath("//div[@class='author-name']/text()")[0]
        publishMeta = tree.xpath("//div[@class='publish-meta']/text()")
        timePublished = re.sub('\s\s*', ' ', publishMeta[0])
        placePublished = re.sub('\s\s*', ' ', publishMeta[1])
        title = tree.xpath("//h1/text()")[0]
        subtitle = tree.xpath("//div[@class='subtitle']/text()")[0]
        lead = tree.xpath("//p[@class='lead']/text()")[0]
        multipleContents = tree.xpath("//article[@class='article']/p//text()")
        content = multipleContents[0]
        for i in range(1, len(multipleContents)):
            content = content + '\n' + multipleContents[i]

        jsonData = dict()
        jsonData['author'] = author
        jsonData['timePublished'] = timePublished
        jsonData['placePublished'] = placePublished
        jsonData['title'] = title
        jsonData['subtitle'] = subtitle
        jsonData['lead'] = lead
        jsonData['content'] = content
        print(json.dumps(jsonData))

    elif pageType == 'ovr':
        tree = html.fromstring(page)
        title = tree.xpath(
            "//table[2]//tr[1]/td[5]/table//tr[2]/td/table//tr/td/table//tr[@bgcolor]/td[2]/a//text()")
        list_price = tree.xpath(
            "//table[2]//tr[1]/td[5]/table//tr[2]/td/table//tr/td/table//tr[@bgcolor]/"
            "td[2]/table//table//tr[1]/td[2]//text()")
        price = tree.xpath(
            "//table[2]//tr[1]/td[5]/table//tr[2]/td/table//tr/td/table//tr[@bgcolor]/"
            "td[2]/table//table//tr[2]/td[2]//text()")
        you_save = tree.xpath(
            "//table[2]//tr[1]/td[5]/table//tr[2]/td/table//tr/td/table//tr[@bgcolor]/"
            "td[2]/table//table//tr[3]/td[2]//text()")
        content = tree.xpath("//table[2]//tr[1]/td[5]/table//tr[2]/td/table//tr/td/table//tr[@bgcolor]/"
                             "td[2]/table/tbody/tr/td[2]//text()")
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
            jsonData['content'] = content
            print(json.dumps(jsonData))

    elif pageType == 'npr':
        print("NPR")

def implementationB(pages):
    # xpathIzrazi(pages[0], 'rtv')
    # xpathIzrazi(pages[1], 'rtv')
    xpathIzrazi(pages[2], 'ovr')
    # xpathIzrazi(pages[3], 'ovr')
    # xpathIzrazi(pages[4], 'nep')
    # xpathIzrazi(pages[5], 'nep')