from datetime import datetime, timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from scrapy.crawler import CrawlerProcess

from diamond_jay.diamond_jay.spiders.secondpoints import SecondHalfPointsSpider
from diamond_jay.diamond_jay.spiders.totalpoints import TotalPointsSpider
from diamond_jay.diamond_jay.spiders.firstpoints import FirstHalfPointsSpider

import json
import os
import requests

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


process.crawl(TotalPointsSpider)
process.start() # the script will block here until the crawling is finished
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")

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
        home_teams.append(game['homeTeam']['teamCity'] + " " + game['homeTeam']['teamName'])
    elif game['homeTeam']['teamCity'] == "Oklahoma City":
        home_teams.append("Okla City")
    elif game['homeTeam']['teamCity'] == "Los Angeles":
        home_teams.append("LA Lakers")
    else:
        home_teams.append(game['homeTeam']['teamCity'])

    if game['awayTeam']['teamCity'] == "LA":
        away_teams.append(game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName'])
    elif game['awayTeam']['teamCity'] == "Oklahoma City":
        away_teams.append("Okla City")
    elif game['awayTeam']['teamCity'] == "Los Angeles":
        away_teams.append("LA Lakers")
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
total_teams_combine_by_home_team = {'0This is my prediction dictionary' : 1}

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
    elif home_team == "Oklahoma City":
        home_team = "Okla City"
    elif home_team == "Los Angeles":
        home_team = "LA Lakers"
    else:
        home_team = home_team

    if away_team == 'LA':
        away_team = game['awayTeam']['teamCity'] + " " + game['awayTeam']['teamName']
    elif away_team == "Oklahoma City":
        away_team = "Okla City"
    elif away_team == "Los Angeles":
        away_team = "LA Lakers"
    else:
        away_team = away_team

    game_total = total_teams_dict[home_team] + total_teams_dict[away_team]
    total_teams_combine_by_home_team[home_team] = game_total

    print(game['awayTeam']['teamName'] + ' VS ' + game['homeTeam']['teamName'])
    print(game_total)
    print(" ")
    print(" ")


# TODO: Get the O/U from the Sports Books for historical odds (if we change the scoreboard date)
print("Daily Line info: ")

API_KEY = 'bd21706b568c46f05ab0aaeb60c6198e'
#API_KEY = "DEBUG"
SPORT = 'basketball_nba'
REGION = 'us'
MARKET = 'totals'

odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key': API_KEY,
    'sport': SPORT,
    'region': REGION,
    'mkt': MARKET,
})

odds_json = json.loads(odds_response.text)

if not odds_json['success']:
    print(odds_json['msg'])

else:
    print('Number of events:', len(odds_json['data']))

    # Check your usage
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])

predictive_teams_dict = {'0This OU dictionary from Odds API' : 2}
for item in odds_json['data']:
    sites = item['sites']
    points = 0
    for site in sites:
        points_list = site['odds']['totals']['points']
        points = points + float(points_list[0])
    sites_count = float(item['sites_count'])
    if sites_count > 0:
        points = points / float(item['sites_count'])
    predictive_teams_dict[item['home_team']] = points

print(" ")
for key, value in predictive_teams_dict.items():
    print(key + " " + str(value))

#TODO: Compare the Odds v the Predictive v the Actual (we should run this in the day and save the results)
now = datetime.now()

# Format the date and time as a string
date_string = now.strftime("%Y-%m-%d")
filename_title = "predictions-info-"+date_string+'.txt'

# Sort the two dicts by ABC
total_teams_combine_by_home_team_sorted = {k: total_teams_combine_by_home_team[k] for k in sorted(total_teams_combine_by_home_team)}
predictive_teams_dict_sorted = {k: predictive_teams_dict[k] for k in sorted(predictive_teams_dict)}

file_contents = json.dumps(total_teams_combine_by_home_team_sorted) + " " + json.dumps(predictive_teams_dict_sorted)
directory = r'C:\Users\jgatens\Downloads\0Stuff-PC\work\code\NBA-Predictive-Modeling\predictions'
file_path = os.path.join(directory, filename_title)

with open(file_path, "w") as f:
    f.write(file_contents)

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
