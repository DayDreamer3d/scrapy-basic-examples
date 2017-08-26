# -*- coding: utf-8 -*-
import scrapy


class FormQuotesSpider(scrapy.Spider):

    name = 'quotes-form'
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]

    def parse(self, response):
        yield self.parse_login(response)

    def parse_login(self, response):

        csrf = response.css('input[name="csrf_token"]::attr(value)').extract_first()
        post_attrs = {
            'username': 'username',
            'password': 'password',
            'csrf_token': csrf
        }

        return scrapy.FormRequest(url=self.login_url, formdata=post_attrs, callback=self.parse_quotes)

    def parse_quotes(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author_name': quote.css('small.author::text').extract_first(),
                'author_url': quote.css('small.author ~ a[href*="goodreads.com"]::attr(href)').extract_first(),
            }

