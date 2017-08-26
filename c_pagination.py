# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for item in response.css('div.quote'):
            yield {
                'author': item.css('small.author::text').extract_first(),
                'text': item.css('span.text::text').extract_first(),
            }

        next_page = response.css('li.next > a::attr(href)').extract_first()
        next_page = response.urljoin(next_page)

        yield scrapy.Request(url=next_page, callback=self.parse)
