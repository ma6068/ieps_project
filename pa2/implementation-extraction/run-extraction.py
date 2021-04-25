import sys

import A as a
import B as b
import C as c



pages = ['../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html',
         '../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljs╠îe v razredu - RTVSLO.si.html',
         '../input-extraction/overstock.com/jewelry01.html',
         '../input-extraction/overstock.com/jewelry02.html',
         '../input-extraction/nepremicnine.net/stanovanje.html',
         '../input-extraction/nepremicnine.net/hisaa.html']

typeOfImplementation = sys.argv[1]

if typeOfImplementation == 'A':
    a.implementationA(pages)
elif typeOfImplementation == 'B':
    b.implementationB(pages)
elif typeOfImplementation == 'C':
    c.implementationC(pages)
else:
    print("Wrong implementation!")