from pybrain.structure import FeedForwardNetwork, FullConnection
from pybrain.datasets            import ClassificationDataSet, SupervisedDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer, LinearLayer, SigmoidLayer
from testing import getMeTeamsAndGamesBitch



n = FeedForwardNetwork()
inLayer = LinearLayer(8)
hiddenLayer = SigmoidLayer(3)
outLayer = LinearLayer(2)

n.addInputModule(inLayer)
n.addModule(hiddenLayer)
n.addOutputModule(outLayer)

in_to_hidden = FullConnection(inLayer, hiddenLayer)
hidden_to_out = FullConnection(hiddenLayer, outLayer)

n.addConnection(in_to_hidden)
n.addConnection(hidden_to_out)

n.sortModules()




teams, games = getMeTeamsAndGamesBitch()
alldata = SupervisedDataSet(8, 2)

#home, away
for gameid, game in games.iteritems():
    inputs = [game.avgoffrushyds[0], game.avgoffrushyds[1], game.avgoffpassyds[0], game.avgoffpassyds[1], game.avgdefrushyds[0], game.avgdefrushyds[1], game.avgdefpassyds[0], game.avgdefpassyds[1]]
    outputs = [game.points[0], game.points[1]]
    alldata.addSample(inputs, outputs)

testdata, traindata = alldata.splitWithProportion(0.25)
print "Number of training patterns: ", len(traindata)
trainer = BackpropTrainer( n, dataset=traindata, momentum=0.1, verbose=True, weightdecay=0.01)
trainer.trainUntilConvergence()
print traindata




