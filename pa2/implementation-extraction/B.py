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
        #content = re.findall("<p[^>]*>([^<]*)</p>.*", page)
        #content = " ".join(content)

        jsonData = dict()
        jsonData['author'] = author
        jsonData['timePublished'] = timePublished
        jsonData['placePublished'] = placePublished
        jsonData['title'] = title
        jsonData['subtitle'] = subtitle
        jsonData['lead'] = lead
        print(json.dumps(jsonData))

    elif pageType == 'ovr':
        print("OVR")

    elif pageType == 'npr':
        print("NPR")

def implementationB(pages):

    xpathIzrazi(pages[0], 'rtv')
    xpathIzrazi(pages[1], 'rtv')
#    xpathIzrazi(pages[2], 'ovr')
#    xpathIzrazi(pages[3], 'ovr')
#    xpathIzrazi(pages[4], 'nep')
#    xpathIzrazi(pages[5], 'nep')