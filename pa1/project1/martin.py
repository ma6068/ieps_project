from urllib.error import HTTPError
from pip._vendor import requests

try:
    r = requests.get('https://www.gov.si/')
    content_type = r.headers['content-type']
    print(content_type)
    if "html" in content_type:
        print("da")
except HTTPError:
    print('ERROR: THIS PAGE DOES NOT EXIST')