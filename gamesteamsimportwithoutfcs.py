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
    return min(combined), max(combined)

def GetAverage(attribute, games):
    return sum([g[attribute][0] + g[attribute][1] for key, g in games.iteritems()])/(len(games) * 2)

def GetAverageDifferential(attribute, games):
    return sum([abs(float(g[attribute][0]) - g[attribute][1]) for key, g in games.iteritems()])/(len(games))

class Team:
    def __init__(self, name=None, games=None):
        if games is None:
            self.games = []
        self.name = name

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
            newgame['avgoffrushydspergame'] = [None, None]
            newgame['avgdefrushydspergame'] = [None, None]
            newgame['avgoffpassydspergame'] = [None, None]
            newgame['avgdefpassydspergame'] = [None, None]
            newgame['avgyardsperplay'] = [None, None]
            newgame['avgpointsperplay'] = [None, None]
            newgame['avgpointsperplaymarginpergame'] = [None, None]
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
            # print homecode
            # print visitcode
            # print teams[homecode].games
            #  & (homecode == 5 | visitcode == 5):
            # print "GODDAMN"
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
        points = 0.0
        gamecount = 0.0
        margin = 0.0
        firstgame = True
        # print teamid
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
                games[gamecode]['avgoffrushydspergame'][A] = offrushyds
                games[gamecode]['avgdefrushydspergame'][A] = defrushyds
                games[gamecode]['avgoffpassydspergame'][A] = offpassyds
                games[gamecode]['avgdefpassydspergame'][A] = defpassyds
                games[gamecode]['avgyardsperplay'][A] = 0
                games[gamecode]['avgpointsperplay'][A] = 0
                print type(games[gamecode]['avgpointsperplaymarginpergame'])
                games[gamecode]['avgpointsperplaymarginpergame'][A] = 0

                firstgame = False
                offrushyds += games[gamecode]['rushyds'][A]
                defrushyds += games[gamecode]['rushyds'][B]
                offpassyds += games[gamecode]['passyds'][A]
                defpassyds += games[gamecode]['passyds'][B]
                rushats += games[gamecode]['rushats'][A]
                passats += games[gamecode]['passats'][A]
                points += games[gamecode]['points'][A]
                margin += (games[gamecode]['points'][A] / float(games[gamecode]['rushats'][A]+ games[gamecode]['passats'][A])) - (games[gamecode]['points'][B]/ float(games[gamecode]['rushats'][B]+games[gamecode]['passats'][B]))
            else:
                games[gamecode]['avgoffrushydspergame'][A] = offrushyds/gamecount
                games[gamecode]['avgdefrushydspergame'][A] = defrushyds/gamecount
                games[gamecode]['avgoffpassydspergame'][A] = offpassyds/gamecount
                games[gamecode]['avgdefpassydspergame'][A] = defpassyds/gamecount
                games[gamecode]['avgyardsperplay'][A] = (offrushyds + offpassyds) / float(rushats + passats)
                games[gamecode]['avgpointsperplay'][A] = points/float(rushats+passats)
                games[gamecode]['avgpointsperplaymarginpergame'][A] = margin/(gamecount)
                offrushyds += games[gamecode]['rushyds'][A]
                defrushyds += games[gamecode]['rushyds'][B]
                offpassyds += games[gamecode]['passyds'][A]
                defpassyds += games[gamecode]['passyds'][B]
                rushats += games[gamecode]['rushats'][A]
                passats += games[gamecode]['passats'][A]
                points += games[gamecode]['points'][A]
                margin += (games[gamecode]['points'][A] / float(games[gamecode]['rushats'][A]+ games[gamecode]['passats'][A])) - (games[gamecode]['points'][B]/ float(games[gamecode]['rushats'][B]+games[gamecode]['passats'][B]))

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
    metadata['maxmins']['avgoffrushydspergame'] = GetMaxMins('avgoffrushydspergame', games)
    metadata['maxmins']['avgdefrushydspergame'] = GetMaxMins('avgdefrushydspergame', games)
    metadata['maxmins']['avgoffpassydspergame'] = GetMaxMins('avgoffpassydspergame', games)
    metadata['maxmins']['avgdefpassydspergame'] = GetMaxMins('avgdefpassydspergame', games)
    metadata['maxmins']['avgpointsperplaymarginpergame'] = GetMaxMins('avgpointsperplaymarginpergame', games)
    metadata['maxmins']['avgyardsperplay'] = GetMaxMins('avgyardsperplay', games)
    metadata['maxmins']['avgpointsperplay'] = GetMaxMins('avgpointsperplay', games)
    metadata['averages']['points'] = GetAverage('points', games)
    metadata['averages']['pointdifferential'] = GetAverageDifferential('points', games)

    print metadata
    return teams, games, metadata
