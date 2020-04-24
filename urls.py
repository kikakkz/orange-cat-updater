from url import Url


class Urls:
    def __init__(self, urls):
        self.urls = []
        for url in urls:
            self.urls.append(Url(url))

    def source_urls(self):
        return self.urls
