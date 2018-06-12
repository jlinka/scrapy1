#-*-coding utf-8-*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import InvestmentItem

class InvestmentSpider(scrapy.Spider):
    name = "investment"
    #allowed_domains = ['www.58ztr.com']
    start_urls = ["http://www.58trz.com/zixun_149.html"]

    def parse(self, response):
        #提取列表中每一个新闻的链接
        #le = LinkExtractor(restrict_css='ul#articleList>li>h3')

        #for link in le.extract_links(response):
            #yield scrapy.Request(link.url, callback=self.parse_investment())

        link = response.css('ul#articleList>li>h3>a::attr(href)').extract()
        for one in link:
            url = response.urljoin(one)
            yield scrapy.Request(url=url, callback=self.parse_investment)

        for num in range(1, 180):
            next_link = "http://www.58trz.com/zixun_149.html?page="
            next_link += str(num)
            print(next_link)
            yield scrapy.Request(url=next_link, callback=self.parse)

        #提取下一页
        #le = LinkExtractor(restrict_css='li>a.page-next')
        #links = le.extract_links(response)
        #print(links)
        # if links:
        #     next_url = links[-1].url
        #     print(next_url)
        #     yield scrapy.Request(next_url, callback=self.parse)

    def parse_investment(self, response):
        item = InvestmentItem()

        item['title'] = response.xpath('//div[@class="info-d-title"]/h1/text()').extract_first()
        item['date'] = response.xpath('//div[@class="info-d-title"]/div/span/text()').extract()[4]
        item['content'] = response.xpath('string(//div[@class="info-d-body"])').\
            extract_first().replace(u'\u3000\u3000', u'\n').replace(u'\r\n', u'\n').replace(u'\t\t\t\t\t\t\n', u'\n')\
            .replace(u'\t\t\t\t\t', u'')
        item['source'] = response.xpath('//div[@class="info-d-title"]/div/span/text()').extract()[1]
        item['link'] = response.url


        yield item

    # def parse(self, response):
    #     for book in response.css('article.product_pod'):
    #         name = book.xpath('./h3/a/@title').extract_first()
    #         price = book.css('p.price_color::text').extract_first()
    #         yield{
    #             'name': name,
    #             'price': price,
    #         }
    #     #提取链接
    #     next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
    #     print(next_url)
    #     if next_url:
    #         next_url = response.urljoin(next_url)
    #         yield scrapy.Request(next_url, callback=self.parse)
    #     #
    #     # le = LinkExtractor(restrict_css='ul.pager li.next')
    #     # links = le.extract_links(response)
    #     # if links:
    #     #     next_url = links[0].url
    #     #     yield scrapy.Request(next_url, callback=self.parse)