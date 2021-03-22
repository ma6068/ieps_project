# da dostopuva ednska vo 5 sekundi se pravi so sleep i vreme da se oznaci koga ima dostop

text = '''User-agent: *
Disallow: /admin 
Disallow: /resources 
Disallow: /pomoc'''

robotPages = []


def takeAllRobotPages(robotText):
    r = []
    for line in robotText.split("\n"):
        if line.startswith('Disallow'):  # this is for disallowed url
            r.append(line.split(': ')[1].split(' ')[0])
    return r


print(takeAllRobotPages(text))

a = [1, 2, 3]
b = [2, 3, 3]
c = a + b
print(c)

