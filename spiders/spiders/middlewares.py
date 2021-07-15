import random
import time
import urllib.parse

import requests

from spiders.settings import PROXY_URL


class ProxyMiddleware:
    proxy = None
    delay = None

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def process_request(self, request, spider):
        if 'captcha' in request.url:
            return request.replace(url=urllib.parse.unquote(request.url.split('from=')[-1]))
        if ProxyMiddleware.proxy is None or time.time() - ProxyMiddleware.delay > 30:
            ProxyMiddleware.delay = time.time()
            ProxyMiddleware.proxy = \
                ['http://' + proxy['host'] + ':' + proxy['port'] for proxy in requests.get(PROXY_URL).json()['data']]
        request.meta['download_timeout'] = 10
        request.meta['proxy'] = random.choice(ProxyMiddleware.proxy)

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def process_exception(self, request, exception, spider):
        request.meta['proxy'] = random.choice(ProxyMiddleware.proxy)
        return request
