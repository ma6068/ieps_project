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
            content = content + ' ' + multipleContents[i]

        jsonData = dict()
        jsonData['author'] = author
        jsonData['timePublished'] = timePublished
        jsonData['placePublished'] = placePublished
        jsonData['title'] = title
        jsonData['subtitle'] = subtitle
        jsonData['lead'] = lead
        jsonData['content'] = content
        print(json.dumps(jsonData, ensure_ascii=False))

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
        cont = tree.xpath("//table[2]//tr[1]/td[5]/table//tr[2]/td/table//tr/td/table//tr[@bgcolor]/"
                             "td[2]/table/tbody/tr/td[2]//text()")
        content = []
        for i in range(0, len(cont), 3):
            c = cont[i] + " " + cont[i+1]
            c = c.replace('\\r\\n', ' ').replace('\\', '').replace('  ', ' ')
            content.append(c)

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
            print(json.dumps(jsonData, ensure_ascii=False))

    elif pageType == 'npr':
        tree = html.fromstring(page)
        cena = tree.xpath("//span[@class='cena']/text()")
        agencija = tree.xpath("//span[@class='agencija']/text()")
        velikost = tree.xpath("//span[@class='velikost']/text()")
        district = tree.xpath("//span[@class='title']/text()")
        desc = tree.xpath("//div[@class='kratek']/text()")
        leto = tree.xpath("//span[@class='atribut leto']/strong/text()")
        title = tree.xpath("//span[@class='vrsta']/text()")
        slika = tree.xpath("//img[@class='lazyload']/@data-src | //img[@class=' lazyload']/@data-src | //img[@class='lazyloaded']/@data-src | //img[@class=' lazyloaded']/@data-src")

        for i in range(0, len(title)):
            jsonData = dict()
            jsonData['cena'] = cena[i]
            jsonData['agencija'] = agencija[i]
            jsonData['velikost'] = velikost[i]
            jsonData['district'] = district[i]
            jsonData['desc'] = desc[i]
            jsonData['leto'] = leto[i]
            jsonData['title'] = title[i]
            jsonData['slika'] = slika[i]
            print(json.dumps(jsonData, ensure_ascii=False))


def implementationB(pages):
    print("-------------------------  RTV 1 STRAN  --------------------------------------\n")
    xpathIzrazi(pages[0], 'rtv')
    print("\n-------------------------  RTV 2 STRAN  --------------------------------------\n")
    xpathIzrazi(pages[1], 'rtv')
    print("\n-------------------------  Overstock 1 STRAN  --------------------------------------\n")
    xpathIzrazi(pages[2], 'ovr')
    print("\n-------------------------  Overstock 2 STRAN  --------------------------------------\n")
    xpathIzrazi(pages[3], 'ovr')
    print("\n-------------------------  Nepremicnine 1 STRAN  --------------------------------------\n")
    xpathIzrazi(pages[4], 'npr')
    print("\n-------------------------  Nepremicnine 2 STRAN  --------------------------------------\n")
    xpathIzrazi(pages[5], 'npr')
