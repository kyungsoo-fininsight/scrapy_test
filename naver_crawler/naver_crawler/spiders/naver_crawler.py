import scrapy


class NaverSpider(scrapy.Spider):
    name = "naver"

    def start_requests(self):

        urls = [
            "https://search.naver.com/search.naver?where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=2005.01.01&de=2015.01.31&docid=&nso=so%3Ar%2Cp%3Afrom20050101to20150131%2Ca%3Aall&mynews=1&refresh_start=0&related=0"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        articles = response.xpath("//dd[@class='txt_inline']")
        urls = []
        for article in articles:
            if (article.xpath("./span[@class='_sp_each_source']/text()").get().
                    strip() == "연합뉴스"):
                urls.extend(article.xpath("./a/@href").extract())

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content = response.xpath(
            "//div[@id='articleBodyContents']//text()").getall()
        self.log(content)
