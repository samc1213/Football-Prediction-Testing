from pybrain.structure import FeedForwardNetwork, FullConnection
from pybrain.datasets            import ClassificationDataSet, SupervisedDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer, LinearLayer, SigmoidLayer, TanhLayer
from gamesteamsimportwithoutfcs import getMeTeamsAndGamesBitch

attributelist = ['avgoffpassydspergame', 'avgdefpassydspergame', 'avgoffrushydspergame', 'avgdefrushydspergame', 'avgyardsperplay', 'avgpointsperplay', 'avgpointsperplaymarginpergame']

def Normalize(minmaxtuple, value):
    newvalues = []
    denom = minmaxtuple[1] - minmaxtuple[0]
    return (value - minmaxtuple[0]) / denom

n = FeedForwardNetwork()
inLayer = LinearLayer(len(attributelist)*2)
hiddenLayer = SigmoidLayer(3)
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

#home, away
for gameid, game in games.iteritems():
    inputs = [Normalize(metadata['maxmins'][attr], game[attr][0]) for attr in attributelist]
    inputs.extend( [Normalize(metadata['maxmins'][attr], game[attr][1]) for attr in attributelist] )

    outputs = [game['points'][0] - game['points'][1]]
    alldata.addSample(inputs, outputs)

testdata, traindata = alldata.splitWithProportion(0.70)

print "IMPORTANT ", traindata.outdim
print "Number of training patterns: ", len(traindata)
trainer = BackpropTrainer( n, dataset=traindata, momentum=0.1, verbose=True, weightdecay=0.01)
trainer.trainEpochs(100)

totalcount = 0
rightcount = 0
sumerrors = 0.0
for data in testdata:
    inputvalues = []
    for attr in attributelist:
        inputvalues.append(Normalize(metadata['maxmins'][attr], game[attr][0]))
        inputvalues.append(Normalize(metadata['maxmins'][attr], game[attr][1]))

    expectedOutput = n.activate(data[0])
    print expectedOutput[0]

    sumerrors += abs((game['points'][0] - game['points'][1]) - expectedOutput[0])

print sumerrors/len(testdata)
