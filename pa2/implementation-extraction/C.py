
from bs4 import BeautifulSoup

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

    page1Elemenets = []
    for tag in allElements1:
        if tag.name == 'p' or tag.name == 'div' or tag.name == 'h1' or tag.name == 'title' or tag.name == 'table':
            print(str(tag).splitlines()[0])

    # page2Elemenets = []
    # for tag in allElements2:
    #    if tag.name == 'p' or tag.name == 'div' or tag.name == 'h1' or tag.name == 'title' or tag.name == 'table':
    #        page2Elemenets.append(tag.name)



def implementationC(pages):
    webExtraction(pages[1], pages[2])
#    webExtraction(pages[3], pages[4])
#    webExtraction(pages[5], pages[6])