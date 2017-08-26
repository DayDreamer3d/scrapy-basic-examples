# -*- coding: utf-8 -*-
import json
import scrapy


class ScrollQuotesSpider(scrapy.Spider):

    name = 'quotes-scroll'
    api_page = 1
    api_url = 'http://quotes.toscrape.com/api/quotes?page={}'
    start_urls = [api_url.format(api_page)]

    def parse(self, response):
        data = json.loads(response.text)

        for quote in data['quotes']:
            yield {
                'author': quote['author']['name'],
                'text': quote['text']
            }

        if data.get('has_next'):
            self.api_page += 1
            yield scrapy.Request(url=self.api_url.format(self.api_page), callback=self.parse)
