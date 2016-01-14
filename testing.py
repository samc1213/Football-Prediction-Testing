import csv
import datetime

class Team:
    def __init__(self, name=None, games=None):
        if games is None:
            self.games = []
        self.name = name

class Game:
    def __init__(self, date, hometeamcode, visitteamcode):
        self.date = date
        self.hometeamcode = hometeamcode
        self.visitteamcode = visitteamcode
        # self.homerushyards = homerushyards
        # self.homepassyards = homepassyards
        # self.homerushtds = homerushtds
        # self.homepasstds = homepasstds

teams = {}
games = {}

with open('game.csv') as game:
    for row in csv.DictReader(game):
        visitteamcode = int(row['Visit Team Code'])
        hometeamcode = int(row['Home Team Code'])
        gamecode = int(row['Game Code'])
        gamedate = datetime.datetime.strptime(row['Date'], '%m/%d/%Y').date()

        games[gamecode] = Game(gamedate, hometeamcode, visitteamcode)

with open('team-game-statistics.csv') as gamestats:
    for row in csv.DictReader(gamestats):
        gamecode = int(row['Game Code'])
        rowTeamCode = int(row['Team Code'])
        rowGame = games[gamecode]

        if rowGame.hometeamcode == rowTeamCode:
            rowGame.homerushyards = row['Rush Yard']
            rowGame.homepassyards = row['Pass Yard']
            rowGame.homerushtds = row['Rush TD']
            rowGame.homepasstds = row['Pass TD']
        else:
            rowGame.visitrushyards = row['Rush Yard']
            rowGame.visitpassyards = row['Pass Yard']
            rowGame.visitrushtds = row['Rush TD']
            rowGame.visitpasstds = row['Pass TD']

        if rowTeamCode not in teams:
            teams[rowTeamCode] = Team()

        teams[rowTeamCode].games.append(rowGame)

for code, team in teams.iteritems():
    team.games.sort(key=lambda x: x.date)

for game in teams[5].games:
    print game.date
