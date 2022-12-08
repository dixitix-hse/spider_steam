import scrapy

from spider_steam.items import SpiderSteamItem
from urllib.parse import urlencode
import re

queries = ['Football', 'Adventure', 'Horrors']

class SteamspiderSpider(scrapy.Spider):
    name = 'SteamSpider'

    def parse_game_page(self, response):
        release_date = response.xpath('//div[@class="release_date"]//div[@class="date"]/text()').extract()
        not_yet = response.xpath('//*[@class="not_yet"]/text()').extract()
        if release_date == [] or not_yet != [] or not any(char.isdigit() for char in release_date[0]) or int(release_date[0][-4:]) <= 2000:
            return
        item = SpiderSteamItem()
        name = response.xpath('//div[@id="appHubAppName"]/text()').extract()
        categories = response.xpath('//div[@class="blockbg"]//a/text()').extract()[1:]
        reviews_count = response.xpath('//div[@itemprop="aggregateRating"]//span[@class="responsive_hidden"]/text()').extract()
        review_points = response.xpath('//div[@itemprop="aggregateRating"]//span[contains(@class, "game_review_summary")]/text()').extract()
        developer = response.xpath('//div[@id="developers_list"]//a/text()').extract()
        tags = response.xpath('//div[@class="glance_tags popular_tags"]//a/text()').extract()
        for index in range(len(tags)):
            tags[index] = tags[index].strip()
        price = response.xpath('//div[@class="game_purchase_action_bg"]//div[@class="game_purchase_price price" or @class="discount_final_price"]/text()').extract()[0]
        platforms_available = response.xpath('//div[contains(@class, "game_area_sys_req sysreq_content")]//@data-os').extract()

        item['name'] = ''.join(name).strip()
        item['category'] = '/'.join(categories).strip()
        item['reviews_count'] = re.sub(r'[()]', '', ''.join(reviews_count).strip())
        item['review_points'] = ''.join(review_points).strip()
        item['developer'] = '&'.join(developer).strip()
        item['tags'] = ', '.join(tags).strip()
        item['price'] = ''.join(price).strip()
        item['platforms_available'] = '&'.join(platforms_available).strip()
        yield item

    def start_requests(self):
        for query in queries:
            url_1 = 'https://store.steampowered.com/search/?' + urlencode({'term': query, 'page': '1'})
            yield scrapy.Request(url=url_1, callback=self.parse_keyword_response)
            url_2 = 'https://store.steampowered.com/search/?' + urlencode({'term': query, 'page': '2'})
            yield scrapy.Request(url=url_2, callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        games = response.xpath("//a[contains(@href,'app')]/@href").extract()
        for game in games:
            yield scrapy.Request(url=game, callback=self.parse_game_page)
