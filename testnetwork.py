from pybrain.structure import FeedForwardNetwork, FullConnection
from pybrain.datasets            import ClassificationDataSet, SupervisedDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer, LinearLayer, SigmoidLayer, TanhLayer
from testing import getMeTeamsAndGamesBitch



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




teams, games = getMeTeamsAndGamesBitch()
alldata = SupervisedDataSet(10, 1)
# alldata = ClassificationDataSet(10)

#home, away
for gameid, game in games.iteritems():
    inputs = [game.avgoffrushyds[0], game.avgoffrushyds[1], game.avgoffpassyds[0], game.avgoffpassyds[1], game.avgdefrushyds[0], game.avgdefrushyds[1], game.avgdefpassyds[0], game.avgdefpassyds[1], game.yardsperplay[0], game.yardsperplay[1]]
    # inputs = [game.yardsperplay[0], game.yardsperplay[1]]
    outputs = [(game.points[0] - game.points[1])]
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
    inputs = [game.avgoffrushyds[0], game.avgoffrushyds[1], game.avgoffpassyds[0], game.avgoffpassyds[1], game.avgdefrushyds[0], game.avgdefrushyds[1], game.avgdefpassyds[0], game.avgdefpassyds[1], game.yardsperplay[0], game.yardsperplay[1]]
    expectedOutput = n.activate(inputs)
    print expectedOutput
    print game.points[0]-game.points[1]
    if ((game.points[0] - game.points[1])>0) == expectedOutput:
        rightcount += 1
    print rightcount / float(totalcount)
