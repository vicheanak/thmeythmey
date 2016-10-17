# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from thmeythmey.items import ThmeythmeyItem
from scrapy.linkextractors import LinkExtractor
import time


class TestSpider(CrawlSpider):
    name = "thmeythmey"
    allowed_domains = ["thmeythmey.com"]
    start_urls = [
    'https://thmeythmey.com/?page=location&menu1=3&ref_id=9&ctype=article&id=3&lg=kh',
    ]

    def parse(self, response):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        hxs = scrapy.Selector(response)

        articles = hxs.xpath('//div[@class="news_icon"]')

        for article in articles:
            item = ThmeythmeyItem()
            item['categoryId'] = '1'
            name = article.xpath('div[contains(@class, "title_item_news")]/span[1]/a[1]/text()')
            if not name:
                print('ThmeyThmey => [' + now + '] No title')
            else:
                item['name'] = name.extract_first()

            url = article.xpath('div[contains(@class, "title_item_news")]/span[1]/a[1]/@href')
            if not url:
                print('ThmeyThmey => [' + now + '] No url')
            else:
                item['url'] = 'https://thmeythmey.com/' + url.extract_first()

            description = article.xpath('div[contains(@class, "short_detail_ctn")]/span[1]/text()')
            if not description:
                print('ThmeyThmey => [' + now + '] No description')
            else:
                item['description'] = description.extract_first()

            imageUrl = article.xpath("""
                a[1]/div[1]/@data-src
                """)

            item['imageUrl'] = ''
            if not imageUrl:
                print('ThmeyThmey => [' + now + '] No imageUrl')
            else:
                item['imageUrl'] = imageUrl.extract_first()

            yield item

    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        item_page = hxs.css('div.item-page')
        description = item_page.xpath('p[1]/text()')
        if not description:
            print('ThmeyThmey => [' + now + '] No description')
        else:
            item['description'] = item_page.xpath('p[1]/strong/text()').extract_first() + ' ' + description.extract_first()

        imageUrl = item_page.xpath('p[last()]/img/@src')
        if not imageUrl:
            print('ThmeyThmey => [' + now + '] No imageUrl')
        else:
            item['imageUrl'] = imageUrl.extract_first()


        yield item
