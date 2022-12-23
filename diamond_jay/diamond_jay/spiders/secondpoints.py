import scrapy
import json

class SecondHalfPointsSpider(scrapy.Spider):
    name = 'teamranking'
    allowed_domains = ['teamrankings.com']
    start_urls = ['https://www.teamrankings.com/nba/stat/2nd-half-points-per-game']
    kwargs = []

    def parse(self, response):
        information = response.xpath('//h1[@id="h1-title"]/text()').get()
        count = 0
        good_info = []
        team_names = response.xpath('//td[@class="text-left nowrap"]//a/text()').getall()
        #print(team_names)

        more_info = response.xpath('//td[@class="text-right"]/text()').getall()
        small_list = []

        for info in more_info:
            small_list.append(info)
            count = count + 1
            if count > 5:
                count = 0
                good_info.append(small_list)
                small_list = []

        res = dict(zip(team_names, good_info))
        #print(res)
        with open("2nd-half-points.txt", "w") as f:
            f.write(json.dumps(res))

        return {"good_info": "good_info"}


