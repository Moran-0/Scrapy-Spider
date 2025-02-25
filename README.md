# 注记文档
## **创建scrapy爬虫项目**
```python scrapy startproject 项目名称```
## **创建爬虫模板文件**
```python scrapy genspider 文件名 "域名" # 文件名不能和项目名一样```
## **运行scrapy项目**
```python scrapy crawl 爬虫项目名称（记得去除robot协议）```
## **开启管道**
- 管道可以有很多个,那么管道是有优先级的,优先级的范围是1到1000,s值越小优先级越高