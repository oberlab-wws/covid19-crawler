from .Covid19Crawler import Covid19Crawler

class CACrawler(Covid19Crawler):
    def __init__(self, urls_tested = list(), urls_positive = list(), urls_deaths = list()):
        kwargs = {
                'urls_tested': urls_tested,
                'urls_positive': urls_positive,
                'urls_deaths': urls_deaths
            }
        super().__init__(state = 'CA', **kwargs)

    def crawl(self):
        print('crawling {}'.format(self.state))
