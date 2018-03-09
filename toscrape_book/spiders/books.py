# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractor import LinkExtractor
from ..items import ToscrapeBookItem, ToscrapeItemload


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        le = LinkExtractor(restrict_css='article.product_pod h3')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_book)

        le = LinkExtractor(restrict_css='ul.pager li.next')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_book(self, response):

        book_item = ToscrapeBookItem()
        item_loader = ToscrapeItemload(item=ToscrapeBookItem(), response=response)
        item_loader.add_css("name", "li.active::text")
        item_loader.add_css("price", "p.price_color::text")
        item_loader.add_css("upc", "th+td::text")
        item_loader.add_xpath("stock", "(.//tr)[last()-1]/td/text()")
        item_loader.add_xpath("review_num", "(.//tr)[last()]/td/text()")
        book_item = item_loader.load_item()

        yield book_item
