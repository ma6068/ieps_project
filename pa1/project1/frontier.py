import collections


class Frontier:
    def __init__(self, startUrls=None):
        if not startUrls:
            self.frontier = []
        else:
            self.frontier = startUrls.copy()

    def addUrl(self, url):
        self.frontier.append(url)

    def getUrl(self):
        if not self.frontier:
            return None
        else:
            nextUrl = self.frontier[0]
            self.frontier.pop(0)
            return nextUrl

    def duplicates(self):
        return [item for item, count in collections.Counter(self.frontier).items() if count > 1]
