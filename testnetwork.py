from pybrain.structure import FeedForwardNetwork, FullConnection
from pybrain.datasets            import ClassificationDataSet, SupervisedDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer, LinearLayer, SigmoidLayer, TanhLayer
from gamesteamsimportwithoutfcs import getMeTeamsAndGamesBitch


 # newgame['date'] = gamedate
 #            newgame['gamecode'] = gamecode
 #            newgame['hometeamcode'] = hometeamcode
 #            newgame['visitteamcode'] = visitteamcode
 #            newgame['rushyds'] = [None, None]
 #            newgame['passyds'] = [None, None]
 #            newgame['rushtds'] = [None, None]
 #            newgame['passtds'] = [None, None]
 #            newgame['passats'] = [None, None]
 #            newgame['rushats'] = [None, None]
 #            newgame['points'] = [None, None]
 #            newgame['avgoffrushydspergame'] = [None, None]
 #            newgame['avgyardsperplay'] = [None, None]
 #            newgame['avgdefrushydspergame'] = [None, None]
 #            newgame['avgoffpassydspergame'] = [None, None]
 #            newgame['avgdefpassydspergame'] = [None, None]


attributelist = ['avgoffpassydspergame', 'avgdefpassydspergame', 'avgoffrushydspergame', 'avgdefrushydspergame', 'avgyardsperplay', 'avgpointsperplay', 'avgpointsperplaymarginpergame']





def Normalize(minmaxtuple, value):
    newvalues = []
    denom = minmaxtuple[1] - minmaxtuple[0]
    return (value - minmaxtuple[0]) / denom

n = FeedForwardNetwork()
inLayer = LinearLayer(len(attributelist)*2)
hiddenLayer = SigmoidLayer(3)
# outLayer = SoftmaxLayer(1)
outLayer = LinearLayer(1)


n.addInputModule(inLayer)
n.addModule(hiddenLayer)
n.addOutputModule(outLayer)

in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)

n.addConnection(in_to_hidden)
n.addConnection(hidden_to_out)

n.sortModules()

teams, games, metadata = getMeTeamsAndGamesBitch()
alldata = SupervisedDataSet(len(attributelist)*2, 1)
# alldata = ClassificationDataSet(10)




# threewintotal = 0
# threewincorrect = 0.0 
# fourwintotal = 0
# fourwincorrect = 0
# fivewintotal = 0
# fivewincorrect = 0
# for gameid, game in games.iteritems():
#     counthome = 0
#     countaway = 0
#     for attr in attributelist:
#         if game[attr][0] > game[attr][1]:
#             counthome +=1
#         else:
#             countaway +=1
#     if counthome ==3 or countaway == 3:
#         threewintotal +=1
#         if counthome > countaway:
#             if game['points'][0] > game['points'][1]:
#                 threewincorrect +=1.0
#         else:
#             if game['points'][0] < game['points'][1]:
#                 threewincorrect +=1.0
#     if counthome ==4 or countaway == 4:
#         fourwintotal +=1
#         if counthome > countaway:
#             if game['points'][0] > game['points'][1]:
#                 fourwincorrect +=1.0
#         else:
#             if game['points'][0] < game['points'][1]:
#                 fourwincorrect +=1.0
#     if counthome ==5 or countaway == 5:
#         fivewintotal +=1
#         if counthome > countaway:
#             if game['points'][0] > game['points'][1]:
#                 fivewincorrect +=1.0
#         else:
#             if game['points'][0] < game['points'][1]:
#                 fivewincorrect+=1.0

# print "Threewin ", (threewincorrect/threewintotal)
# print "4win ", (fourwincorrect/fourwintotal)
# print "5win ", (fivewincorrect/fivewintotal)


#home, away
for gameid, game in games.iteritems():
    inputs = [Normalize(metadata['maxmins'][attr], game[attr][0]) for attr in attributelist]
    inputs.extend( [Normalize(metadata['maxmins'][attr], game[attr][1]) for attr in attributelist] )

    # inputs = [game['avgoffrushydspergame'][0], game['avgoffrushydspergame'][1], game['avgoffpassydspergame'][0], game['avgoffpassydspergame'][1], game['avgdefrushydspergame'][0], game['avgdefrushydspergame'][1], game['avgdefpassydspergame'][0], game['avgdefpassydspergame'][1], game['avgyardsperplay'][0], game['avgyardsperplay'][1]]
    # inputs = [game.yardsperplay[0], game.yardsperplay[1]]
    outputs = [abs(game['points'][0] - game['points'][1])]
    alldata.addSample(inputs, outputs)

testdata, traindata = alldata.splitWithProportion(0.70)
print "Number of training patterns: ", len(traindata)
trainer = BackpropTrainer( n, dataset=traindata, momentum=0.1, verbose=True, weightdecay=0.01)
# trainer.trainUntilConvergence()
trainer.trainEpochs(50)
# print traindata

totalcount = 0
rightcount = 0
sumerrors = 0.0
for data in testdata:
    # print data[0]
    totalcount+=1
    inputvalues = []
    for attr in attributelist:
        inputvalues.append(Normalize(metadata['maxmins'][attr], game[attr][0]))
        inputvalues.append(Normalize(metadata['maxmins'][attr], game[attr][1]))
    # inputvalues.append(Normalize(metadata['maxmins']['avgoffpassydspergame'], game['avgoffpassydspergame'][0]))
    # inputvalues.append(Normalize(metadata['maxmins']['avgoffpassydspergame'], game['avgoffpassydspergame'][1]))
    # inputvalues.append(Normalize(metadata['maxmins']['avgdefrushydspergame'], game['avgdefrushydspergame'][0]))
    # inputvalues.append(Normalize(metadata['maxmins']['avgdefrushydspergame'], game['avgdefrushydspergame'][1]))
    # inputvalues.append(Normalize(metadata['maxmins']['avgdefpassydspergame'], game['avgdefpassydspergame'][0]))
    # inputvalues.append(Normalize(metadata['maxmins']['avgdefpassydspergame'], game['avgdefpassydspergame'][1]))
    # inputvalues.append(Normalize(metadata['maxmins']['avgyardsperplay'], game['avgyardsperplay'][0]))
    # inputvalues.append(Normalize(metadata['maxmins']['avgyardsperplay'], game['avgyardsperplay'][1]))
    # inputvalues.append(Normalize(metadata['maxmins']['avgpointsperplay'], game['avgpointsperplay'][0]))
    # inputvalues.append(Normalize(metadata['maxmins']['avgpointsperplay'], game['avgpointsperplay'][1]))
    expectedOutput = n.activate(data[0])
    print expectedOutput
    # print game.points[0]-game.points[1]

    sumerrors += abs((abs(game['points'][0] - game['points'][1])) - expectedOutput[0])

print sumerrors/len(games)
    # print rightcount / float(totalcount)
