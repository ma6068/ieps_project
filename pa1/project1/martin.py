from urllib.request import urlopen, Request

f = urlopen(Request('https://www.gov.si/', headers={'User-Agent': 'fri-wier-obidzuko'}), timeout=10)
page = f.read().decode('utf-8')

htmlStatusCode = f.getcode()
html_content = f.read()
print(html_content)
info = f.info()
a = info.get_content_type()