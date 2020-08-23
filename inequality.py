import random
import parameters
from anytree import Node, RenderTree, NodeMixin
import copy
import numpy as np
import matplotlib.pyplot as plt

MAX_AGE = 6
BASED_ON_WEALTH = 1
RANDOM_MATING = 2
MUTATION_SCALAR = 5
WEALTH_SELECTION_STRENGTH = 1


def averageWealth(parents):
	if len(parents) == 2:
		return (parents[0].wealth + parents[1].wealth) / 2 + MUTATION_SCALAR * (random.random() - 0.5)
	elif len(parents) == 0:
		return random.randint(100, 110)

def bernoulli(p):
	i = random.random()
	if i < p:
		return True
	else:
		return False

class Individual:
	
	def __init__(self, idx, gender, parents=[], children=[], drug_strat=None):

		self.idx = idx
		self.age = 0
		self.alive = True
		self.numChildren = 0
		self.gender = gender # 0 for female, 1 for male
		self.parent = parents
		self.isDiseased = False
		self.drug_strat = drug_strat
		#self.wealth = averageWealth(parents)
		self.spouses = {}
	
	def incrementAge(self):
		self.age += 1

	def dies(self):
		self.alive = False

	def changeWealth(self, wealth):
		self.wealth += wealth

	def setWealth(self, wealth):
		self.wealth = wealth

	def setIncome(self, income):
		self.income = income


	def getSpousesAndChildren(self):
		return self.spouses

	def getSpouses(self):
		return self.getSpousesAndChildren().keys()

	def getChildren(self):
		return [x for listy in self.getSpousesAndChildren().values() for x in listy]


	def addChild(self, otherParent, child=None):

		#self.incrementAge()

		if self.isDiseased:
			if bernoulli(parameters.pPassingByVaginalSex):
				otherParent.isDiseased = True

		gender = random.randint(0, 1)

		if child == None:
			num = random.random()
			isDiseased = False
			if self.gender == 0:
				isDiseased = bernoulli(parameters.pChildGettingFromMother)
			child = Individual(int(str(self.idx) + str(self.numChildren)), gender, [self, otherParent], isDiseased)

		if otherParent not in self.spouses:
			self.spouses[otherParent] = [child]
		else:
			self.spouses[otherParent].append(child)

		if child not in otherParent.getChildren():
			otherParent.addChild(self, child)
		self.numChildren += 1
		return child
		

	def toString(self):

		d = {}
		for x in self.spouses:

			d[x.id] =  str([child.id for child in self.spouses[x]])

		return ("my Id is " + str(self.idx), "my gender is " + str(self.gender)+ " " + str(d))

	def BFS(self):

		level = 0
		prev = 0
		saidSoFar = set()
		queue = []
		queue.append((self, level))
		saidSoFar.add(self)
		while queue: 
			s, level = queue.pop(0)
			if level != prev:
				print("\n" + str(s.id), end = " ")
			else:
				print(s.id, end = " ")
			for Individual in s.getChildren():
				if Individual not in saidSoFar:
					queue.append((Individual, level + 1))
					saidSoFar.add(Individual)
			prev = level
            
def isChildOrParentRelationship(i, j):  
	return i in j.getChildren() or j in i.getChildren()

def isSibling(i, j):
	parents = j.parent
	for parent in parents:
		if i in parent.getChildren():
			return True
	iparents = i.parent
	for parent in iparents:
		if j in parent.getChildren():
			return True
	return False

def isNuclear(i, j):
	return isSibling(i, j) or isChildOrParentRelationship(i, j)    

def findMate(Individual, population, genderMatters, strategy, incestIsBanned):


	# BREED LIKE RABBITS - FIRST Individual YOU MEET OF THE OPPOSITE GENDER
	if strategy == RANDOM_MATING:
		for i in population:
			if not genderMatters or Individual.gender != i.gender:
				# if i.age < MAX_AGE:
					if incestIsBanned:
						if isNuclear(i, Individual):
							continue
					return i
				# else:
				# 	i.dies()
	elif strategy == BASED_ON_WEALTH: # BREED BASED ON WEALTH, by probability.
		for i in population:
			if not genderMatters or Individual.gender != i.gender:
				# if i.age < MAX_AGE:
					if incestIsBanned and isNuclear(i, Individual):
						continue
					wealth_diff = abs(i.wealth - Individual.wealth)
					probability_of_mate = (10 - wealth_diff) / 10
					value = random.random()
					if value < probability_of_mate:
						return i
					else:
						continue
				# else:
				# 	i.dies()
	return None

def mate(Individual, pop, genderMatters, mating_strategy, incestIsBanned):
	mate = findMate(Individual, pop, genderMatters, mating_strategy, incestIsBanned)

	if mate == None:
		return None
	else:
		return Individual.addChild(mate)
MOVES = 9
def breedIndividuals(l, maxNumber, mating_strategy, genderMatters, selective_pressure, incestIsBanned=True):

	allAlive = set(l)
	while len(allAlive) != 0 and len(allAlive) < maxNumber:
		Individual = allAlive.pop()
		if selective_pressure == WEALTH:
			probability_of_mate =  (110 - Individual.wealth) / (110 - 100)
			value = random.random()
			if value / WEALTH_SELECTION_STRENGTH < probability_of_mate:
				Individual.dies()
			else:
				pass


		if not Individual.alive or Individual.age >= MAX_AGE: # you get to have three children max, THEN YOU DIE
			Individual.dies()
			continue
		child = mate(Individual, allAlive, genderMatters, mating_strategy, incestIsBanned)
		if child != None:
			allAlive.add(child)
		else:
			print("No suitable mates")
			break
		allAlive.add(Individual)
		# print("n =", len(allAlive))
		# print("wealth= ", getAverageWealth(allAlive))
	return allAlive


def getSexLife(Individual):
	for spouse in Individual.spouses:
		print("spouse:", spouse.id, "wealth", spouse.wealth)
		for child in Individual.spouses[spouse]:
			print("\t",child.id)


def getWealth(Individual):
	return Individual.wealth




allAlive = []

adam = Individual(1, 1)
eve = Individual(2, 0)


allAlive.append(eve)
allAlive.append(adam)

STARTING_SIZE = 5000
STOP_SIZE = 6000

def plotWealthHistogram(individuals, label):
	plt.hist([i.wealth for i in individuals], bins=[100 + i for i in range(20)], histtype='bar', alpha = 0.5, label=label)


# for i in range(3, STARTING_SIZE):
# 	allAlive.append(Individual(i, i % 2))


# plotWealthHistogram(allAlive, "Original Population")

# def getAverageWealth(l):
# 	return sum([i.wealth for i in l])/len(l)

# mating_strategy = RANDOM_MATING
# WEALTH = 0
# incest = breedIndividuals(allAlive, STOP_SIZE, mating_strategy, genderMatters = True, selective_pressure = WEALTH, incestIsBanned=True)
# noIncest = breedIndividuals(allAlive, STOP_SIZE, mating_strategy, genderMatters = False, selective_pressure = WEALTH, incestIsBanned=True)
# plotWealthHistogram(incest, "heterosexual repro only")
# plotWealthHistogram(noIncest, "men can have babies with men")
# plt.legend(loc= 'upper right')
# plt.show()

# multipe genders helps, no incest helps. 

