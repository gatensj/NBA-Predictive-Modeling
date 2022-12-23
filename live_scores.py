from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.live.nba.endpoints import boxscore
from scrapy.crawler import CrawlerProcess
from diamond_jay.diamond_jay.spiders.secondpoints import SecondHalfPointsSpider

import json

f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}"

board = scoreboard.ScoreBoard()
print("ScoreBoardDate: " + board.score_board_date)
games = board.games.get_dict()
home_teams = []
away_teams = []

for game in games:
    gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
    print(f.format(gameId=game['gameId'], awayTeam=game['awayTeam']['teamName'], homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ))
    gameId = game['gameId']

    #print(game['homeTeam']['teamCity'])
    #okay now we have to figure out what the score is at halftime.
    #https://www.teamrankings.com/nba/stat/2nd-half-points-per-game

    print("home: " + str(game['homeTeam']['score']))
    print("away: " + str(game['awayTeam']['score']))

    home_teams.append(game['homeTeam']['teamCity'])
    away_teams.append(game['awayTeam']['teamCity'])
    print()
    print(" ")

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(SecondHalfPointsSpider)
process.start() # the script will block here until the crawling is finished

f = open("2nd-half-points.txt", "r")
my_output = f.read()
points_results = json.loads(my_output)
#print(points_results)

filtered_home_dict = {k: v for k, v in points_results.items() if k in home_teams}
filtered_away_dict = {k: v for k, v in points_results.items() if k in away_teams}

print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
utah_points = filtered_home_dict['Utah']

# empty list to store the floats
utah_float_list = []

# loop through the list of strings
utah_points = utah_points[:-1]

fifth_item = utah_points.pop(4)

for string in utah_points:
  utah_float_list.append(float(string))

utah_points_totals = 0
for points in utah_float_list:
    utah_points_totals = utah_points_totals + points
average_utah_points = utah_points_totals / 4

print("utah avg points " + str(average_utah_points))

print(" ")
print(filtered_home_dict)
print(filtered_away_dict)

'''
nba_teams = teams.get_teams()
sixers = [team for team in nba_teams if team['abbreviation'] == 'PHI'][0]
sixers_id = sixers['id']

# Query for games where the Sixers were playing
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=sixers_id, date_from_nullable='12/01/2022')
games = gamefinder.get_data_frames()[0]
games.head()
print(games)
print(games['GAME_ID'])

print(" ")
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print(" ")
'''
