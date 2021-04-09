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

        # Regularni izrazi
        author = re.search("<div class=\"author-name\">([^<]*)</div>", page).group(1)
        publishMeta = re.search("<div class=\"publish-meta\">\\s*([^<]*)<br>\\s*([^<]*)\\s*</div>", page)
        timePublished = publishMeta.group(1)
        placePublished = re.sub('\s\s+', ' ', publishMeta.group(2))
        title = re.search("<h1>([^<]*)</h1>", page).group(1)
        subtitle = re.search("<div class=\"subtitle\">([^<]*)</div>", page).group(1)
        lead = re.search("<p class=\"lead\">([^<]*)</p>", page).group(1)
        content = re.findall("<p[^>]*>([^<]*)</p>.*", page)
        content = " ".join(content)
        print(content)

    elif pageType == 'ovr':

        title = re.findall("PROD_ID[^>]*><b>([^<]*)</b>", page)

        list_price = re.findall("List Price:</b></td><td align=\"left\" nowrap=\"nowrap\"><s>([^<]*)</s>", page)

        price = re.findall("Price:</b></td><td align=\"left\" nowrap=\"nowrap\"><span class=\"bigred\"><b>([^<]*)</b>", page)

        you_save = re.findall("You Save:</b></td><td align=\"left\" nowrap=\"nowrap\"><span class=\"littleorange\">([^<]*) ([^<]*)</span>", page)
        saving = []
        saving_percent = []
        for el in you_save:
            saving.append(el[0])
            saving_percent.append(el[1])

        content = re.findall("class=\"normal\">([^<]*)<br>", page)
        print(price)

    elif pageType == 'npr':
        print("NEPREMICNINE")


def implementationA(pages):
    regularniIzrazi(pages[0], 'rtv')
#    regularniIzrazi(pages[1], 'rtv')
#    regularniIzrazi(pages[2], 'ovr')
#    regularniIzrazi(pages[3], 'ovr')
#    regularniIzrazi(pages[4], 'nep')
#    regularniIzrazi(pages[5], 'nep')