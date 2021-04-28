import json
import re


def regularniIzrazi(path, pageType):

    page = open(path, 'rb').read()
    try:
        page = str(page, "utf-8")
    except (UnicodeDecodeError, AttributeError):
        try:
            page = str(page)
        except (UnicodeDecodeError, AttributeError):
            pass

    if pageType == 'rtv':
        author = re.search("<div class=\"author-name\">([^<]*)</div>", page).group(1)
        publishMeta = re.search("<div class=\"publish-meta\">\\s*([^<]*)<br>\\s*([^<]*)\\s*</div>", page)
        timePublished = publishMeta.group(1)
        placePublished = re.sub('\s\s*', ' ', publishMeta.group(2))
        title = re.search("<h1>([^<]*)</h1>", page).group(1)
        subtitle = re.search("<div class=\"subtitle\">([^<]*)</div>", page).group(1)
        lead = re.search("<p class=\"lead\">([^<]*)</p>", page).group(1)
        content = re.findall('<article class=\"article\">(.+?)</article>', page, flags=re.DOTALL)
        c = ''
        for e in content:
            c = re.sub('<figure.*?</figure>', '', e, flags=re.DOTALL)
            c = re.sub('<.*?>', '', c)
        lines = c.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]
        string_without_empty_lines = ""
        for line in non_empty_lines:
            string_without_empty_lines += line
        content = string_without_empty_lines

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
        title = re.findall("PROD_ID[^>]*><b>([^<]*)</b>", page)
        title = [el.replace('\\', '') for el in title]
        list_price = re.findall("List Price:</b></td><td align=\"left\" nowrap=\"nowrap\"><s>([^<]*)</s>", page)
        price = re.findall("Price:</b></td><td align=\"left\" nowrap=\"nowrap\"><span class=\"bigred\"><b>([^<]*)</b>", page)
        you_save = re.findall("You Save:</b></td><td align=\"left\" nowrap=\"nowrap\"><span class=\"littleorange\">([^<]*) ([^<]*)</span>", page)
        saving = []
        saving_percent = []
        for el in you_save:
            saving.append(el[0])
            saving_percent.append(el[1])
        content = re.findall("span class=\"normal\">([^<]*)<br>", page)
        content = [el.replace('\\r\\n', ' ').replace('\\', '') for el in content]

        for i in range(0, len(title)):
            jsonData = dict()
            jsonData['title'] = title[i]
            jsonData['list_price'] = list_price[i]
            jsonData['price'] = price[i]
            jsonData['saving'] = saving[i]
            jsonData['saving_percent'] = saving_percent[i]
            jsonData['content'] = content[i]
            print(json.dumps(jsonData, ensure_ascii=False))

    elif pageType == 'npr':
        cena = re.findall("<span class=\"cena\">([^<]*)</span>", page)
        agencija = re.findall("<span class=\"agencija\">([^<]*)</span>", page)
        velikost = re.findall("<span class=\"velikost\" lang=\"sl\">([^<]*)</span>", page)
        district = re.findall("<span class=\"title\">([^<]*)</span>", page)
        desc = re.findall("<div class=\"kratek\" (itemprop|itemqrop)=\"description\">([^<]*)</div>", page)
        leto = re.findall("<span class=\"atribut leto\">Leto: <strong>([^<]*)</strong></span>", page)
        title = re.findall("<span class=\"vrsta\">([^<]*)</span>", page)
        slika = re.findall("<img class=\"(lazyload|lazyloaded| lazyload| lazyloaded)\" data-src=\"([^\"]*)\"", page)

        for i in range(0, len(title)):
            jsonData = dict()
            jsonData['cena'] = cena[i]
            jsonData['agencija'] = agencija[i]
            jsonData['velikost'] = velikost[i]
            jsonData['district'] = district[i]
            jsonData['desc'] = desc[i][1]
            jsonData['leto'] = leto[i]
            jsonData['title'] = title[i]
            jsonData['slika'] = slika[i][1]
            print(json.dumps(jsonData, ensure_ascii=False))


def implementationA(pages):
    print("-------------------------  RTV SITE 1  --------------------------------------\n")
    regularniIzrazi(pages[0], 'rtv')
    print("\n-------------------------  RTV SITE 2  --------------------------------------\n")
    regularniIzrazi(pages[1], 'rtv')
    print("\n-------------------------  Overstock SITE 1  --------------------------------------\n")
    regularniIzrazi(pages[2], 'ovr')
    print("\n-------------------------  Overstock SITE 2  --------------------------------------\n")
    regularniIzrazi(pages[3], 'ovr')
    print("\n-------------------------  Nepremicnine SITE 1  --------------------------------------\n")
    regularniIzrazi(pages[4], 'npr')
    print("\n-------------------------  Nepremicnine SITE 2  --------------------------------------\n")
    regularniIzrazi(pages[5], 'npr')
