'''
This file includes FCS teams that may only play 1 game. In fact 59 teams have played only 1 game.
Therefore, some long-run summing might get messed up.
'''


import csv
import datetime

def GetMaxMins(attribute, games):
    combined = []
    for key, game in games.iteritems():
        combined.append(game[attribute][0])
        combined.append(game[attribute][1])
    return max(combined), min(combined)

def GetAverage(attribute, games):
    return sum([g[attribute][0] + g[attribute][1] for key, g in games.iteritems()])/(len(games) * 2)

class Team:
    def __init__(self, name=None, games=None):
        if games is None:
            self.games = []
        self.name = name

# class Game:
#     def __init__(self, date, gamecode, hometeamcode, visitteamcode, rushyds=None, passyds=None, rushtds=None, passtds=None, points=None, avgoffrushyds=None, avgdefrushyds=None, avgoffpassyds=None, avgdefpassyds=None, passats=None, rushats=None,  yardsperplay=None):
#         self.date = date
#         self.hometeamcode = hometeamcode
#         self.visitteamcode = visitteamcode
#         self.gamecode = gamecode
#         if rushyds is None:
#             self.rushyds = [None, None]
#         if passyds is None:
#             self.passyds = [None, None]
#         if points is None:
#             self.points = [None, None]
#         if rushtds is None:
#             self.rushtds = [None, None]
#         if passtds is None:
#             self.passtds = [None, None]
#         if avgoffrushyds is None:
#             self.avgoffrushyds = [None, None]
#         if avgdefrushyds is None:
#             self.avgdefrushyds = [None, None]
#         if avgdefpassyds is None:
#             self.avgdefpassyds = [None, None]
#         if avgoffpassyds is None:
#             self.avgoffpassyds = [None, None]
#         if passats is None:
#             self.passats = [None, None]
#         if rushats is None:
#             self.rushats = [None, None]
#         if yardsperplay is None:
#             self.yardsperplay = [None, None]
    # def getAttr(self, str):
    #     return self[str]

def getMeTeamsAndGamesBitch(badteamsout=True):
    teams = {}
    games = {}

    with open('data/2013/game.csv') as game:
        for row in csv.DictReader(game):
            visitteamcode = int(row['Visit Team Code'])
            hometeamcode = int(row['Home Team Code'])
            gamecode = int(row['Game Code'])
            gamedate = datetime.datetime.strptime(row['Date'], '%m/%d/%Y').date()

            newgame = {}
            newgame['date'] = gamedate
            newgame['gamecode'] = gamecode
            newgame['hometeamcode'] = hometeamcode
            newgame['visitteamcode'] = visitteamcode
            newgame['rushyds'] = [None, None]
            newgame['passyds'] = [None, None]
            newgame['rushtds'] = [None, None]
            newgame['passtds'] = [None, None]
            newgame['passats'] = [None, None]
            newgame['rushats'] = [None, None]
            newgame['points'] = [None, None]
            newgame['avgoffrushyds'] = [None, None]
            newgame['avgdefrushyds'] = [None, None]
            newgame['avgoffpassyds'] = [None, None]
            newgame['avgdefpassyds'] = [None, None]
            newgame['yardsperplay'] = [None, None]
            games[gamecode] = newgame

    with open('data/2013/team-game-statistics.csv') as gamestats:
        for row in csv.DictReader(gamestats):
            gamecode = int(row['Game Code'])
            rowTeamCode = int(row['Team Code'])
            rowGame = games[gamecode]
            # rowGame['gamecode'] = gamecode
            # HOME, AWAY!!!! HOME, AWAY in ze lists
            if rowGame['hometeamcode'] == rowTeamCode:
                rowGame['rushyds'][0] = int(row['Rush Yard'])
                rowGame['passyds'][0] = int(row['Pass Yard'])
                rowGame['rushtds'][0] = int(row['Rush TD'])
                rowGame['passtds'][0] = int(row['Pass TD'])
                rowGame['passats'][0] = int(row['Pass Att'])
                rowGame['rushats'][0] = int(row['Rush Att'])
                rowGame['points'][0] = int(row['Points'])
            else:
                rowGame['rushyds'][1] = int(row['Rush Yard'])
                rowGame['passyds'][1] = int(row['Pass Yard'])
                rowGame['rushtds'][1] = int(row['Rush TD'])
                rowGame['passtds'][1] = int(row['Pass TD'])
                rowGame['passats'][1] = int(row['Pass Att'])
                rowGame['rushats'][1] = int(row['Rush Att'])
                rowGame['points'][1] = int(row['Points'])
            if rowTeamCode not in teams:
                teams[rowTeamCode] = Team()

            teams[rowTeamCode].games.append(gamecode)

    for code, team in teams.iteritems():
        team.games.sort(key=lambda x: games[x]['date'])

    badteams = []
    badgames = []

# get rid of all teams with less than 10 games
    for code, team in teams.iteritems():
        if len(team.games) < 10:
            badteams.append(code)
            if badteamsout:
                for g in team.games:
                    badgames.append(g)
    for g in badgames:

        homecode = games[g]['hometeamcode']
        visitcode = games[g]['visitteamcode']
        if (g == 317000520130907):
            print homecode
            print visitcode
            # print teams[homecode].games
            #  & (homecode == 5 | visitcode == 5):
            print "GODDAMN"
        for i in range(len(teams[homecode].games)):
            if teams[homecode].games[i] == g:
                del teams[homecode].games[i]
                break
        for i in range(len(teams[visitcode].games)):
            if teams[visitcode].games[i] == g:
                del teams[visitcode].games[i]
                break
        del games[g]

    for t in badteams:
        del teams[t]

    for teamid, team in teams.iteritems():
        offrushyds = 0
        offpassyds = 0
        defrushyds = 0
        defpassyds = 0
        rushats = 0
        passats = 0
        gamecount = 0.0
        firstgame = True
        print teamid
        for g in range(len(team.games)):
            gamecode = team.games[g]
            if games[gamecode]['hometeamcode'] == teamid:
                A = 0
                B = 1
            elif games[gamecode]['visitteamcode'] == teamid:
                A = 1
                B = 0
            else:
                print "ERROR"
            if firstgame:
                games[gamecode]['avgoffrushyds'][A] = offrushyds
                games[gamecode]['avgdefrushyds'][A] = defrushyds
                games[gamecode]['avgoffpassyds'][A] = offpassyds
                games[gamecode]['avgdefpassyds'][A] = defpassyds
                games[gamecode]['yardsperplay'][A] = 0
                firstgame = False
                offrushyds += games[gamecode]['rushyds'][A]
                defrushyds += games[gamecode]['rushyds'][B]
                offpassyds += games[gamecode]['passyds'][A]
                defpassyds += games[gamecode]['passyds'][B]
                rushats += games[gamecode]['rushats'][A]
                passats += games[gamecode]['passats'][A]
            else:
                games[gamecode]['avgoffrushyds'][A] = offrushyds/gamecount
                games[gamecode]['avgdefrushyds'][A] = defrushyds/gamecount
                games[gamecode]['avgoffpassyds'][A] = offpassyds/gamecount
                games[gamecode]['avgdefpassyds'][A] = defpassyds/gamecount
                games[gamecode]['yardsperplay'][A] = (offrushyds + offpassyds) / (rushats + passats)
                offrushyds += games[gamecode]['rushyds'][A]
                defrushyds += games[gamecode]['rushyds'][B]
                offpassyds += games[gamecode]['passyds'][A]
                defpassyds += games[gamecode]['passyds'][B]
                rushats += games[gamecode]['rushats'][A]
                passats += games[gamecode]['passats'][A]
            gamecount += 1.0
    firstgames = []
    for code, team in teams.iteritems():
        if team.games[0] not in firstgames:
            firstgames.append(team.games[0])
            del team.games[0]
    for g in firstgames:
        del games[g]

    metadata = {}
    metadata['maxmins'] = {}
    metadata['averages'] = {}
    metadata['maxmins']['avgoffrushyds'] = GetMaxMins('avgoffrushyds', games)
    metadata['maxmins']['avgdefrushyds'] = GetMaxMins('avgdefrushyds', games)
    metadata['maxmins']['avgoffpassyds'] = GetMaxMins('avgoffpassyds', games)
    metadata['maxmins']['avgdefpassyds'] = GetMaxMins('avgdefpassyds', games)
    metadata['maxmins']['yardsperplay'] = GetMaxMins('yardsperplay', games)
    metadata['averages']['points'] = GetAverage('points', games)

    return teams, games, metadata
