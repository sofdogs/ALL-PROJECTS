# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""


import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
     #using a stack for depth because it is LIFO 

    #creating empty stack 
    depthList = util.Stack() 

    visitedNodes = []
    actions = [] #path/actions it will take/perform
    startPos = problem.getStartState()

    depthList.push((startPos, actions, 0))

    #alg starts
    while not depthList.isEmpty(): 
        curr_node = depthList.pop() 
        position = curr_node[0]
        actions = curr_node [1]

        #if curr position is the goal then, 
        if problem.isGoalState(position): 
            return actions

        #adding first position in array/checking if node is not in list
        if position not in visitedNodes:
            visitedNodes.append(position)
            successor_list = problem.getSuccessors(position)

            for child in successor_list: 
                if child[0] not in visitedNodes: 
                    childPos = child[0]
                    childActions = actions + [child[1]]
                    depthList.push((childPos, childActions, child[2]))

    return []

def breadthFirstSearch(problem: SearchProblem):
    if problem.isGoalState(problem.getStartState()): return []
    
    queue = util.Queue()
    head = problem.getStartState()
    queue.push(head)

    paths = util.Queue()
    parentPath = []
    visited = []
    
    curr = queue.pop()
    flag = problem.isGoalState(curr)

    while(not flag):
        if curr not in visited: 
            visited.append(curr) 
            children = problem.getSuccessors(curr)
            for child in children: 
                queue.push(child[0])
                childAction = child[1]
                childPath = parentPath + (list(childAction))
                paths.push(parentPath + [child[1]])

        parentPath = paths.pop()
        curr = queue.pop()
        flag = problem.isGoalState(curr)
    return parentPath
    
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
     ##followed pseudocode from https://medium.com/@dipalimajet/understanding-hintons-capsule-networks-c2b17cd358d7
    ##setting up alg
    visitedNodes = []
    action = []
    startPos = problem.getStartState()

    #print("Is the start a goal?", problem.getStartState())

    ##create the queue
    costSearch = util.PriorityQueue()
    costSearch.push((startPos, action), 0)

    while not costSearch.isEmpty(): 
        #fetching element from queue
        curNode, curActions = costSearch.pop() 

        #if current position of node is in the right spot, it will return set of actions
        if problem.isGoalState(curNode): 
            return curActions

        if curNode not in visitedNodes: 
            #if the current position has not been visited, 
            #it will add that position to the visited nodes array 
            visitedNodes.append(curNode)

            successors = problem.getSuccessors(curNode)

            for child in successors: 
                succ, actions, cost = child
                costSearch.push((succ, curActions + [actions]),
                #get next cost of actions  
            problem.getCostOfActions(curActions) + cost)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def gaStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    print("TYPE: ")
    print (type(problem))
    #if(isinstance(problem, CornersProblem)): return genaStarSearch(problem, heuristic)
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue() #store nodes based on g+h value (arc cost to get to it + heuristic on node)
    dict = {} #(0, 0) --> [g: int, parent: Tuple [x, y], String: action to get to this node] where g is the current best cost from the start to this node, not including heurisitc
    visited = []
    
    start = [problem.getStartState(), None, 0]
    print(start)
    dict[start[0]] = [0, None, None] #when we expand a node from the prio queue, look here to see if we can find a better g value, if so, update it & ~~re-add to queue??
    frontier.push(start[0], 0)
    
    while(not frontier.isEmpty()): #while list is not empty
        curr = frontier.pop() #pop node with shortest current f value (est cost from A to goal)
        
        if len(curr) == 3: curr = curr[0]
        if problem.isGoalState(curr):
            break
        if curr in visited: continue
        visited.append(curr)
        #explore its neighbors
        
        for successor in problem.getSuccessors(curr):
            if(successor[0] in visited): continue
            if problem.getStartState() == successor[0]: continue #would never want to go back to start state
            successorCost = dict[curr][0] + successor[2] #compute new g value if we were to set curr as this node's parent
            #if the successor does not have a computed shortest path from the start to it, or the shortest path is no longer
            #the shortest, update the successor's path
            if(successor[0] not in dict.keys()):
            #this is the current best path if we have no current path    
                dict[successor[0]] = [successorCost, curr, successor[1]] # if the node has no current best path, this is its current best path
                #update best distance from start to this node in dict
                newPrioValue = dict[successor[0]][0] + heuristic(successor[0], problem)   #update value in prio queue if this updated cost is better
                frontier.update(successor, newPrioValue) #this method will automatically update the node's f value with the higher one or push it in the queue for the first time
            else:
                if successorCost < dict[successor[0]][0]:
                    dict[successor[0]] = [successorCost, curr, successor[1]] 
                    #update best distance from start to this node in dict
                    newPrioValue = dict[successor[0]][0] + heuristic(successor[0], problem)   #update value in prio queue if this updated cost is better
                    frontier.update(successor[0], newPrioValue) #this method will automatically update the node's f value with the higher one or push it in the queue for the first time
    finalPath = []
        #append parent of this node until we reach the start state (a node is the start state if its parent = None)
    
    while curr != problem.getStartState():
        action = (dict[curr])[2]
        finalPath.insert(0, action)  #append the last action we took to get to this node & backtrack to its parent                 
        parent = (dict[curr])[1] #get coordinates (0, 1) of parent for backtracking
        curr = parent
        
    print(finalPath)
    return finalPath


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    frontier = util.PriorityQueue() #store nodes based on g+h value (arc cost to get to it + heuristic on node)
    dict = {} #(0, 0) --> [g: int, parent: Tuple [x, y], String: action to get to this node] where g is the current best cost from the start to this node, not including heurisitc
    visited = [] #list of visited coordinates
    
    start = [problem.getStartState(), None, 0] #make start into full state (we are only given coords)
    #extract state (state, action, cost)
    isCornerProblem = False
    
    #calculate coords: (if we are using the a CornersProblem object, our state is in a different format ( ((x,y), []), action, cost )
    #set bool, we know entire problem is corner problem if start state belongs to corner problem
    if isinstance(start[0][0], int) or isinstance(start[0][0], str): isCornerProblem = False
    elif not isinstance(start[0][1], list): return gaStarSearch(problem, heuristic)
    else: isCornerProblem = True
    print (isCornerProblem)
    #if isinstance(start[0][0], tuple): isCornerProblem = True
    #else: isCornerProblem = False
    
    print("START: ")
    print(start)
    #only use start[0] as a key if it is the coordinate pair
    if isCornerProblem: position = start[0][0]
    else: position = start[0]
        
    startPosition = position
    #(g, Parent, Action)
    dict[position] = [0, None, None] #when we expand a node from the prio queue, look here to see if we can find a better g value, if so, update it & ~~re-add to queue??
    frontier.push(start, 0) #frontier must contain full state, not just coords, dict only contains coords
    
    while(not frontier.isEmpty()): #while list is not empty
        curr = frontier.pop() #pop node with shortest current f value (est cost from A to goal)
        #need to keep entire state if it is using the cornersproblem states
        if isCornerProblem: position = curr[0][0]
        else: position = curr[0]
        #if this is the goal, break out of while loop & return path
        if problem.isGoalState(curr[0]):
            break
      
        if position in visited: continue #visited should contain only coordinates
        visited.append(position)
        #explore its neighbors
        #position = coordinate pair
        #state must be complete when we enter it into getSuccessors
        
        for successor in problem.getSuccessors(curr[0]):
            if isCornerProblem: successorPosition = successor[0][0]
            else: successorPosition = successor[0]
            
            if(successorPosition in visited): continue
            if startPosition == successorPosition: continue #would never want to go back to start state
            
            successorCost = (dict[position])[0] + successor[2] #compute new g value if we were to set curr as this node's parent
            #if the successor does not have a computed shortest path from the start to it, or the shortest path is no longer
            #the shortest, update the successor's path
            if(successorPosition not in dict.keys()):
            #this is the current best path if we have no current path    
                dict[successorPosition] = [successorCost, position, successor[1]] # if the node has no current best path, this is its current best path
                #update best distance from start to this node in dict
                newPrioValue = dict[successorPosition][0] + heuristic(successor[0], problem)   #update value in prio queue if this updated cost is better
                frontier.update(successor, newPrioValue) #this method will automatically update the node's f value with the higher one or push it in the queue for the first time
            else:
                #if the new cost is less than the old cost, replace that entry in the dictionary
                if successorCost < dict[successorPosition][0]: #TODO: may need to change to dict[positions]
                    dict[successorPosition] = [successorCost, position, successor[1]] #g, parent position, action
                    #update best distance from start to this node in dict
                    newPrioValue = dict[successorPosition][0] + heuristic(successor[0], problem)   #update value in prio queue if this updated cost is better
                    frontier.update(successor, newPrioValue) #this method will automatically update the node's f value with the higher one or push it in the queue for the first time
    finalPath = []
        #append parent of this node until we reach the start state (a node is the start state if its parent = None)
    if isCornerProblem: curr = curr[0][0]
    else: curr = curr[0]
    while dict[curr][1] != None:
    #while curr != problem.getStartState():
        action = (dict[curr])[2]
        finalPath.insert(0, action)  #append the last action we took to get to this node & backtrack to its parent                 
        parent = (dict[curr])[1] #get coordinates (0, 1) of parent for backtracking (at position 1)
        curr = parent
        
    print(finalPath)
    return finalPath
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
