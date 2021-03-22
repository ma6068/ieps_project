
from urllib.parse import urljoin,urlsplit

from url_normalize import url_normalize

def canonicalUrl(url):
    splited =  '{uri.scheme}://{uri.netloc}/'.format(uri=urlsplit(url))

    return url_normalize(urljoin(splited, url))

if __name__ == "__main__":
    print(canonicalUrl("www.foo.com:80/foo"))
    print(canonicalUrl("http://example.com/dir/../../thing/."))






