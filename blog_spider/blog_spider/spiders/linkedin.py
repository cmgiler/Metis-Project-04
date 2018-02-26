import scrapy


class LinkedinSpider(scrapy.Spider):

    name = 'linkedin_spider'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'https://blog.linkedin.com/'
    ]

    def parse(self, response):
        # Extract the links to the individual festival pages
        article_links = response.xpath('//ul[@class="post-list"]/li/div[@class="post-wrapper"]/div[@class="post"]/div[@class="header"]/h2/a/@href').extract()
        article_links = ['https://blog.linkedin.com'+link for link in article_links]

        article_titles = response.xpath('//ul[@class="post-list"]/li/div[@class="post-wrapper"]/div[@class="post"]/div[@class="header"]/h2/a/text()').extract()

        
        for i in range(len(article_links)):
            yield scrapy.Request(
                url=article_links[i],
                callback=self.parse_article,
                meta={'url': article_links[i], 'name': article_titles[i]}
            )

        # Follow pagination links and repeat
        next_url = 'https://blog.linkedin.com' + response.xpath('//div[@id="older"]/a/@href').extract()[0]


        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def parse_article(self, response):
        
        title = response.xpath('//h1[@class="heading"]/text()').extract()[0]

        content = response.xpath('//div[@class="full-content"]//p/text()').extract()
        content = [c.strip() for c in content]
        content = ' '.join(content)

        date = response.xpath('//h2[@class="publish-info"]/div[@class="date"]/text()').extract()[0]

        author = response.xpath('//a[@rel="author"]/text()').extract()[-1]

        post_categories = response.xpath('//ul[@class="category-list"]/li/a/text()').extract()

        yield {
            'title': title,
            'content': content,
            'date': date,
            'author': author,
            'post_categories': post_categories
        }