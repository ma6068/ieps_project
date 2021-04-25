import re

from bs4 import BeautifulSoup

def comparePageElements(page1Elemenets, page2Elemenets, i, j):

    # napravi eden for koj pominuva niz sekoj element za prva strana
    # ako najdi ist element so ist ID togas to e to skokni gi prethodnite elementi
    # ako ne najdi ist element togas sporedi gi elementite so drugiot for
    # (verojatno elementot na koj so sme ne e dobar)
    for k in range(i, len(page1Elemenets)):
        if(page1Elemenets[k] == page2Elemenets[j]):
            return k, j

    # napravi eden for koj pominuva niz sekoj element za vtora strana
    # ako najdi ist element so ist ID togas to e to skokni gi prethodnite elementi
    # ako ne najdi ist element vo dvata slucai, togas dvata elementi izbrisi gi
    # (verojatno dvata elementi se razlicni i treba  da se skoknat)
    for l in range(j, len(page2Elemenets)):
        if(page1Elemenets[i] == page2Elemenets[l]):
            return i, l

    return -1, -1

def webExtraction(path1, path2):
    page1 = open(path1, 'rb').read()
    try:
        page1 = str(page1, "utf-8")
    except (UnicodeDecodeError, AttributeError):
        try:
            page1 = str(page1)
        except (UnicodeDecodeError, AttributeError):
            pass

    page2 = open(path2, 'rb').read()
    try:
        page2 = str(page2, "utf-8")
    except (UnicodeDecodeError, AttributeError):
        try:
            page2 = str(page2)
        except (UnicodeDecodeError, AttributeError):
            pass

    allElements1 = re.findall(r'<[^>]+>', page1)
    allElements2 = re.findall(r'<[^>]+>', page2)

    page1Elemenets = []
    for tag in allElements1:
        if tag.startswith('<p') or tag.startswith('< p') \
                or tag.startswith('<div') or tag.startswith('< div') \
                or tag.startswith('<h1') or tag.startswith('< h1') \
                or tag.startswith('<title') or tag.startswith('< title') \
                or tag.startswith('<table') or tag.startswith('< table'):
            page1Elemenets.append(tag)

    page2Elemenets = []
    for tag in allElements2:
        if tag.startswith('<p') or tag.startswith('< p') \
                or tag.startswith('<div') or tag.startswith('< div') \
                or tag.startswith('<h1') or tag.startswith('< h1') \
                or tag.startswith('<title') or tag.startswith('< title') \
                or tag.startswith('<table') or tag.startswith('< table'):
            # page2Elemenets.append(str(tag).splitlines()[0])
            page2Elemenets.append(tag)

    combinedElements = []
    j = 0
    i = 0
    while i < len(page1Elemenets) and j < len(page2Elemenets):
        if page1Elemenets[i] == page2Elemenets[j]:
            combinedElements.append(page1Elemenets[i])
            i += 1
            j += 1
            continue

        k, l = comparePageElements(page1Elemenets, page2Elemenets, i, j)
        if k >= 0:
            combinedElements.append(page1Elemenets[i])
            i = k
            j = l
        i += 1
        j += 1
    # print(combinedElements)
    # print(page2Elemenets)
    # for i in range(10):
    #     print(page2Elemenets[i])
    #     print("--------------------------------------------")


def implementationC(pages):
    webExtraction(pages[0], pages[1])
#    webExtraction(pages[2], pages[3])
#    webExtraction(pages[4], pages[5])

#div 1
#div 2
#div 3

#div 1
#div 5
#div 4
#div 2
#div 3
