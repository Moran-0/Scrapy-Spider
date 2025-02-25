import requests
import urllib
import os
import re
from scrapy_learn.spiders.ZeroChan import character


class ScrapyLearnPipeline:
    def process_item(self, item, spider):
        return item


class ZeroChanImageDownloadPipeline(object):
    def __init__(self):
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'referer': 'https://www.zerochan.net/',
        }
        self.image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), character)
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)

    def process_item(self, item, spider):
        res = re.search(pattern='(?<=https://static\.zerochan\.net/)(.*)', string=item["file_urls"][0]).group()
        print(res)
        file_name = f'{item["position"]}-{res}'
        print(item["file_urls"][0])
        response = requests.get(item["file_urls"][0], stream=True,headers=self.default_headers)
        # 检查请求是否成功
        if response.status_code == 200:
            # 打开一个文件用于写入二进制数据
            with open(os.path.join(self.image_path, file_name), 'wb') as file:
                # 将图片内容写入文件
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print("图片保存成功！")
            file.close()
        else:
            print(f"请求失败，状态码: {response.status_code}")
        # urllib.request.urlretrieve(url=item["file_urls"][0], filename=os.path.join(self.image_path, file_name))
        return item
