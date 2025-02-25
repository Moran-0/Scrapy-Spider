import random
import time
import re
import scrapy
import requests
import json
from scrapy_learn.items import ScrapyLearnItem

character = "Hoshimi+Miyabi"


class ZerochanSpider(scrapy.Spider):
    name = "ZeroChan"
    allowed_domains = ["www.zerochan.net"]
    start_urls = ["https://www.zerochan.net/login"]

    def parse(self, response):

        formData = {
            'ref': '/',
            'name': 'Moran',
            'password': '@CYF1112zerochan',
            'login': '登录',
        }
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/127.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'referer': 'https://www.zerochan.net/login?ref=%2F',
        }
        session = requests.Session()
        session.post(url='https://www.zerochan.net/login', data=formData, headers=self.default_headers)
        # print(str(session.cookies))

        for i in range(1, 9):
            url = f'https://www.zerochan.net/{character}?s=fav&p=' + str(i)
            yield scrapy.Request(url=url, cookies=session.cookies.get_dict(), callback=self.parse_data)
            time.sleep(random.uniform(0.5, 1.5))

    def parse_data(self, response):
        character_new = re.sub('\+', '\+', character)
        page = int(
            re.search(pattern=f'(?<=https://www.zerochan.net/{character_new}\?s=fav&p=)(\d+)', string=response.url).group())
        if page == 1:
            script = response.xpath('//*[@id="content"]/script[2]/text()').extract_first()
        else:
            script = response.xpath('//*[@id="content"]/script/text()').extract_first()
        image_json_list = json.loads(script)['itemListElement']

        for item in image_json_list:
            position, url = item['position'], [item['url']]
            image = ScrapyLearnItem(position=position, file_urls=url)
            yield image
            time.sleep(random.uniform(1.5, 2.5))
