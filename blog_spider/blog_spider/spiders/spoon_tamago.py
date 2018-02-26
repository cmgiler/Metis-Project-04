import scrapy


class TamagoSpider(scrapy.Spider):

    name = 'spoon_tamago'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'http://www.spoon-tamago.com/'
    ]

    def parse(self, response):
        # Extract the links to the individual festival pages
        article_links = response.xpath('//h2[@class="post-title"]/a/@href').extract()
        article_titles = response.xpath('//h2[@class="post-title"]/a/text()').extract()
        
        for i in range(len(article_links)):
            yield scrapy.Request(
                url=article_links[i],
                callback=self.parse_article,
                meta={'url': article_links[i], 'name': article_titles[i]}
            )

        # Follow pagination links and repeat
        next_url = response.xpath('//a[@class="post-nav-older"]/@href').extract()[0]


        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def parse_article(self, response):
        
        title = response.xpath('//h2[@class="post-title"]/a/text()').extract()[0]

        content = response.xpath('//div[@class="post-content"]/p/text() | //div[@class="post-content"]/p/a/text()').extract()
        content = [c.strip() for c in content]
        content = ' '.join(content)

        date = response.xpath('//span[@class="post-date"]/a/text()').extract()[0]

        author = ', '.join(response.xpath('//span[@class="post-author"]/a/text()').extract())

        post_categories = response.xpath('//p[@class="post-categories"]/a/text()').extract()
        post_tags = response.xpath('//p[@class="post-tags"]/a/text()').extract()

        yield {
            'title': title,
            'content': content,
            'date': date,
            'author': author,
            'post_categories': post_categories,
            'post_tags': post_tags
        }
