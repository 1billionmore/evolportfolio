from Robot import Robot
import Graph
import math
import random

class NeuralRobot(Robot):

    def __init__(self, parents=[], children=[]):
        self.wins = 0
        self.ties = 0
        self.losses = 0
        self.idx = 0
        self.age = 0
        self.alive = True
        self.numChildren = 0
        self.gender = 1
         # 0 for female, 1 for male
        self.parent = parents
        self.aveMoves = 0
        self.spouses = {}
        self.strategy = None
        if len(parents) == 0:
            self.strategy = Graph.initializeStrategy()
        elif len(parents) == 2:
            self.strategy = Graph.produceChild(parents[0].strategy, parents[1].strategy)

    def getMove(self, arr):
        arr = [item for sublist in arr for item in sublist]
        a = self.strategy.predict(arr)
        return math.floor(a / 3), a % 3

    def addChild(self, otherParent, child=None):

        self.incrementAge()
        
        gender = random.randint(0, 1)

        if child == None: 
            child = NeuralRobot(parents=[self, otherParent])

        if otherParent not in self.spouses:
            self.spouses[otherParent] = [child]
        else:
            self.spouses[otherParent].append(child)

        if child not in otherParent.getChildren():
            otherParent.addChild(self, child)
        self.numChildren += 1
        return child

