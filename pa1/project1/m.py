
from urllib.parse import urljoin,urlsplit,urlparse

from url_normalize import url_normalize
import os
from datetime import datetime
from urllib.request import urlopen

def canonicalUrl(url):
    splited =  '{uri.scheme}://{uri.netloc}/'.format(uri=urlsplit(url))

    return url_normalize(urljoin(splited, url))

if __name__ == "__main__":
    # print(canonicalUrl("www.foo.com:80/foo"))
    # print(canonicalUrl("http://example.com/dir/../../thing/."))


    # image
    url = "https://www.planetware.com/wpimages/2019/11/canada-in-pictures-beautiful-places-to-photograph-morraine-lake.jpg"
    a = urlparse(url)
    filename = os.path.basename(a.path)
    # print(filename)
    content_type = "/"
    if filename.__contains__("."):
        content_type_table = filename.split(".")
        content_type = content_type_table[len(content_type_table)-1]
    # print(content_type)

    data = urlopen(url).read()
    # print(data)

    db.insertImage(pageID, filename, content_type, data, datetime.now())






