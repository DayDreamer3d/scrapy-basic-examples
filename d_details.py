# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):

    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):

        for about_url in response.css('div.quote > span > a::attr(href)').extract():
            about_url = response.urljoin(about_url)
            yield scrapy.Request(url=about_url, callback=self.parse_about)


        next_page = response.css('li.next > a::attr(href)').extract_first()
        next_page = response.urljoin(next_page)

        yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_about(self, response):
        yield {
            'name': response.css('h3.author-title::text').extract_first(),
            'dob': response.css('span.author-born-date::text').extract_first()
        }
