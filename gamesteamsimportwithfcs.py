'''
This file includes FCS teams that may only play 1 game. In fact 59 teams have played only 1 game.
Therefore, some long-run summing might get messed up.
'''


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

def getMeTeamsAndGamesBitch():
    teams = {}
    games = {}

    with open('data/2013/game.csv') as game:
        for row in csv.DictReader(game):
            visitteamcode = int(row['Visit Team Code'])
            hometeamcode = int(row['Home Team Code'])
            gamecode = int(row['Game Code'])
            gamedate = datetime.datetime.strptime(row['Date'], '%m/%d/%Y').date()

            games[gamecode] = Game(gamedate, hometeamcode, visitteamcode)

    with open('data/2013/team-game-statistics.csv') as gamestats:
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
                rowGame.passats[0] = int(row['Pass Att'])
                rowGame.rushats[0] = int(row['Rush Att'])
                rowGame.points[0] = int(row['Points'])
            else:
                rowGame.rushyds[1] = int(row['Rush Yard'])
                rowGame.passyds[1] = int(row['Pass Yard'])
                rowGame.rushtds[1] = int(row['Rush TD'])
                rowGame.passtds[1] = int(row['Pass TD'])
                rowGame.passats[1] = int(row['Pass Att'])
                rowGame.rushats[1] = int(row['Rush Att'])
                rowGame.points[1] = int(row['Points'])
            if rowTeamCode not in teams:
                teams[rowTeamCode] = Team()

            teams[rowTeamCode].games.append(rowGame)

    for code, team in teams.iteritems():
        team.games.sort(key=lambda x: x.date)

    for teamid, team in teams.iteritems():
        offrushyds = 0
        offpassyds = 0
        defrushyds = 0
        defpassyds = 0
        rushats = 0
        passats = 0
        gamecount = 0.0
        firstgame = True
        for game in team.games:
            if game.hometeamcode == teamid:
                A = 0
                B = 1
            elif game.visitteamcode == teamid:
                A = 1
                B = 0
            else:
                print "ERROR"
            if firstgame:
                game.avgoffrushyds[A] = offrushyds
                game.avgdefrushyds[A] = defrushyds
                game.avgoffpassyds[A] = offpassyds
                game.avgdefpassyds[A] = defpassyds
                game.yardsperplay[A] = 0
                firstgame = False
                offrushyds += game.rushyds[A]
                defrushyds += game.rushyds[B]
                offpassyds += game.passyds[A]
                defpassyds += game.passyds[B]
                rushats += game.rushats[A]
                passats += game.passats[A]
            else:
                game.avgoffrushyds[A] = offrushyds/gamecount
                game.avgdefrushyds[A] = defrushyds/gamecount
                game.avgoffpassyds[A] = offpassyds/gamecount
                game.avgdefpassyds[A] = defpassyds/gamecount
                game.yardsperplay[A] = (offrushyds + offpassyds) / (rushats + passats)
                offrushyds += game.rushyds[A]
                defrushyds += game.rushyds[B]
                offpassyds += game.passyds[A]
                defpassyds += game.passyds[B]
                rushats += game.rushats[A]
                passats += game.passats[A]
            gamecount += 1.0
    return teams, games
