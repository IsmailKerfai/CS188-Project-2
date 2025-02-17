# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """ Well, we need 3 main key information here to deal with the fucntion state:
        -position of pacman before the action
        -position of the remaining food
        -postion and state of the ghosts

        so the manhattan distance is used for both calclated the distance between our Pacman and the food, 
        and between Pacman and the ghosts

        and the use of the distance between the food and pacman is to adjust the score, this encourages it to move forward to nearst food since
        the close the distance the larger the the score will get
        """
        newFood = successorGameState.getFood().asList()
        minFoodist = float("inf")
        for food in newFood:
            minFoodist = min(minFoodist, manhattanDistance(newPos, food))

        for ghost in successorGameState.getGhostPositions():
            if (manhattanDistance(newPos, ghost) < 2):
                return -float('inf')
            
        return successorGameState.getScore() + 1.0/minFoodist

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def Min(gameState, remainingDepth, agent):

            if (gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
                        
            minEval = 99999
            actions = gameState.getLegalActions(agent)
            
            for action in actions:
                result = gameState.generateSuccessor(agent, action)

                if (agent == gameState.getNumAgents() - 1): #last ghost, so do next pacMove
                    eval = Max(result, remainingDepth)
                else:
                    eval = Min(result, remainingDepth, agent + 1)  #any other Ghost

                if (eval < minEval): 
                    minEval = eval
                
            return minEval

        def Max(gameState, remainingDepth):
            if (remainingDepth == 0 or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            
            maxEval = -99999
            actions = gameState.getLegalActions(0)

            for action in actions:
                new_board = gameState.generateSuccessor(0, action)

                eval = Min(new_board, remainingDepth-1, 1)
                if (eval > maxEval): 
                    maxEval = eval
                
            return maxEval
        
        def MinMax(gameState, maxDepth):
            maxEval = -99999
            bestMove = None            
            remainingDepth = maxDepth-1            
            actions = gameState.getLegalActions(0)

            for action in actions:

                result = gameState.generateSuccessor(0, action)
                
                eval = Min(result, remainingDepth, 1)
                
                if (eval > maxEval):
                    maxEval = eval
                    bestMove = action

            return bestMove 

        return MinMax(gameState, self.depth)   

        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def MinAB(gameState, remainingDepth, agent, a, b):

            if (gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
                        
            minEval = 99999
            actions = gameState.getLegalActions(agent)
            
            for action in actions:
                result = gameState.generateSuccessor(agent, action)

                if (agent == gameState.getNumAgents() - 1): #last ghost, so do next pacMove
                    eval = MaxAB(result, remainingDepth, a, b)
                else:
                    eval = MinAB(result, remainingDepth, agent + 1, a ,b)  #any other Ghost

                if (eval < minEval): 
                    minEval = eval
                
                if(minEval < a): #prune
                    return eval 
                elif(minEval < b):
                    b = minEval

            return minEval

        def MaxAB(gameState, remainingDepth, a, b):
            if (remainingDepth == 0 or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            
            maxEval = -99999
            actions = gameState.getLegalActions(0)

            for action in actions:
                new_board = gameState.generateSuccessor(0, action)

                eval = MinAB(new_board, remainingDepth-1, 1, a, b)

                if (eval > maxEval): 
                    maxEval = eval

                if(maxEval > b): #prune
                    return eval 
                elif(maxEval > a):
                    a = maxEval
                
            return maxEval
        
        def MinMaxAB(gameState, maxDepth):
            maxEval = -99999
            a = -99999
            b = 99999
            bestMove = None            
            remainingDepth = maxDepth-1            
            actions = gameState.getLegalActions(0)

            for action in actions:

                result = gameState.generateSuccessor(0, action)
                eval = MinAB(result, remainingDepth, 1, a, b)
                
                if (eval > maxEval):
                    maxEval = eval
                    bestMove = action
                if (a < eval):
                    a = eval

            return bestMove 

        return MinMaxAB(gameState, self.depth)  

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def Min(gameState, remainingDepth, agent):

            if (gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
                        
            actions = gameState.getLegalActions(agent)
            i = 0
            evalSum = 0
            
            for action in actions:
                result = gameState.generateSuccessor(agent, action)

                if (agent == gameState.getNumAgents() - 1): #last ghost, so do next pacMove
                    eval = Max(result, remainingDepth)
                else:
                    eval = Min(result, remainingDepth, agent + 1)  #any other Ghost
                
                i += 1
                evalSum += eval
            
            avgEval = evalSum/i
            #print(avgEval)
            return avgEval

                
                
            return minEval

        def Max(gameState, remainingDepth):
            if (remainingDepth == 0 or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            
            maxEval = -99999
            actions = gameState.getLegalActions(0)

            for action in actions:
                new_board = gameState.generateSuccessor(0, action)

                eval = Min(new_board, remainingDepth-1, 1)
                if (eval > maxEval): 
                    maxEval = eval
                
            return maxEval
        
        def ExpectiMax(gameState, maxDepth):
            maxEval = -99999
            bestMove = None            
            remainingDepth = maxDepth-1            
            actions = gameState.getLegalActions(0)

            for action in actions:

                result = gameState.generateSuccessor(0, action)
                
                eval = Min(result, remainingDepth, 1)
                
                if (eval > maxEval):
                    maxEval = eval
                    bestMove = action

            return bestMove 

        return ExpectiMax(gameState, self.depth)

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
