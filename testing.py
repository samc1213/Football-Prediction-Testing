import csv
import datetime

class Team:
    def __init__(self, name=None, games=None):
        if games is None:
            self.games = []
        self.name = name

class Game:
    def __init__(self, date, hometeamcode, visitteamcode, rushyds=None, passyds=None, rushtds=None, passtds=None, points=None, avgoffrushyds=None, avgdefrushyds=None, avgoffpassyds=None, avgdefpassyds=None):
        self.date = date
        self.hometeamcode = hometeamcode
        self.visitteamcode = visitteamcode
        if rushyds is None:
            self.rushyds = [None, None]
        if passyds is None:
            self.passyds = [None, None]
        if points is None:
            self.points = [None, None]
        if rushtds is None:
            self.rushtds = [None, None]
        if passtds is None:
            self.passtds = [None, None]
        if avgoffrushyds is None:
            self.avgoffrushyds = [None, None]
        if avgdefrushyds is None:
            self.avgdefrushyds = [None, None]
        if avgdefpassyds is None:
            self.avgdefpassyds = [None, None]
        if avgoffpassyds is None:
            self.avgoffpassyds = [None, None]

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
        # HOME, AWAY!!!! HOME, AWAY in ze lists
        if rowGame.hometeamcode == rowTeamCode:
            rowGame.rushyds[0] = int(row['Rush Yard'])
            rowGame.passyds[0] = int(row['Pass Yard'])
            rowGame.rushtds[0] = int(row['Rush TD'])
            rowGame.passtds[0] = int(row['Pass TD'])
            rowGame.points[0] = int(row['Points'])
        else:
            rowGame.rushyds[1] = int(row['Rush Yard'])
            rowGame.passyds[1] = int(row['Pass Yard'])
            rowGame.rushtds[1] = int(row['Rush TD'])
            rowGame.passtds[1] = int(row['Pass TD'])
            rowGame.points[1] = int(row['Points'])
        if rowTeamCode not in teams:
            teams[rowTeamCode] = Team()

        teams[rowTeamCode].games.append(rowGame)

for code, team in teams.iteritems():
    team.games.sort(key=lambda x: x.date)

offrushyds = 0
offpassyds = 0
defrushyds = 0
defpassyds = 0
gamecount = 0.0
firstgame = True
for game in teams[5].games:
    if game.hometeamcode == 5:
        A = 0
        B = 1
    elif game.visitteamcode == 5:
        A = 1
        B = 0
    else:
        print "ERROR"
    if firstgame:
        game.avgoffrushyds[A] = offrushyds
        game.avgdefrushyds[A] = defrushyds
        game.avgoffpassyds[A] = offpassyds
        game.avgdefpassyds[A] = defpassyds
        firstgame = False
        offrushyds += game.rushyds[A]
        defrushyds += game.rushyds[B]
        offpassyds += game.passyds[A]
        defpassyds += game.passyds[B]
    else:
        game.avgoffrushyds[A] = offrushyds/gamecount
        game.avgdefrushyds[A] = defrushyds/gamecount
        game.avgoffpassyds[A] = offpassyds/gamecount
        game.avgdefpassyds[A] = defpassyds/gamecount
        offrushyds += game.rushyds[A]
        defrushyds += game.rushyds[B]
        offpassyds += game.passyds[A]
        defpassyds += game.passyds[B]
    gamecount += 1.0

for game in teams[5].games:
    if game.hometeamcode == 5:
        print game.avgoffrushyds[0], " offh"
        print game.avgdefrushyds[0], " home"
        print game.avgoffrushyds[0]
        print game.avgdefpassyds[0]
    else:
        print game.avgoffrushyds[1], " offv"
        print game.avgdefrushyds[1], " visit"
        print game.avgoffrushyds[1]
        print game.avgdefpassyds[1]
