from nba_api.stats.endpoints import leaguedashteamstats
import openpyxl
import scrapy
from scrapy.crawler import CrawlerProcess
from diamond_jay.diamond_jay.spiders.espn import EspnSpider


print('hello world')

season_factors = leaguedashteamstats.LeagueDashTeamStats(
    season='2022-23', measure_type_detailed_defense="Four Factors",
).get_data_frames()[0]

season_factors = season_factors.drop(columns=[
    'TEAM_ID', 'GP', 'W', 'L', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'EFG_PCT_RANK', 'FTA_RATE_RANK',
    'TM_TOV_PCT_RANK', 'OREB_PCT_RANK', 'OPP_EFG_PCT_RANK', 'OPP_FTA_RATE_RANK', 'OPP_TOV_PCT_RANK',
    'OPP_OREB_PCT_RANK', 'CFID', 'CFPARAMS', 'W_PCT', 'MIN'
])

print(season_factors)
season_factors.to_excel('nba_stats.xlsx', sheet_name='Four Factors')


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(EspnSpider)
process.start() # the script will block here until the crawling is finished

print(" ")
print(" ")
print(" ")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print(process)
print('goodbye moon')
