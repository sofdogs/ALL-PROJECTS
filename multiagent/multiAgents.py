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

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
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

    def evaluationFunction(self, currentGameState, action):
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
        ##depends on current and successor state 

        curPos = currentGameState.getPacmanPosition() 
        pacState = currentGameState.getPacmanState() 

        newFood = newFood.asList() 
        score =0

        #Keep moving until
        if action == Directions.STOP:
            score += -10 
        
        #how i play pacman--extra step 
        pacDir = pacState.configuration.direction 
        if pacDir == action and action != Directions.STOP: 
            score +=10 #small enough to keeo him moving in one direction but not too big to distract him

        #Move to closest food
        if currentGameState.hasFood(newPos[0], newPos[1]): 
            score += 20 
        else : 
            foodDistances = [util.manhattanDistance(newPos, food) for food in newFood] #so dont have to append!
            foodDistances.sort() #sorts in ascending order 
            nearestFood = foodDistances[0]

            score += float(20/nearestFood)

            if len(foodDistances) >= 2: 
                #nearestFood = foodDistances[-1]
                avgFoodDist = sum(foodDistances)/len(foodDistances) 
                score += float(12/avgFoodDist)
        
        #Move away from ghosts unless they are scared 
        newGhostDistances = [util.manhattanDistance(newPos, ghost.configuration.pos)for ghost in newGhostStates]
        #want smallest distance so...
        newNearestGhost = min(newGhostDistances)

        curGhostDistances = [util.manhattanDistance(curPos, ghost.configuration.pos)for ghost in newGhostStates]
        curNearestGhost = min(curGhostDistances)

        if curNearestGhost != newNearestGhost: 
            #if ghost is now closer...
            if newNearestGhost < curNearestGhost: 
                #if ghost is scared, chase it!
                closestGhostIndex = newGhostDistances.index(newNearestGhost) 
                if newScaredTimes[closestGhostIndex]> newNearestGhost:
                    score += 20 #motivation to chase ghosts 
                elif newNearestGhost == 0: #if none in array, they arent scared and want to aavoid 
                    score -= 200
                elif  newNearestGhost < 4: #getting close, move away 
                    score -= 20/newNearestGhost 

        #Move closer to an energy pellet
        #Not needed but playing around to get higher score
        if True and len(successorGameState.getCapsules()): 
            
            currentEnergyDistances = [util.manhattanDistance(curPos, pos) for pos in currentGameState.getCapsules()]
            nearestCurrentEnergy = min(currentEnergyDistances)

            newEnergyDistances = [util.manhattanDistance(newPos, pos) for pos in currentGameState.getCapsules()]
            nearestNewEnergy = min(newEnergyDistances)
            if nearestNewEnergy< nearestCurrentEnergy: 
                score += nearestNewEnergy

        return successorGameState.getScore() + score

         #reciprocal of distance to food 
         #converts large numbers into smaller and smaller into bigger
def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
            #!!! based on psudocode from lecture: https://youtu.be/1KTCoQRWKOE
    """
    Your minimax agent (question 2)
    """
    
    ## keep track of depth & don't go past self.depth
    # self = a multisearch agent, can tell by its index what it is 
    def getAction(self, gameState):
        # returns tuple: (bestState, bestValue)
        def maximizer(gameState, index, depth):
            maxVal = -9999999
            maxTuple = [None, maxVal]
            
            if(index != 0): print("ERROR: minimizer called on a ghost")
            # if we are at an ending state, evaluate the cost to this state, it is a leaf node. 
            # We can backtrack & build the parent cost based on this constant
            if(gameState.isLose() or gameState.isWin() or depth == self.depth): 
                leafNode = [None, self.evaluationFunction(gameState)]
                #print("LEAF: ")
                #print(leafNode)
                return leafNode
            
            #want to generate all successors & find highest, take it & return it to prev call (by a minimizer)
            actions = gameState.getLegalActions(index) 
            #generate all successors & choose min / max based on eval function & return it to prev call
            # loop through all indeces to find best positon for each agent
            for action in actions:
                #print("ACTION & INDEX: ")
               # print(action, index)
                successorState = gameState.generateSuccessor(index, action) #does not contain action, must add after
                #print("SUCCESSOR STATE IN maximizer funct: ")
                #print(successorState)
                # traverse tree & get returned values from the minimizers (ghosts)
                potentialMaxTuple = minimizer(successorState, index+1, depth) #TODO: is depth off by 1? should start at 0 or 1?
                #print("POTENTIAL MAX TUPLE: ")
                #print(potentialMaxTuple)
                if(potentialMaxTuple[1] > maxVal): 
                    maxTuple = [action, potentialMaxTuple[1]] #action, score
                    maxVal = potentialMaxTuple[1]
                
            #return the maximum value & action taken to get there returned from the minimizer successors
            return maxTuple
        
        # returns tuple: (bestState, bestValue)
        def minimizer(gameState, index, depth):
            min = 999999
            minTuple = [None, min]
            if(gameState.isLose() or gameState.isWin()): 
                leafNode = [None, self.evaluationFunction(gameState)]
                #print("LEAF: ")
               #print(leafNode)
                return leafNode
            
            actions = gameState.getLegalActions(index) 
            #try out all actions and check which one achieves the min score, then return that aciton, score back to parent
            for action in actions:
                min = minTuple[1]
                successorState = gameState.generateSuccessor(index, action)
                #print("HERE SUCCESSOR STATE")
                #print(successorState)
                
                numAgents = gameState.getNumAgents()
                lastGhostIndex = numAgents - 1 # last ghost should move on to pacman of next state, keep looping
                if(index == lastGhostIndex):
                    potentialMinTuple = [action, maximizer(successorState, 0, depth+1)[1]]
                    potentialMin = potentialMinTuple[1] #potential min integer
                else: #if there are more ghosts left, see if they can find a move that generates a lower score & use it if so
                    potentialMinTuple = [action, minimizer(successorState, index+1, depth)[1]] # keep depth the same, expanding the same node but with diff agent
                    potentialMin = potentialMinTuple[1]
                    # if we found a better path with a minimum score, update the current min action & score to match the new best
                if potentialMin < min: 
                    minTuple = potentialMinTuple
                   
            return minTuple
        
        #return the action generated by maximizing the score returnd by the first max node with the given gamestate
        return maximizer(gameState, 0, 0)[0] # [action, cost] return next best action (must save action in tuple every return from max / min)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

   
    # # Evaluate MAX (pacman) moves...
    # def max_value (self, gameState, alpha, beta):
    #     v = -999999
    #     agentIndex = 0 
    #     actions = gameState.getLegalActions(agentIndex)
    #     for action in actions:
    #         newState = gameState.generateSuccessor(agentIndex, action)


    def do_alphabeta (self, gameState, cur_depth, agentIndex, alpha, beta):
        
        # Handle game over and reached a terminal leaf...
        if gameState.isWin() or gameState.isLose() or cur_depth == self.depth:
              return self.evaluationFunction (gameState), None

        # print('Num agents=', gameState.getNumAgents())
        bestScore = -999999 if agentIndex == 0 else 999999
        bestAction = None

        # Expand all moves/actions...
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:

              # If this is the last agent, then next level increases our depth...
              newDepth = cur_depth + 1 if agentIndex == gameState.getNumAgents() - 1 else cur_depth

              # Generate the new state...                                  
              newState = gameState.generateSuccessor (agentIndex, action)

              # Recursively call alphabeta...
              curScore, curAction = self.do_alphabeta (newState, newDepth, 
                                                       (agentIndex + 1) % gameState.getNumAgents(),
                                                       alpha, beta)

              # Keep the best score and action...
              if agentIndex == 0:
                    if curScore > bestScore:
                          bestScore = curScore
                          bestAction = action
                    if bestScore > beta:
                          return bestScore, bestAction # prune any remaining branches
                    alpha = max(alpha, bestScore)
              else:
                    if curScore < bestScore:
                          bestScore = curScore
                          bestAction = action
                    if bestScore < alpha:
                          return bestScore, bestAction  # prune any remaining branches
                    beta = min(beta, bestScore)                    

        return bestScore, bestAction


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        score, action = self.do_alphabeta (gameState, 0, 0, -99999, 99999)
        return action         
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
      # !!! based on psudocode from lecture: https://youtu.be/jaFRyzp7yWw
        #returns [action, score] action = most optimal action from this state, score = best score we could achieve branching out from this node
        # max should be very similar to minimax
        # called on pacman only, index 0
    def getAction(self, gameState):
        def maximizer(gameState, index, depth):
            maxTuple = [None, 0]
            if(index != 0): 
                print("ERROR: maximizer called on a ghost")
                return 0
            #check if we are at a terminal state, if so, return the evaluation of this state
            if(gameState.isWin() or gameState.isLose() or depth == self.depth):
                leafNode = [None, self.evaluationFunction(gameState)]
                return leafNode #return a leafnode with its score & none as action, since there are no actions we can take from here
            #if not a leaf, need to go further in tree & evaluate average value of child choices
            actions = gameState.getLegalActions(index)
            for action in actions:
                successorState = gameState.generateSuccessor(index, action)
                #find avg of every subtree an action can generate & return the action that results in the largest score
                potentialMaxTuple = [action, averageOfChildren(successorState, index+1, depth)[1]] #expanding new child layer, add 1 to depth
                if potentialMaxTuple[1] > maxTuple[1]:
                    maxTuple = potentialMaxTuple
                    
            return maxTuple
                      
        def averageOfChildren(gameState, index, depth):
            childScoreTotal = 0
            childScoreAverage = 0
            lastGhostIndex = gameState.getNumAgents() - 1
            if(gameState.isWin() or gameState.isLose() or depth == self.depth):
                leafNode = [None, self.evaluationFunction(gameState)]
                return leafNode #return a leafnode with its score & none as action, since there are no actions we can take from here
            # sum up all possible children & average them out
            actions = gameState.getLegalActions(index)
            for action in actions:
                #generate the successor state if we took this action
                childState = gameState.generateSuccessor(index, action)
                if index == lastGhostIndex: # next agent is pacman, call maximizer funct
                    childScore = maximizer(childState, 0, depth+1)[1] # maximizer returns [action, score]
                else:
                    childScore = averageOfChildren(childState, index+1, depth)[1]
                  # for each action, add the score it could achieve to the total child score for this parent  
                childScoreTotal += childScore
            # after loop terminates, find average of all children by dividing by num children (the num of actions)
            childScoreAverage = childScoreTotal / len(actions)
            return [action, childScoreAverage]
        
        return maximizer(gameState, 0, 0)[0] #return best action  


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    food = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates() 
    pacPos = currentGameState.getPacmanPosition() 
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates] 
    food_score = 0 

    #Closer to food is good 
    if len(food) == 0: 
        food_score += 500 #if no food youve won the game
    else: 
        foodDistances = [util.manhattanDistance(pacPos, food) for food in food] #learning abt pythonic stytle 
        foodDistances.sort() 
        nearestFood = foodDistances [0]
        food_score += max(0, 20.0-0.5*nearestFood)

        if len(foodDistances) >= 2: 
            nextFood = max(0, 10.0 -0.5*foodDistances[-1])
            food_score += nextFood 

    #Further away from ghosts is good 
    ghost_score = 0 
    curGhostDistances = [util.manhattanDistance(pacPos, ghost.configuration.pos) for ghost in ghostStates] 
    nearestGhostDist = min(curGhostDistances) 
    closestGhostIndex = curGhostDistances.index(nearestGhostDist) 

    #If ghost is scared and within striking range go get him 
    if scaredTimes[closestGhostIndex]> 0: 
        if scaredTimes[closestGhostIndex] > nearestGhostDist: 
            ghost_score += 30*nearestGhostDist #chase ghost!
    else: 
        #avoid ghosts the clsoer they are
        if nearestGhostDist == 0.0: 
            ghost_score -= 9999
        else: 
            ghost_score -= 20.0/nearestGhostDist 
    
    #Move closer to an energy pellet 
    energy_score = 0 
    if True and len(currentGameState.getCapsules()): 
        currentEnergyDistances = [util.manhattanDistance(pacPos, pos) for pos in currentGameState.getCapsules()]
        nearestCurrentEnergy = min(currentEnergyDistances) 
        energy_score += max(0.0, 10.0 -0.5*nearestCurrentEnergy)  
    
    return currentGameState.getScore() + food_score + ghost_score + energy_score 



# Abbreviation
better = betterEvaluationFunction
