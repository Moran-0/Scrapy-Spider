import json
import random
from typing import Iterable, Any
import requests
import scrapy
from scrapy import Request
from scrapy.http import Response
import time

from scrapy_learn.items import SimpleWallpaperItem


class SimplewallpaperSpider(scrapy.Spider):
    name = "SimpleWallpaper"
    allowed_domains = ["bz.zzzmh.cn", "api.zzzmh.cn", "cdn2.zzzmh.cn"]
    start_urls = ["https://bz.zzzmh.cn/index"]

    def start_requests(self) -> Iterable[Request]:
        data = {'size': '24', 'current': '1', 'sort': '0', 'category': '0', 'resolution': '0', 'color': '0',
                'categoryId': '0', 'ratio': '0', }
        headers = {
            "authority": "api.zzzmh.cn",
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://bz.zzzmh.cn",
            "referer": "https://bz.zzzmh.cn/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
        url = "https://api.zzzmh.cn/v2/bz/v3/getData"
        for page in range(1, 6):
            data["current"] = str(page)
            yield scrapy.Request(url=url, method='POST', body=json.dumps(data))

    def parse(self, response: Response,  **kwargs: Any) -> Any:
        img_data = json.loads(response.text)['data']['list']
        base_url = "https://api.zzzmh.cn/v2/bz/v3/getUrl/"
        download_url = []
        for i in range(0, len(img_data)):
            res = requests.get(url=base_url + img_data[i]['i'] + str(img_data[i]['t']) + str(9))
            download_url.append(res.url)
            time.sleep(random.uniform(0.5, 1.5))
        print(download_url)
        item = SimpleWallpaperItem(file_urls=download_url)
        yield item
