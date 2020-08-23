
import math
import random
import time
import Graph
import inequality
import numpy as np
import matplotlib.pyplot as plt
from RandomRobot import RandomRobot
from NeuralRobot import NeuralRobot
from PlayerRobot import PlayerRobot

NUMBER_OF_SQUARES = 9
MAX_AGE = 10

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


def isWinningMove(l, player, move):
	row, col = move

	intersectingColumn = [l[i][col] for i in range(3)]
	

	rowColWin =  isRowSame(l[row], player) or isRowSame(intersectingColumn, player)
	if rowColWin:
		return True
	elif (row * 3 + col) % 2 == 1:
		return False
	else: # we need to check diagonals
		diag1Win =  l[0][0] == l[2][2] == l[1][1] == player 
		diag2Win = l[1][1] == l[2][0] == l[0][2] == player
		return diag1Win or diag2Win


def isRowSame(l, player):
	prev = None
	for k in l:
		if k != player:
			return False
	return True

def isValid(arr, row, col):

	if arr[row][col] == 0:
		return True
	return False

def ensureValidMove(bot, arr):
	valid = False
	while not valid:
		row, col = bot.getMove(arr)
		if arr[row][col] == 0:
			valid = True
	return row, col

def displayBoard(arr):
	for row in arr:
		print(row)
def playGame(bot0, bot1):

	arr = [[0 for x in range(3)] for y in range(3)] 
	moves = 0
	#displayBoard(arr)
	while  moves < (len(arr) * len(arr[0])):
		if moves % 2 == 0:
			# X
			valid = False
			row, col = bot0.getMove(arr)
			if not isValid(arr, row, col):
				return 1, moves
			arr[row][col] = 1
			if moves >= 4:
				if isWinningMove(arr, 0, (row, col)):
					#displayBoard(arr)
					return 0, moves
		else:
			# O
			row, col = bot1.getMove(arr)
			if not isValid(arr, row, col):
				return 0, moves
			arr[row][col] = -1
			if moves >= 5:
				if isWinningMove(arr, 1, (row, col)):
					#displayBoard(arr)
					return 1, moves
		moves += 1
		#displayBoard(arr)
	return None






def recursiveMean(old, newPoint, n):
	return (old * (n - 1) + newPoint) / (n)

def totalGames(bot):
	return bot.ties + bot.wins + bot.losses

def scoreHowFitAnIndividualIs(ind, testSize):
	score = 0
	#print(ind)
	for i in range(testSize):
		num = random.randint(1, 8)
		bag = [i for i in range(9)]
		arr = random.sample(bag, num)

		board = [0 for i in range(9)]
		for place in arr:
			board[place] = random.choice([1, -1])
		if ind.strategy.predict(board) not in set(arr):
			score += 1
	return score


def everyoneFindsAMatch(l):
	for i, rob in enumerate(l):

			randomOpponentIndex = random.randint(0, len(l) - 1)
			winner = playGame(rob, l[randomOpponentIndex])
			numMoves = winner[1]
			allMoveTotals.append(numMoves)
			if winner == None:
				l[i].ties += 1
				l[randomOpponentIndex].ties += 1
			elif winner[0] == 0:
				l[i].wins += 1
				l[randomOpponentIndex].losses += 1
			elif winner[0] == 1:
				l[i].losses += 1
				l[randomOpponentIndex].wins += 1
			l[i].aveMoves = recursiveMean(l[i].aveMoves, numMoves, totalGames(l[i]))
			l[randomOpponentIndex].aveMoves = recursiveMean(l[randomOpponentIndex].aveMoves, numMoves, totalGames(l[randomOpponentIndex]))
def findMate(Ind, population, genderMatters, strategy, incestIsBanned):


	# BREED LIKE RABBITS - FIRST Individual YOU MEET OF THE OPPOSITE GENDER
	if strategy == RANDOM_MATING:
		for i in population:
			if not genderMatters or Ind.gender != i.gender:
				if i.age < MAX_AGE:
					if incestIsBanned:
						if isNuclear(i, Ind):
							continue

					return i
				else:
					i.dies()
	elif strategy == BASED_ON_WEALTH: # BREED BASED ON WEALTH, by probability.
		for i in population:
			if not genderMatters or Ind.gender != i.gender:
				if i.age < MAX_AGE:
					if incestIsBanned and isNuclear(i, Ind):
						continue
					wealth_diff = abs(i.wealth - Ind.wealth)
					probability_of_mate = (10 - wealth_diff) / 10
					value = random.random()
					if value < probability_of_mate:
						return i
					else:
						continue
				else:
					i.dies()
	return None

def mate(Ind, pop, genderMatters, mating_strategy, incestIsBanned):
	mate = findMate(Ind, pop, genderMatters, mating_strategy, incestIsBanned)

	if mate == None:
		return None
	else:
		return Ind.addChild(mate)
MOVESANDWINNING = 23
def breedIndividuals(l, mating_strategy, genderMatters, selective_pressure, incestIsBanned=True):

	allAlive = set(l)

	generations = 0
	start = time.time()

	

	while len(allAlive) != 0 and generations  < 50000:
		if generations % 1000 == 500:
			print(generations, len(allAlive))
		Ind = allAlive.pop()
		if selective_pressure == MOVESANDWINNING:
			testSize = 3
			probability_of_living = ((testSize) / (testSize - 1)) * ((scoreHowFitAnIndividualIs(Ind, testSize)) / (testSize))
			probability_of_death =  (1 - probability_of_living)
			value = random.random()
			if value  < probability_of_death:
				Ind.dies()
			else:
				pass

		if not Ind.alive or Ind.age >= MAX_AGE: # you get to have three children max, THEN YOU DIE
			Ind.dies()
			continue
		child = mate(Ind, allAlive, genderMatters, mating_strategy, incestIsBanned)
		if child != None:
			allAlive.add(child)

		else:
			print("No suitable mates")
			break
		allAlive.add(Ind)
		generations += 1
	return allAlive


l = []
for i in range(400):
	l.append(NeuralRobot())

adam = NeuralRobot()
eve = NeuralRobot()
#son = NeuralRobot(parents=[adam,eve])


rounds = 0
allMoveTotals = []

while rounds < 100:
	print(rounds / 100)
	everyoneFindsAMatch(l)
	rounds += 1


bestRatio = 0
worstRatio = 99
bestRobot = None
worstRobot = None
for i in l:
	if i.ties != 0:
		print(i.wins, i.losses, i.ties)
	ratio = i.wins/i.losses
	if ratio > bestRatio:
		bestRatio = ratio
		bestRobot = i
	elif ratio < worstRatio:
		worstRatio = ratio
		worstRobot = i

a = sum(allMoveTotals)/len(allMoveTotals)

plt.hist(allMoveTotals, alpha = 0.5, label="pre")



RANDOM_MATING = 4

results = list(breedIndividuals(l,RANDOM_MATING, genderMatters = False, selective_pressure = MOVESANDWINNING, incestIsBanned=True))



rounds = 0
allMoveTotals = []
while rounds < 100:
	print(rounds / 100)
	everyoneFindsAMatch(results)
	rounds += 1
bestRatio = 0
worstRatio = 99
bestRobot = None
worstRobot = None
for i in results:
	if i.ties != 0:
		print(i.wins, i.losses, i.ties)
	ratio = i.wins/i.losses
	if ratio > bestRatio:
		bestRatio = ratio
		bestRobot = i
	elif ratio < worstRatio:
		worstRatio = ratio
		worstRobot = i
print(a)

print(sum(allMoveTotals)/len(allMoveTotals))

plt.hist(allMoveTotals, alpha = 0.5, label = "post")
plt.legend(loc ='upper right')
plt.show()









	