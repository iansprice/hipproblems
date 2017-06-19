from tornado import gen, ioloop, web, httpserver
from hotel_search.scrapers import get_scraper


class ScraperApiHandler(web.RequestHandler):

    @gen.coroutine
    def get(self, provider='all'):
        scraper_cls = get_scraper(provider)
        if not scraper_cls:
            self.set_status(400)
            self.write({
                "error": "Unkown provider",
            })
            return

        scraper = scraper_cls()
        results = yield scraper.run()

        if provider == 'all': # Combine results from all scrapers
            new_results = []
            for scraper_result_list in results:
                for result in scraper_result_list:
                    new_results.append(result)

            sorted_results = sorted(
                new_results,
                key=lambda d: d['ecstasy'],
                reverse=True)
            results = sorted_results

        self.write({
            "results": results,
        })


ROUTES = [
    (r"/scrapers/(?P<provider>\w+)", ScraperApiHandler),
]

ALL_SCRAPER_ROUTES = [
    (r"/hotels/search", ScraperApiHandler),
]

def run():
    app = web.Application(
        ROUTES,
        debug=True,
    )
    http_server_individual_scrapers = httpserver.HTTPServer(app)
    http_server_individual_scrapers.listen(9000)

    app_2 = web.Application(
        ALL_SCRAPER_ROUTES,
        debug=True
    )
    http_server_all_scrapers = httpserver.HTTPServer(app_2)
    http_server_all_scrapers.listen(8000)
    print "Server (re)started. Listening on ports 9000/8000"

    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run()
