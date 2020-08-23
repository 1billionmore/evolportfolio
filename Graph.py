
import random
import numpy as np

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()
class Node:
	def __init__(self, value, incoming=[], outgoing=[]):
		self.value = value
		self.contents = []
		self.outputvalue = 0
		self.incoming = incoming
		self.outgoing = outgoing
	def __str__(self):
		return str(self.value)

class Edge:

	def __init__(self, start, dest, weight, bias=0):
		# NEEDS TO BE REORGANIZED as
		self.info = {dest: (weight, bias)}
		self.start = start
		self.dest = dest
		self.weight = weight
		self.bias = bias

class Graph:



	def __init__(self):

		self.layers =[]
		self.start = None
		self.edges = {}

	def _addEdge(self, start, n, weightEdge):
		newEdge = Edge(start, n, weightEdge, 0)

		if start in self.edges:
			self.edges[start].append(newEdge)
		else:
			self.edges[start] = [newEdge]
		return newEdge
		

	def addVertex(self, value):

		vtx = self._find(value)
		if not self.start and vtx:
			self.start = vtx

		if vtx == None:
			n = Node(value, [], [])
			if self.start == None:
				self.start = n
			self.edges[n] =[]
			return n
		return vtx


	def edgeExists(self, startValue, value):
		v1 = self._find(startValue)
		v2 = self._find(value)

		if v1 and v2:

			vtxEdges = self.edges[v1]

			for edge in vtxEdges:
				if edge.dest == v2:
					return True

		return False


	
	def addNodeConnectedToVertex(self, startValue, value, weightEdge):

		start = self._find(startValue)
		if start:

			alreadyThere = False

			n = self.addVertex(value)

			if n:
				vtxEdges = self.edges[start]

				for edge in vtxEdges:
					if edge.dest == n:
						alreadyThere = True
			if not alreadyThere:
				newEdge = self._addEdge(start, n, weightEdge)
				n.incoming.append(newEdge)
				start.outgoing.append(newEdge)





	def putEdgeBetweenTwoVertices(self, id1, id2, weightEdge):
		v1 = self._find(id1)
		v2 = self._find(id2)

		if v1 and v2:
			
			newEdge = self._addEdge(v1, v2, weightEdge)
			v1.outgoing.append(newEdge)
			v2.incoming.append(newEdge)


	def _find(self, value):
		for v in self.edges:
			if v.value == value:
				return v
		return None

	def __str__(self):
		s = ""
		for v in self.edges:
			if len(self.edges[v]) or not len(v.incoming):
				s += "\"" + str(v) + "\""

				for i, edge in enumerate(self.edges[v]):
					dest = edge.dest
					if i == 0:
					 	s +=  " -> \"" + str(dest) +  "\" [label=" + str(edge.weight)+ "] ;\n"
					else:
						s += "\"" + str(v) + "\" -> \"" + str(dest) + "\" [label=" + str(edge.weight)+ "] ;\n"



		return s


	def __len__(self):
		return len(self.edges)

	def addInputLayer(self, inputSize):
		inputLayer = []
		for i in range(inputSize):

			n = self.addVertex(i)
			inputLayer.append(n)
		self.layers.append(inputLayer)
		return inputLayer



	def addFullyConnectedLayer(self, layerBefore, numNodesInLayer):
		nextLayer = []
		length = self.__len__()
		for j in range(length, length + numNodesInLayer):
			n = self.addVertex(j)
			nextLayer.append(n)
			for node in layerBefore:
				self.putEdgeBetweenTwoVertices(node.value, j, random.random())
		self.layers.append(nextLayer)
		return nextLayer

	def addConvolutionalLayer(self, layerBefore, i):
		nextLayer = []
		if i >= len(layerBefore):
			return []
		for j in range(i, len(layerBefore) + 1):
			startVertices = layerBefore[j - i:j]
			newId = len(g)
			n = self.addVertex(newId) 
			nextLayer.append(n)
			for vtx in startVertices:
				self.putEdgeBetweenTwoVertices(vtx.value, newId, random.random())
		self.layers.append(nextLayer)
		return nextLayer

	def getOutputFromLayerAsMatrix(self, i):
		layer = self.layers[i]
		return np.array([node.outputvalue for node in layer])


	def getWeightsAndBiasesAsMatrix(self, i):

		layer = self.layers[i]
		arr = np.zeros((len(self.layers[i - 1]), len(layer)))
		for i, node in enumerate(layer):
			incomingEdges = node.incoming
			for j, edge in enumerate(incomingEdges):
				arr[j][i] = edge.weight
		return arr

	def setWeights(self, arr, i):
		layer = self.layers[i]
		nRows, nCols = arr.shape
		for i in range(nRows):
			for j in range(nCols):
				wt = arr[i][j]
				layer[j].incoming[i].weight = wt


	def eval(self, data):
		if len(data) == len(self.layers[0]):
			

			for i, val in enumerate(data):
				self.layers[0][i].outputvalue = val
			outputs = data
			for i in range(1, len(self.layers)):
				wx = np.dot(outputs, self.getWeightsAndBiasesAsMatrix(i))
				outputs = np.max(wx, 0) # RELU
			return outputs
		else:
			print("LENGTH MISMATCH", data, self.layers[0])
			raise

	def predict(self, data):

		out = self.eval(data)
		soft = softmax(out)
		return np.argmax(soft)






def createGraphFile(g, file):
	with open(file, 'w+') as f:
		s = "digraph {\n"
		s += str(g)
		s += "}"
		f.write(s)


def initializeStrategy():

	g = Graph()

	inputSize = 9
	firstLayerSize = 4
	secondLayerSize = 3
	thirdLayerSize = 2
	outputSize = 9
	inputLayer = []

	inputLayer = g.addInputLayer(inputSize)
	firstLayer  = g.addFullyConnectedLayer(inputLayer, firstLayerSize)
	secondLayer = g.addFullyConnectedLayer(firstLayer, secondLayerSize)
	thirdLayer = g.addFullyConnectedLayer(secondLayer, thirdLayerSize)
	outputLayer = g.addFullyConnectedLayer(thirdLayer, outputSize)


	return g

MUTATION_RATE = 0.2
def produceChild(parent1, parent2):
	child = initializeStrategy()

	for i in range(1, len( parent1.layers)):
		layer = parent1.layers[i]
		arr1 = parent1.getWeightsAndBiasesAsMatrix(i)
		arr2 = parent2.getWeightsAndBiasesAsMatrix(i)
		randoms = np.random.rand(arr1.shape[0], arr1.shape[1])

		mean = (arr1 + arr2)  / 2

		mean[randoms < 0.25] = arr1[randoms < 0.25]
		mean[randoms > 0.75] = arr2[randoms > 0.75]
		mutationError = .2 * np.random.rand(mean.shape[0], mean.shape[1]) - 0.1
		mutationErrorMsk = np.random.rand(mean.shape[0], mean.shape[1])
		mutationError[mutationErrorMsk < 0.8] = 0
		mean = mean + mutationError

		child.setWeights(mean, i)
	return child



	





initializeStrategy()



