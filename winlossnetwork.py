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

teams, games, metadata = getMeTeamsAndGamesBitch()
# alldata = SupervisedDataSet(len(attributelist)*2, 1)
alldata = SupervisedDataSet(len(attributelist)*2, 2)


#home, away
for gameid, game in games.iteritems():
    inputs = [Normalize(metadata['maxmins'][attr], game[attr][0]) for attr in attributelist]
    inputs.extend( [Normalize(metadata['maxmins'][attr], game[attr][1]) for attr in attributelist] )

    if game['points'][0] > game['points'][1]:
        outputs = [1, 0]

    else:
        outputs = [0, 1]
    print outputs
    alldata.addSample(inputs, outputs)

testdata, traindata = alldata.splitWithProportion(0.70)


print "IMPORTANT ", traindata.outdim
n = buildNetwork(traindata.indim, 5, traindata.outdim, outclass=SoftmaxLayer)
print "Number of training patterns: ", len(traindata)
trainer = BackpropTrainer( n, dataset=traindata, momentum=0.1, verbose=True, weightdecay=0.01)
trainer.trainEpochs(200)
# print traindata

totalcount = 0
rightcount = 0
sumerrors = 0.0
for data in testdata:
    # print data[0]
    inputvalues = []
    for attr in attributelist:
        inputvalues.append(Normalize(metadata['maxmins'][attr], game[attr][0]))
        inputvalues.append(Normalize(metadata['maxmins'][attr], game[attr][1]))

    expectedOutput = n.activate(data[0])
    print expectedOutput
    if expectedOutput[0] > expectedOutput[1]:
        if game['points'][0] > game['points'][1]:
            rightcount +=1.0
    else:
        if game['points'][0] < game['points'][1]:
            rightcount +=1.0
    totalcount +=1.0
    # print game.points[0]-game.points[1]

print rightcount/float(totalcount)
