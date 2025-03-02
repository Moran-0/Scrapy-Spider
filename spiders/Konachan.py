from typing import Iterable, Any

from lxml import etree
from tqdm import tqdm
import scrapy
from scrapy import Request
from scrapy.http import Response
from scrapy_learn.items import KonachanItem
import requests


class KonachanSpider(scrapy.Spider):
    name = "Konachan"
    allowed_domains = ["konachan.net"]
    start_urls = ["https://konachan.net/post/"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        year, month, day, num = 2025, 2, 10, 11
        img_url_list = []
        print("开始Konochan网站图片爬取：")
        for i in tqdm(range(0, num)):
            popular_url = f"https://konachan.net/post/popular_by_day?day={day + i}&month={month}&year={year}"
            res = etree.HTML(requests.get(url=popular_url).text)
            img_url_show = res.xpath('//*[@id="post-list-posts"]/li/div/a/@href')
            for url_show in img_url_show:
                res_show = etree.HTML(requests.get(url='https://konachan.net'+url_show).text)
                file_url = res_show.xpath("//a[@class='original-file-unchanged']/@href")
                if len(file_url) == 0:
                    file_url = res_show.xpath("//a[@class='original-file-changed']/@href")
                img_url_list.append(file_url[0])
            item = KonachanItem(file_urls=img_url_list)
            yield item

