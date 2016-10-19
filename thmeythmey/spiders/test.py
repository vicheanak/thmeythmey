# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from thmeythmey.items import ThmeythmeyItem
from scrapy.linkextractors import LinkExtractor
import time
import lxml.etree
import lxml.html
from lxml.html import builder as E
from stripogram import html2text, html2safehtml

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
<<<<<<< Updated upstream

            item['imageUrl'] = ''
=======
>>>>>>> Stashed changes
            if not imageUrl:
                print('ThmeyThmey => [' + now + '] No imageUrl')
            else:
                item['imageUrl'] = imageUrl.extract_first()

            # if item['url'] == 'https://thmeythmey.com/?page=detail&ctype=article&id=45659&lg=kh':
            request = scrapy.Request(item['url'], callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")

        content = root.xpath('//span[@class="left kh size17_kh dark lineheight26_kh"][1]')[0]
        imageEle = E.IMG(src=item['imageUrl'])
        imageEle = lxml.html.tostring(imageEle, encoding=unicode)
        htmlcontent = imageEle
        for p in content.iterchildren():
            imgE = p.xpath('//img[contains(@src, "advertise")]')
            if imgE:
                for im in imgE:
                    im.drop_tag()
            c = lxml.html.tostring(p, encoding=unicode)
            wrap_p = lxml.html.fragment_fromstring(c, create_parent='p')

            wrap_p_string = lxml.html.tostring(wrap_p, encoding=unicode)
            clean_html = html2safehtml(wrap_p_string,valid_tags=("p", "img", "div"))
            htmlcontent += clean_html.replace('\n', ' ').replace('\r', '').replace('%0A', '').replace('%0D', '').replace('<p> </p>', '').replace('<p></p>', '')

        print htmlcontent

        item['htmlcontent'] = htmlcontent

        yield item
