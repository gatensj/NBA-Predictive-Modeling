from nba_api.stats.endpoints import leaguedashteamstats
from scrapy.crawler import CrawlerProcess
from diamond_jay.diamond_jay.spiders.firstpoints import FirstHalfPointsSpider
from diamond_jay.diamond_jay.spiders.secondpoints import SecondHalfPointsSpider
from diamond_jay.diamond_jay.spiders.totalpoints import TotalPointsSpider
import openpyxl
import scrapy
import json

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})


'''
process.crawl(FirstHalfPointsSpider)
process.start() # the script will block here until the crawling is finished
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
'''

'''
process.crawl(SecondHalfPointsSpider)
process.start() # the script will block here until the crawling is finished
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
'''

'''
process.crawl(TotalPointsSpider)
process.start() # the script will block here until the crawling is finished
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
'''


season_factors = leaguedashteamstats.LeagueDashTeamStats(
    season='2022-23', measure_type_detailed_defense="Four Factors",
).get_data_frames()[0]

season_factors_dict = leaguedashteamstats.LeagueDashTeamStats(
    season='2022-23', measure_type_detailed_defense="Four Factors",
).get_dict()

season_factors = season_factors.drop(columns=[
    'TEAM_ID', 'GP', 'W', 'L', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'EFG_PCT_RANK', 'FTA_RATE_RANK',
    'TM_TOV_PCT_RANK', 'OREB_PCT_RANK', 'OPP_EFG_PCT_RANK', 'OPP_FTA_RATE_RANK', 'OPP_TOV_PCT_RANK',
    'OPP_OREB_PCT_RANK', 'CFID', 'CFPARAMS', 'W_PCT', 'MIN'
])

team_info = season_factors_dict['resultSets']
resultSets = team_info[0]
rowSet = resultSets['rowSet']

team_data = []
for items in rowSet:
    team_name = items.pop(1)
    team_values = items
    my_dict = {team_name: team_values}
    team_data.append(my_dict)

print(season_factors)
season_factors.to_excel('nba_stats.xlsx', sheet_name='Four Factors')

print(" ")
print(" ")
print(" ")
print(team_data)

'''
f = open("total-points.txt", "r")
my_output = f.read()
points_results = json.loads(my_output)

print("   ")
print(points_results)
'''