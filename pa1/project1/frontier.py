class Frontier:
    def __init__(self):
        self.frontier = []

    def addUrl(self, url, parentId):
        self.frontier.append([url, parentId])

    def getUrl(self):
        if not self.frontier:
            return None
        else:
            element = self.frontier[0]
            self.frontier.pop(0)
            return element
