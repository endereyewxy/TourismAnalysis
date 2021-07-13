import json

import requests


class ProxyMiddleware:
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def process_request(self, request, spider):
        request.meta['download_timeout'] = 10
        request.meta["proxy"] = 'http://' + json.loads(requests.get('http://127.0.0.1:5010/get/').text)['proxy']

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def process_exception(self, request, exception, spider):
        requests.get('http://192.168.31.230:5010/delete/?proxy=' + request.meta['proxy'].split("//")[-1])
        request.meta['proxy'] = 'http://' + json.loads(requests.get('http://127.0.0.1:5010/get/').text)['proxy']
        return request
