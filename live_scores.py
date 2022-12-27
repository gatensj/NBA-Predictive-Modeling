from datetime import timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from scrapy.crawler import CrawlerProcess

from diamond_jay.diamond_jay.spiders.secondpoints import SecondHalfPointsSpider
from diamond_jay.diamond_jay.spiders.totalpoints import TotalPointsSpider
from diamond_jay.diamond_jay.spiders.firstpoints import FirstHalfPointsSpider

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

#TODO: Figure out how to change the date of the Scoreboard
board = scoreboard.ScoreBoard()

print(" ")
print(" ")
print("ScoreBoardDate: " + board.score_board_date)
print(" ")

games = board.games.get_dict()
home_teams = []
away_teams = []

# make a list of home and away games
print("Real time scores: ")
for game in games:
    gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
    gameId = game['gameId']

    print(game['homeTeam']['teamCity'] + ": " + str(game['homeTeam']['score']))
    print(game['awayTeam']['teamCity'] + ": " + str(game['awayTeam']['score']))

    home_scores_by_period = game['homeTeam']['periods']
    home_first_half_result = [item for item in home_scores_by_period if item.get('period') < 3]
    home_second_half_result = [item for item in home_scores_by_period if item.get('period') > 2]

    away_scores_by_period = game['awayTeam']['periods']
    away_first_half_result = [item for item in away_scores_by_period if item.get('period') < 3]
    away_second_half_result = [item for item in away_scores_by_period if item.get('period') > 2]

    home_team_first_half_points = 0
    for period in home_first_half_result:
        home_team_first_half_points = home_team_first_half_points + period['score']

    away_team_first_half_points = 0
    for period in away_first_half_result:
        away_team_first_half_points = away_team_first_half_points + period['score']

    home_team_second_half_points = 0
    for period in home_second_half_result:
        home_team_second_half_points = home_team_second_half_points + period['score']

    away_team_second_half_points = 0
    for period in away_second_half_result:
        away_team_second_half_points = away_team_second_half_points + period['score']

    print("First Half for " + game['awayTeam']['teamCity'] + ": "  + str(away_team_first_half_points))
    print("First Half for " + game['homeTeam']['teamCity'] + ": "  + str(home_team_first_half_points))
    first_half_totals = away_team_first_half_points + home_team_first_half_points
    print("First Half Totals for " + game['awayTeam']['teamCity'] + " vs "  + game['homeTeam']['teamCity'] + " " + str(first_half_totals))
    print("Second Half for " + game['homeTeam']['teamCity'] + ": "  + str(home_team_second_half_points))
    print("Second Half for " + game['awayTeam']['teamCity'] + ": " + str(away_team_second_half_points))
    second_half_totals = away_team_second_half_points + home_team_second_half_points
    print("Second Half Totals for " + game['awayTeam']['teamCity'] + " vs " + game['homeTeam']['teamCity'] + " " + str(second_half_totals))

    total_score = game['homeTeam']['score'] + game['awayTeam']['score']
    print("Total: " + str(total_score))
    print(" ")
    print(" ")
    print(" ")

    if game['homeTeam']['teamCity'] == "LA":
        home_teams.append(game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName'])
    else:
        home_teams.append(game['homeTeam']['teamCity'])

    if game['awayTeam']['teamCity'] == "LA":
        away_teams.append(game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName'])
    else:
        away_teams.append(game['awayTeam']['teamCity'])

#TODO: refactor so we can pass the file name so we can get the 1st & 2nd half predictions
file = open("total-points.txt", "r")
#file = open("2nd-half-points.txt", "r")
#file = open("1st-half-points.txt", "r")

my_output = file.read()
points_results = json.loads(my_output)

filtered_home_dict = {k: v for k, v in points_results.items() if k in home_teams}
filtered_away_dict = {k: v for k, v in points_results.items() if k in away_teams}

home_teams_list = [key for key in filtered_home_dict.keys()]
away_teams_list = [key for key in filtered_away_dict.keys()]

total_teams_dict = {}

# use the list of home teams and use it against the scrapped data
for team in home_teams_list:
    home_team_points = filtered_home_dict[team]
    home_team_float_list = []

    # loop through the list of strings and remove the away score and 2021 avg
    home_team_points = home_team_points[:-1]
    fifth_item = home_team_points.pop(4)

    for string_points in home_team_points:
      home_team_float_list.append(float(string_points))

    home_points_totals = 0
    for points in home_team_float_list:
        home_points_totals = home_points_totals + points
    average_team_points = home_points_totals / 4
    total_teams_dict[team] = average_team_points

# use the list of away teams and use it against the scrapped data
for team in away_teams_list:
    away_team_points = filtered_away_dict[team]
    away_team_float_list = []

    # loop through the list of strings and remove the away score and 2021 avg
    away_team_points = away_team_points[:-1]
    fourth_item = away_team_points.pop(3)

    for string_points in away_team_points:
      away_team_float_list.append(float(string_points))

    away_points_totals = 0
    for points in away_team_float_list:
        away_points_totals = away_points_totals + points
    average_team_points = away_points_totals / 4
    total_teams_dict[team] = average_team_points

# take the avg of the home/away points total and add them back up
print("Predictive Score: ")
for game in games:
    home_team = game['homeTeam']['teamCity']
    away_team = game['awayTeam']['teamCity']
    if home_team == 'LA':
        home_team = game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName']

    if away_team == 'LA':
        away_team = game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName']

    game_total = total_teams_dict[home_team] + total_teams_dict[away_team]
    print(game['awayTeam']['teamName'] + ' VS ' + game['homeTeam']['teamName'])
    print(game_total)
    print(" ")
    print(" ")


# TODO: Get the O/U from the Sports Books
print("Daily Line info: ")


'''
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.live.nba.endpoints import boxscore


nba_teams = teams.get_teams()
sixers = [team for team in nba_teams if team['abbreviation'] == 'PHI'][0]
sixers_id = sixers['id']

# Query for games where the Sixers were playing
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=sixers_id, date_from_nullable='12/01/2022')
games = gamefinder.get_data_frames()[0]
games.head()
print(games)
print(games['GAME_ID'])
'''
