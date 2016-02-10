from pybrain.structure import FeedForwardNetwork, FullConnection
from pybrain.datasets            import ClassificationDataSet, SupervisedDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer, LinearLayer, SigmoidLayer, TanhLayer
from gamesteamsimportwithoutfcs import getMeTeamsAndGamesBitch

def Normalize(minmaxtuple, value):
    newvalues = []
    denom = minmaxtuple[1] - minmaxtuple[0]
    return (value - minmaxtuple[0]) / denom

n = FeedForwardNetwork()
inLayer = LinearLayer(10)
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
alldata = SupervisedDataSet(10, 1)
# alldata = ClassificationDataSet(10)

#home, away
for gameid, game in games.iteritems():
    inputs = [game['avgoffrushyds'][0], game['avgoffrushyds'][1], game['avgoffpassyds'][0], game['avgoffpassyds'][1], game['avgdefrushyds'][0], game['avgdefrushyds'][1], game['avgdefpassyds'][0], game['avgdefpassyds'][1], game['yardsperplay'][0], game['yardsperplay'][1]]
    # inputs = [game.yardsperplay[0], game.yardsperplay[1]]
    outputs = [(game['points'][0] - game['points'][1])]
    alldata.addSample(inputs, outputs)

testdata, traindata = alldata.splitWithProportion(0.25)
print "Number of training patterns: ", len(traindata)
trainer = BackpropTrainer( n, dataset=traindata, momentum=0.1, verbose=True, weightdecay=0.01)
trainer.trainEpochs(19)
# print traindata

totalcount = 0
rightcount = 0
for gameid, game in games.iteritems():
    totalcount+=1
    normavgoffrushydshome = Normalize(metadata['maxmins']['avgoffrushyds'], game['avgoffrushyds'][0])
    normavgoffrushydsaway = Normalize(metadata['maxmins']['avgoffrushyds'], game['avgoffrushyds'][1])
    normavgoffpassydshome = Normalize(metadata['maxmins']['avgoffpassyds'], game['avgoffpassyds'][0])
    normavgoffpassydsaway = Normalize(metadata['maxmins']['avgoffpassyds'], game['avgoffpassyds'][1])
    normavgdefrushydshome = Normalize(metadata['maxmins']['avgdefrushyds'], game['avgdefrushyds'][0])
    normavgdefrushydsaway = Normalize(metadata['maxmins']['avgdefrushyds'], game['avgdefrushyds'][1])
    normavgdefpassydshome = Normalize(metadata['maxmins']['avgdefpassyds'], game['avgdefpassyds'][0])
    normavgdefpassydsaway = Normalize(metadata['maxmins']['avgdefpassyds'], game['avgdefpassyds'][1])
    normyardsperplayhome = Normalize(metadata['maxmins']['yardsperplay'], game['yardsperplay'][0])
    normyardsperplayaway = Normalize(metadata['maxmins']['yardsperplay'], game['yardsperplay'][1])

    inputs = [normavgoffrushydshome, normavgoffrushydsaway, normavgoffpassydshome, normavgoffpassydsaway, normavgdefrushydshome, normavgdefrushydsaway, normavgdefpassydshome, normavgdefpassydsaway, normyardsperplayhome, normyardsperplayaway]
    expectedOutput = n.activate(inputs)
    print expectedOutput
    # print game.points[0]-game.points[1]
    if ((game.points[0] - game.points[1])>0) == expectedOutput:
        rightcount += 1
    # print rightcount / float(totalcount)
