'''
This file includes FCS teams that may only play 1 game. In fact 59 teams have played only 1 game.
Therefore, some long-run summing might get messed up.
'''


import csv
import datetime

attributelist = [
    'avgoffpassydspergame',
    'avgdefpassydspergame',
    'avgoffrushydspergame',
    'avgdefrushydspergame',
    'avgyardsperplay',
    'avgpointsperplay',
    'avgpointsperplaymarginpergame',
    'successrate',
    'avgthirddownconversionspergame',
    'avgstartingpositionpergame']

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

def GetSuccessRateAttributes(gamecode, teamcode, playsingame):
    totaloffplays = 0.0
    successfuloffplays = 0.0
    for playnumber, play in playsingame.iteritems():
        try:
            notturnover = playsingame[playnumber+1]['offteamcode']==teamcode
        except KeyError:
            notturover = True
        rushorpass = (play['playtype'] == 'RUSH') or (play['playtype'] == 'PASS')
        if play['offteamcode'] == teamcode:
            if ((play['down'] == 1) & rushorpass & notturnover):
                totaloffplays +=1.0
                if play['yards']/float(play['distance']) >= 0.5:
                    successfuloffplays +=1.0
            elif ((play['down'] == 2) & rushorpass & (notturnover)):
                totaloffplays +=1.0
                if play['yards']/float(play['distance']) >= 0.7:
                    successfuloffplays +=1.0
            elif (play['down'] == 3 or play['down'] ==4) & rushorpass & notturnover:
                totaloffplays +=1.0
                if play['yards']/float(play['distance']) >= 1.0:
                    successfuloffplays +=1.0
    return totaloffplays, successfuloffplays


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
            newgame['avgstartingpositionpergame'] = [None, None]
            newgame['successrate'] = [None, None]
            newgame['thirddownconversions'] = [None, None]
            newgame['avgthirddownconversionspergame'] = [None, None]
            newgame['startingpositiongameavg'] = [None, None]
            games[gamecode] = newgame

    lastwasthird = False
    # with open('data/2013/play.csv') as playfile:
    #     for row in csv.DictReader(playfile):
    #         down = int(row['Down'])
    #         gamecode = int(row['Game Code'])
    #         currentoffteam = int(row['Offense Team'])
    #         if down == 3:
    #             lastwasthird = True
    #         else:
    #             lastwasthird = False
    #         if down == 1 and lastwasthird == True and currentoffteam != lastoffensiveteam:
    #             games[]
    #         lastoffensiveteam = offteam

    rushes = {}
    with open('data/2013/rush.csv') as rushfile:
        for row in csv.DictReader(rushfile):
            gamecode = int(row['Game Code'])
            playnumber = int(row['Play Number'])
            teamcode = int(row['Team Code'])
            playercode = int(row['Player Code'])
            attempt = int(row['Attempt'])
            yards = int(row['Yards'])
            touchdown = bool(row['Touchdown'])
            firstdown = bool(row['1st Down'])
            sack = bool(row['Sack'])
            fumble = bool(row['Fumble'])
            fumblelost = bool(row['Fumble Lost'])
            safety = bool(row['Safety'])
            if gamecode not in rushes:
                rushes[gamecode] = {}
            rushes[gamecode][playnumber] = {}
            rushes[gamecode][playnumber]['teamcode'] = teamcode
            rushes[gamecode][playnumber]['playercode'] = playercode
            rushes[gamecode][playnumber]['attempt'] = attempt
            rushes[gamecode][playnumber]['yards'] = yards
            rushes[gamecode][playnumber]['touchdown'] = touchdown
            rushes[gamecode][playnumber]['firstdown'] = firstdown
            rushes[gamecode][playnumber]['sack'] = sack
            rushes[gamecode][playnumber]['fumble'] = fumble
            rushes[gamecode][playnumber]['fumblelost'] = fumblelost
            rushes[gamecode][playnumber]['safety'] = safety

    passes = {}
    with open('data/2013/pass.csv') as passfile:
        for row in csv.DictReader(passfile):
            gamecode = int(row['Game Code'])
            playnumber = int(row['Play Number'])
            teamcode = int(row['Team Code'])
            passercode = int(row['Passer Player Code'])
            #receiver code can be nothing if pass incomplete
            try:
                receivercode = int(row['Receiver Player Code'])
            except ValueError:
                receivercode = -1
            attempt = int(row['Attempt'])
            completion = bool(row['Completion'])
            yards = int(row['Yards'])
            touchdown = bool(row['Touchdown'])
            interception = bool(row['Interception'])
            firstdown = bool(row['1st Down'])
            dropped = bool(row['Dropped'])
            if gamecode not in passes:
                passes[gamecode] = {}
            passes[gamecode][playnumber] = {}
            passes[gamecode][playnumber]['teamcode'] = teamcode
            passes[gamecode][playnumber]['passercode'] = playercode
            passes[gamecode][playnumber]['receivercode'] = attempt
            passes[gamecode][playnumber]['yards'] = yards
            passes[gamecode][playnumber]['touchdown'] = touchdown
            passes[gamecode][playnumber]['firstdown'] = firstdown
            passes[gamecode][playnumber]['attempt'] = attempt
            passes[gamecode][playnumber]['interception'] = interception
            passes[gamecode][playnumber]['dropped'] = dropped

    plays = {}
    with open('data/2013/play.csv') as playsfile:
        for row in csv.DictReader(playsfile):
            gamecode = int(row['Game Code'])
            playnumber = int(row['Play Number'])
            periodnumber = int(row['Period Number'])
            try:
                clock = int(row['Clock'])
            except ValueError:
                clock = -1
            offteamcode = int(row['Offense Team Code'])
            defteamcode = int(row['Defense Team Code'])
            offteampts = int(row['Offense Points'])
            defteampts = int(row['Defense Points'])
            try:
                down = int(row['Down'])
            except ValueError:
                down = 0
            try:
                distance = int(row['Distance'])
            except ValueError:
                distance = -1
            spot = int(row['Spot'])
            playtype = str(row['Play Type'])
            try:
                drivenumber = int(row['Drive Number'])
            except ValueError:
                drivenumber = 0
            try:
                driveplay = int(row['Drive Play'])
            except ValueError:
                driveplay = 0
            if gamecode not in plays:
                plays[gamecode] = {}
            plays[gamecode][playnumber] = {}
            plays[gamecode][playnumber]['periodnumber'] = periodnumber
            plays[gamecode][playnumber]['clock'] = clock
            plays[gamecode][playnumber]['offteamcode'] =offteamcode
            plays[gamecode][playnumber]['defteamcode'] = defteamcode
            plays[gamecode][playnumber]['offteampts'] = offteampts
            plays[gamecode][playnumber]['defteampts'] = defteampts
            plays[gamecode][playnumber]['down'] = down
            plays[gamecode][playnumber]['distance'] = distance
            plays[gamecode][playnumber]['spot'] = spot
            plays[gamecode][playnumber]['playtype'] = playtype
            plays[gamecode][playnumber]['drivenumber'] = drivenumber
            plays[gamecode][playnumber]['driveplay'] = driveplay
            if plays[gamecode][playnumber]['playtype'] == 'RUSH':
                plays[gamecode][playnumber]['yards'] = rushes[gamecode][playnumber]['yards']
            elif plays[gamecode][playnumber]['playtype'] == 'PASS':
                plays[gamecode][playnumber]['yards'] = passes[gamecode][playnumber]['yards']
            else:
                plays[gamecode][playnumber]['yards'] = None

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
                homethirddownconversions = [play for playnumber, play in plays[gamecode].iteritems() if (play['offteamcode'] == rowTeamCode) & (play['down'] == 3) & (play['yards'] > play['distance']) & ((play['playtype'] == 'RUSH') | (play['playtype'] == 'PASS'))]
                rowGame['thirddownconversions'][0] = len(homethirddownconversions)
                homedrivestartplays = []
                for pn, p in plays[gamecode].iteritems():
                    if p['offteamcode'] == rowTeamCode:
                        try:
                            if plays[gamecode][pn - 1]['offteamcode'] != rowTeamCode:
                                homedrivestartplays.append(p)
                        except KeyError:
                            pass
                homestartingposgameavg = sum([p['spot'] for p in homedrivestartplays])/len(homedrivestartplays)
                rowGame['startingpositiongameavg'][0] = homestartingposgameavg
            else:
                rowGame['rushyds'][1] = int(row['Rush Yard'])
                rowGame['passyds'][1] = int(row['Pass Yard'])
                rowGame['rushtds'][1] = int(row['Rush TD'])
                rowGame['passtds'][1] = int(row['Pass TD'])
                rowGame['passats'][1] = int(row['Pass Att'])
                rowGame['rushats'][1] = int(row['Rush Att'])
                rowGame['points'][1] = int(row['Points'])
                awaythirddownconversions = [play for playnumber, play in plays[gamecode].iteritems() if (play['offteamcode'] == rowTeamCode) & (play['down'] == 3) & (play['yards'] > play['distance']) & ((play['playtype'] == 'RUSH') | (play['playtype'] == 'PASS'))]
                rowGame['thirddownconversions'][1] = len(awaythirddownconversions)
                awaydrivestartplays = []
                for pn, p in plays[gamecode].iteritems():
                    if p['offteamcode'] == rowTeamCode:
                        try:
                            if plays[gamecode][pn - 1]['offteamcode'] != rowTeamCode:
                                awaydrivestartplays.append(p)
                        except KeyError:
                            pass
                awaystartingposgameavg = sum([p['spot'] for p in awaydrivestartplays])/len(awaydrivestartplays)
                rowGame['startingpositiongameavg'][1] = awaystartingposgameavg
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
        successfuloffplays = 0.0
        totaloffplays = 0.0
        offrushyds = 0
        offpassyds = 0
        defrushyds = 0
        defpassyds = 0
        rushats = 0
        passats = 0
        points = 0.0
        thirddownconversions = 0
        gamecount = 0.0
        margin = 0.0
        drivestartingpositions = 0
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
                games[gamecode]['avgpointsperplaymarginpergame'][A] = 0
                games[gamecode]['successrate'][A] = 0
                games[gamecode]['avgthirddownconversionspergame'][A] = 0
                games[gamecode]['startingpositiongameavg'][A] = 0

                firstgame = False
                offrushyds += games[gamecode]['rushyds'][A]
                defrushyds += games[gamecode]['rushyds'][B]
                offpassyds += games[gamecode]['passyds'][A]
                defpassyds += games[gamecode]['passyds'][B]
                rushats += games[gamecode]['rushats'][A]
                passats += games[gamecode]['passats'][A]
                points += games[gamecode]['points'][A]
                margin += (games[gamecode]['points'][A] / float(games[gamecode]['rushats'][A]+ games[gamecode]['passats'][A])) - (games[gamecode]['points'][B]/ float(games[gamecode]['rushats'][B]+games[gamecode]['passats'][B]))
                thirddownconversions += games[gamecode]['thirddownconversions'][A]
                drivestartingpositions += games[gamecode]['startingpositiongameavg'][A]
                totaloffplaystemp, successfuloffplaystemp = GetSuccessRateAttributes(gamecode, teamid, plays[gamecode])
                successfuloffplays += successfuloffplaystemp
                totaloffplays += totaloffplaystemp
            else:
                games[gamecode]['avgoffrushydspergame'][A] = offrushyds/gamecount
                games[gamecode]['avgdefrushydspergame'][A] = defrushyds/gamecount
                games[gamecode]['avgoffpassydspergame'][A] = offpassyds/gamecount
                games[gamecode]['avgdefpassydspergame'][A] = defpassyds/gamecount
                games[gamecode]['avgyardsperplay'][A] = (offrushyds + offpassyds) / float(rushats + passats)
                games[gamecode]['avgpointsperplay'][A] = points/float(rushats+passats)
                games[gamecode]['avgpointsperplaymarginpergame'][A] = margin/(gamecount)
                games[gamecode]['successrate'][A] = successfuloffplays/totaloffplays
                games[gamecode]['avgthirddownconversionspergame'][A] = thirddownconversions/gamecount
                games[gamecode]['avgstartingpositionpergame'][A] = drivestartingpositions/gamecount
                offrushyds += games[gamecode]['rushyds'][A]
                defrushyds += games[gamecode]['rushyds'][B]
                offpassyds += games[gamecode]['passyds'][A]
                defpassyds += games[gamecode]['passyds'][B]
                rushats += games[gamecode]['rushats'][A]
                passats += games[gamecode]['passats'][A]
                points += games[gamecode]['points'][A]
                thirddownconversions += games[gamecode]['thirddownconversions'][A]
                margin += (games[gamecode]['points'][A] / float(games[gamecode]['rushats'][A]+ games[gamecode]['passats'][A])) - (games[gamecode]['points'][B]/ float(games[gamecode]['rushats'][B]+games[gamecode]['passats'][B]))
                drivestartingpositions += games[gamecode]['startingpositiongameavg'][A]
                totaloffplaystemp, successfuloffplaystemp = GetSuccessRateAttributes(gamecode, teamid, plays[gamecode])
                successfuloffplays += successfuloffplaystemp
                totaloffplays += totaloffplaystemp
            gamecount += 1.0
    firstgames = []
    for code, team in teams.iteritems():
        if team.games[0] not in firstgames:
            firstgames.append(team.games[0])
            del team.games[0]
    for g in firstgames:
        del games[g]
#
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
    metadata['maxmins']['successrate'] = GetMaxMins('successrate', games)
    metadata['maxmins']['avgthirddownconversionspergame'] = GetMaxMins('avgthirddownconversionspergame', games)
    metadata['maxmins']['avgstartingpositionpergame'] = GetMaxMins('avgstartingpositionpergame', games)
#
#     print metadata
    return teams, games, metadata
teams, games, metadata = getMeTeamsAndGamesBitch()
