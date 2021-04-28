import re
from difflib import SequenceMatcher
from bs4 import BeautifulSoup

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

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

    soup1 = BeautifulSoup(page1)
    soup2 = BeautifulSoup(page2)

    allElements1 = soup1.findAll(True)
    allElements2 = soup2.findAll(True)

    page1Names = []
    page1Elemenets = []
    for tag in allElements1:
        if tag.name == 'p' or tag.name == 'div' or tag.name == 'h1' or tag.name == 'title' or tag.name == 'table':
            page1Names.append(tag.name)
            page1Elemenets.append(tag)

    page2Names = []
    page2Elemenets = []
    for tag in allElements2:
       if tag.name == 'p' or tag.name == 'div' or tag.name == 'h1' or tag.name == 'title' or tag.name == 'table':
           page2Names.append(tag.name)
           page2Elemenets.append(tag)

    LayoutElements1 = []
    LayoutElements2 = []
    j = 0
    i = 0
    while i < len(page1Names) and j < len(page2Names):
        if page1Names[i] == page2Names[j]:
            LayoutElements1.append(page1Elemenets[i])
            LayoutElements2.append(page2Elemenets[j])
            i += 1
            j += 1
            continue

        k, l = comparePageElements(page1Names, page2Names, i, j)
        if k >= 0:
            i = k
            j = l
            LayoutElements1.append(page1Elemenets[i])
            LayoutElements2.append(page2Elemenets[j])
        i += 1
        j += 1

    # We have our layout pattern, now we need to take all elements with that
    # pattern and check their similarity (difference)
    diffElements1 = []
    diffElements2 = []
    for i in range(len(LayoutElements1)):
        if similar(str(LayoutElements1[i]), str(LayoutElements2[i])) < 0.5:
            diffElements1.append(LayoutElements1[i])
            diffElements2.append(LayoutElements2[i])

    print(diffElements1)
    print(diffElements2)


def implementationC(pages):
    webExtraction(pages[0], pages[1])
    webExtraction(pages[2], pages[3])
    webExtraction(pages[4], pages[5])