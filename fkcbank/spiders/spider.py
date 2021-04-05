import scrapy

from scrapy.loader import ItemLoader

from ..items import FkcbankItem
from itemloaders.processors import TakeFirst


class FkcbankSpider(scrapy.Spider):
	name = 'fkcbank'
	start_urls = ['https://www.fkc.bank/information/media-room/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="entry-title"]/text()').get()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "et_pb_text_inner", " " ))]//p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="published"]/text()').get()

		item = ItemLoader(item=FkcbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
