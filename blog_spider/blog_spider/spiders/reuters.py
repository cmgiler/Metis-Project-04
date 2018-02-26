import scrapy
import json

class ReutersSpider(scrapy.Spider):

    name = 'reuters_spider'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['https://www.reuters.com/news/technology']

    def parse(self, response):
        # Extract the links to the individual festival pages
        with open('blog_spider/spiders/reuters_tech.json', 'r') as fn:
            start_links = json.load(fn)

        article_links = [link['link'] for link in start_links]
        article_titles = [link['title'] for link in start_links]

        for i in range(len(article_links)):
            yield scrapy.Request(
                url=article_links[i],
                callback=self.parse_article,
                meta={'url': article_links[i], 'name': article_titles[i]}
            )

    def parse_article(self, response):
        
        title = response.xpath('//h1/text()').extract()[0]

        content = response.xpath('//div[@class="StandardArticleBody_body_1gnLA"]/p/text()').extract()
        content = [c.strip() for c in content]
        content = ' '.join(content)

        date = response.xpath('//div[@class="ArticleHeader_date_V9eGk"]/text()').extract()[0].split('/')[0].strip()

        author = response.xpath('//div[@class="BylineBar_byline_31BCV"]/span/a/text()').extract()
        author = ', '.join(author)

        yield {
            'title': title,
            'content': content,
            'date': date,
            'author': author
        }