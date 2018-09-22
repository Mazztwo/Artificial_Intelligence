#################################################################
#
# Alessio Mazzone
# ALM388@pitt.edu
#
# CS 1571 Aritificial Intelligence
#
# Project 1 
#
#################################################################


import sys
from collections import deque
from Queue import PriorityQueue
from ast import literal_eval as make_tuple
import numpy as np
from scipy.spatial import distance

# Node class used for BFS, DFS, and Unicost.
class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other): 
        return self.path_cost < other.path_cost

    def __le__(self, other): 
        return self.path_cost <= other.path_cost

    def __eq__(self, other):
        return self.path_cost == other.path_cost

    def __ne__(self, other): 
        return self.path_cost != other.path_cost

    def __gt__(self, other): 
        return self.path_cost > other.path_cost

    def __ge__(self, other):
        return self.path_cost >= other.path_cost

def bfs(config_filename):

    # Read in config file and extract appropirate info
    configuration, puzzle, initial_state, goal_state = readConfigFile(config_filename)

    # Time --> Total number of nodes created
    time = 0

    # node <- a node with STATE = problem.initial-state, pathcost = 0
    root = Node(initial_state,None,None,0)
    time += 1

    # if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    isGoalState = goalTest(puzzle, configuration, root.state, goal_state)
    if ( isGoalState ):
        printSolution(root, time, 0, 0)
        return
 
    # biggest size that frontier list grows to
    space_frontier = 0

    # Frontier needs to be a FIFO queue.
    # New nodes go to back of queue.
    # Old nodes get expanded first from the front of the queue.
    # EX: frontier --> []
    #     frontier.append(X)
    #     frontier.append(Y)
    #     frontier.append(Z)
    #     frontier --> [X,Y,Z]
    #     frontier.popleft = X
    #     frontier --> [Y,Z]
    #     frontier.append(A) 
    #     frontier --> [Y,Z,A]
    # frontier <- a FIFO queue that stores nodes
    frontier = deque([])
    frontier.append(root)
    space_frontier += 1

    # explored stores states
    explored = {}

    # In the explored dictionary, we store [key:value] pairs. I don't really care what
    # they key is, I just need a value. So, i'll just keep a counter variable and use that
    # as the key whenever I add a new state to my explored list. Of course, I'll check and make
    # sure that the state I want to add is not already in explored. 
    counter = 0

    #X loop do
    #X   if EMPTY?(frontier) then return failure
    #X   curr_node <-- POP(frontier) /*chooses the shallowest node in frontier */ 
    #X   add curr_node.STATE to explored
    #X   for each action in problem.ACTIONS(curr_node.STATE) do
    #X       child <-- CHILD-NODE(problem,curr_node,action)
    #       if child.STATE is not in explored or frontier then
    #           if problem.GOAL-TEST(child.STATE) then return SOLUTION(child) 
    #           frontier <-- INSERT(child,frontier)
    keep_going = True
    while ( keep_going ):
        if ( len(frontier) == 0 ): 
            printSolution(Node(None,None,None,-1),0,0,0)
            return

        # Get the shallowest node from frontier
        curr_node = frontier.popleft()

        # Add current node's state to explored
        explored[counter] = curr_node.state
        counter += 1

        actions = getActions(puzzle, configuration, curr_node)

        for action in actions:
            # child <-- CHILD-NODE(problem,curr_node,action)
            child = getChildNode(puzzle, configuration, curr_node, action, 0)
            time += 1

            # if child.STATE is not in explored or frontier then
            #   if problem.GOAL-TEST(child.STATE) then return SOLUTION(child) 
            #   frontier <-- INSERT(child,frontier)
            child_state = child.state

            # Check if node is in frontier
            child_in_frontier = isNodeInFrontier(child, frontier, 0)

            # Check that state is not in explored or frontier
            if ( child_state not in explored.values() and child_in_frontier is not True ):
                # Goal Test
                isGoalState = goalTest(puzzle, configuration, child_state , goal_state)
                if ( isGoalState ): 
                    printSolution(child, time, space_frontier,len(explored))
                    return
                
                # Add child to frontier
                frontier.append(child)
            
                # update space_frontier
                frontier_len = len(frontier)
                if ( frontier_len > space_frontier ):
                    space_frontier = frontier_len

def dfs(config_filename):

    # Read in config file and extract appropirate info
    configuration, puzzle, initial_state, goal_state = readConfigFile(config_filename)

    # Time --> Total number of nodes created
    time = 0

    # node <- a node with STATE = problem.initial-state, pathcost = 0
    root = Node(initial_state,None,None,0)
    time += 1

    # if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    isGoalState = goalTest(puzzle, configuration, root.state, goal_state)
    if ( isGoalState ):
        printSolution(root, time, 0, -1)
        return
 
    # biggest size that frontier list grows to
    space_frontier = 0

    # Frontier needs to be a LIFO stack.
    # New nodes go to next open index in array.
    #   frontier.append(x) --> [x]
    #   frontier.append(y) --> [x, y]
    #   frontier.append(z) --> [x, y, z]
    #   frontier.pop()     --> [x, y]
    # Newest node get expanded first from the front(top, rightmost) of the stack
    # frontier <- a LIFO stack that stores nodes
    frontier = []
    frontier.append(root)
    space_frontier += 1

    #X loop do
    #X   if EMPTY?(frontier) then return failure
    #X   curr_node <-- POP(frontier) /*chooses the deepest node in frontier */ 
    #X   add curr_node.STATE to explored
    #X   for each action in problem.ACTIONS(curr_node.STATE) do
    #X       child <-- CHILD-NODE(problem,curr_node,action)
    #X       if child.STATE is not in frontier then
    #X           if problem.GOAL-TEST(child.STATE) then return SOLUTION(child) 
    #X           frontier <-- INSERT(child,frontier)
    keep_going = True
    while ( keep_going ):
        if ( len(frontier) == 0 ): 
            printSolution(Node(None,None,None,-1),0,0,0)
            return

        # Get the deepest node from frontier
        curr_node = frontier.pop()

        actions = getActions(puzzle, configuration, curr_node)

        for action in actions:
            # child <-- CHILD-NODE(problem,curr_node,action)
            child = getChildNode(puzzle, configuration, curr_node, action, 0)
            time += 1

            # Check that state is not in current path back to root
            child_in_path = isNodeInPathToRoot(child)
        
            if ( child_in_path is not True):
                # Goal Test
                is_goal_state = goalTest(puzzle, configuration, child.state , goal_state)
                if ( is_goal_state ): 
                    printSolution(child, time, space_frontier,-1)
                    return
                
                # Add child to frontier
                frontier.append(child)
            
                # update space_frontier
                frontier_len = len(frontier)
                if ( frontier_len > space_frontier ):
                    space_frontier = frontier_len

def unicost(config_filename):
    
    #   q = PriorityQueue()
    #   q.put(5)
    #   q.put(10)
    #   q.put(1)
    #   q.put(5)
    #   print(q.queue) #[1,5,5,10]
    #   q.get()
    #   print(q.queue) #[5,5,10]
    #   if(10 in q.queue):
    #       print("raer") raer

 
    # Read in config file and extract appropirate info
    configuration, puzzle, initial_state, goal_state = readConfigFile(config_filename)

    # Time --> Total number of nodes created
    time = 0

    # root <-- a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    root = Node(initial_state,None,None,0)
    time += 1

    # if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    isGoalState = goalTest(puzzle, configuration, root.state, goal_state)
    if ( isGoalState ):
        printSolution(root, time, 0, 0)
        return
 
    # biggest size that frontier list grows to
    space_frontier = 0

    # Frontier needs to be a priority queue.
    # Nodes added based on path cost. Less expensive nodes are left in the array, more expensive are right.
    # [less expensive <----------> more expensive]
    # EX: [1,5,10,20]
    # Nodes get removed from the front(left) of the queue.
    # frontier <-- a priority queue ordered by PATH-COST, with root as the only element for now 
    frontier = PriorityQueue()
    frontier.put(root)
    space_frontier += 1

    # explored stores states
    explored = {}

    # In the explored dictionary, we store [key:value] pairs. I don't really care what
    # they key is, I just need a value. So, i'll just keep a counter variable and use that
    # as the key whenever I add a new state to my explored list. Of course, I'll check and make
    # sure that the state I want to add is not already in explored. 
    counter = 0

    #X   loop do
    #X       if EMPTY?(frontier) then return failure
    #X       node <-- POP(frontier) /*chooses the lowest-cost node in frontier */ 
    #X       if problem.GOAL-TEST(node.STATE) then return SOLUTION(node) 
    #X       add node.STATE to explored
    #X       for each action in problem.ACTIONS(node.STATE) do
    #X           child <-- CHILD-NODE(problem,node,action)
    #X           if child.STATE is not in explored or frontier then
    #X               frontier <-- INSERT(child,frontier)
    #X           else if child.STATE is in frontier with higher PATH-COST then
    #X              replace that frontier node with child
    keep_going = True
    while ( keep_going ):
        if ( len(frontier.queue) == 0 ): 
            printSolution(Node(None,None,None,-1),0,0,0)
            return

        # Get the lowest cost node from frontier
        curr_node = frontier.get()

        # Goal Test
        isGoalState = goalTest(puzzle, configuration, curr_node.state , goal_state)
        if ( isGoalState ): 
            printSolution(curr_node, time, space_frontier,len(explored))
            return

        # Add current node's state to explored
        explored[counter] = curr_node.state
        counter += 1

        actions = getActions(puzzle, configuration, curr_node)

        for action in actions:
            # child <-- CHILD-NODE(problem,curr_node,action)
            child = getChildNode(puzzle, configuration, curr_node, action, 0)
            time += 1

            # if child.STATE is not in explored or frontier then
            #   if problem.GOAL-TEST(child.STATE) then return SOLUTION(child) 
            #   frontier <-- INSERT(child,frontier)
            child_state = child.state

            # Check if node is in frontier
            child_in_frontier, parent_cost, frontier_index  = isNodeInFrontier(child, frontier, 1)

            # Check that state is not in explored or frontier
            if ( child_state not in explored.values() and child_in_frontier is not True ):
                # Add child to frontier
                frontier.put(child)
            
                # update space_frontier
                frontier_len = len(frontier.queue)
                if ( frontier_len > space_frontier ):
                    space_frontier = frontier_len

            # else if child.STATE is in frontier with higher PATH-COST then
            # replace that frontier node with child
            elif ( child_in_frontier and parent_cost > child.path_cost):
                # Replace node in frontier with higher path cost with child
                tmp = frontier.queue
                tmp.pop(frontier_index)
                frontier.put(child)

                # update space_frontier
                frontier_len = len(frontier.queue)
                if ( frontier_len > space_frontier ):
                    space_frontier = frontier_len

def greedy(config_filename, heuristic):
    
    # Same exact implementation of unicost, except instead of using
    # g(n) --> cost function to order the PriorityQueue,
    # we use h(n) --> heuristic function to order the PriorityQueue.

        
    #   q = PriorityQueue()
    #   q.put(5)
    #   q.put(10)
    #   q.put(1)
    #   q.put(5)
    #   print(q.queue) #[1,5,5,10]
    #   q.get()
    #   print(q.queue) #[5,5,10]
    #   if(10 in q.queue):
    #       print("raer") raer

 
    # Read in config file and extract appropirate info
    configuration, puzzle, initial_state, goal_state = readConfigFile(config_filename)

    # Time --> Total number of nodes created
    time = 0

    # root <-- a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    root = Node(initial_state,None,None,0)
    time += 1

    # if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    isGoalState = goalTest(puzzle, configuration, root.state, goal_state)
    if ( isGoalState ):
        printSolution(root, time, 0, 0)
        return
 
    # biggest size that frontier list grows to
    space_frontier = 0

    # Frontier needs to be a priority queue.
    # Nodes added based on path cost. Less expensive nodes are left in the array, more expensive are right.
    # [less expensive <----------> more expensive]
    # EX: [1,5,10,20]
    # Nodes get removed from the front(left) of the queue.
    # frontier <-- a priority queue ordered by PATH-COST, with root as the only element for now 
    frontier = PriorityQueue()
    frontier.put(root)
    space_frontier += 1

    # explored stores states
    explored = {}

    # In the explored dictionary, we store [key:value] pairs. I don't really care what
    # they key is, I just need a value. So, i'll just keep a counter variable and use that
    # as the key whenever I add a new state to my explored list. Of course, I'll check and make
    # sure that the state I want to add is not already in explored. 
    counter = 0

    #X   loop do
    #X       if EMPTY?(frontier) then return failure
    #X       node <-- POP(frontier) /*chooses the lowest-cost node in frontier */ 
    #X       if problem.GOAL-TEST(node.STATE) then return SOLUTION(node) 
    #X       add node.STATE to explored
    #X       for each action in problem.ACTIONS(node.STATE) do
    #X           child <-- CHILD-NODE(problem,node,action)
    #X           if child.STATE is not in explored or frontier then
    #X               frontier <-- INSERT(child,frontier)
    #X           else if child.STATE is in frontier with higher PATH-COST then
    #X              replace that frontier node with child
    keep_going = True
    while ( keep_going ):
        if ( len(frontier.queue) == 0 ): 
            printSolution(Node(None,None,None,-1),0,0,0)
            return

        # Get the lowest cost node from frontier
        curr_node = frontier.get()

        # Goal Test
        isGoalState = goalTest(puzzle, configuration, curr_node.state , goal_state)
        if ( isGoalState ): 
            printSolution(curr_node, time, space_frontier,len(explored))
            return

        # Add current node's state to explored
        explored[counter] = curr_node.state
        counter += 1

        actions = getActions(puzzle, configuration, curr_node)

        for action in actions:
            # child <-- CHILD-NODE(problem,curr_node,action)
            child = getChildNode(puzzle, configuration, curr_node, action, heuristic)
            time += 1

            # if child.STATE is not in explored or frontier then
            #   if problem.GOAL-TEST(child.STATE) then return SOLUTION(child) 
            #   frontier <-- INSERT(child,frontier)
            child_state = child.state

            # Check if node is in frontier
            child_in_frontier, parent_cost, frontier_index  = isNodeInFrontier(child, frontier, 1)

            # Check that state is not in explored or frontier
            if ( child_state not in explored.values() and child_in_frontier is not True ):
                # Add child to frontier
                frontier.put(child)
            
                # update space_frontier
                frontier_len = len(frontier.queue)
                if ( frontier_len > space_frontier ):
                    space_frontier = frontier_len

            # else if child.STATE is in frontier with higher PATH-COST then
            # replace that frontier node with child
            elif ( child_in_frontier and parent_cost > child.path_cost):
                # Replace node in frontier with higher path cost with child
                tmp = frontier.queue
                tmp.pop(frontier_index)
                frontier.put(child)

                # update space_frontier
                frontier_len = len(frontier.queue)
                if ( frontier_len > space_frontier ):
                    space_frontier = frontier_len

# Given a state, this function will return all possible actions for the 2 jug puzzle
def twoJugsGetActions(state_str, jugs_str):

    # state = (x, y)
    # jugs = (x, y)
    # encoding: XYZ
    #   X = action
    #       empty = 0
    #       fill = 1
    #   Y = which jug
    #       jug1 = 1
    #       jug2 = 2
    #   Z = destination
    #       ground = 0
    #       jug1 = 1
    #       jug2 = 2
    # EX: 012 --> empty jug1 into jug2
    # EX: 110 --> fill jug1 from tap


    # Turn jugs string and state into numerical tuples
    jugs = stringToTuple(jugs_str, 2, 0)
    state = stringToTuple(state_str, 2, 0)

    # Create empty actions array
    actions = []

    # Extract relevant info
    jug1 = state[0]
    jug2 = state[1] 
    capacity1 = jugs[0]
    capacity2 = jugs[1]

    # Check if jug1 is empty
    if ( jug1 == 0 ):
        # Fill jug1 from tap
        actions.append("110")
    # Check if jug1 is not at capacity but not empty
    if ( jug1 > 0 and jug1 < capacity1 ):
        # Fill jug1 from tap
        actions.append("110")
        # Empty jug1 to ground
        actions.append("010")
        # Empty jug1 into jug2 if jug2 is empty or not at capacity
        if ( jug2 < capacity2 ):
            # Empty jug1 into jug2
            actions.append("012")
    # Check if jug1 is at capacity
    if ( jug1 == capacity1 ):
        # Empty jug1 to ground
        actions.append("010")
        # Empty jug1 into jug2 if jug2 is empty or not at capacity
        if ( jug2 < capacity2 ):
            # Empty jug1 into jug2
            actions.append("012")
    # Check if jug2 is empty
    if ( jug2 == 0 ):
        # Fill jug2 from tap
        actions.append("120")
    # Check if jug2 is not at capacity but not empty
    if ( jug2 > 0 and jug2 < capacity2 ):
        # Fill jug2 from tap
        actions.append("120")
        # Empty jug2 to ground
        actions.append("020")
        # Empty jug2 into jug1 if jug1 is empty or not at capacity
        if ( jug1 < capacity1 ):
            # Empty jug2 into jug1
            actions.append("021")
    # Check if jug2 is at capacity
    if ( jug2 == capacity2 ):
        # Empty jug2 to ground
        actions.append("020")
        # Empty jug2 into jug1 if jug1 is empty or not at capacity
        if ( jug1 < capacity1 ):
            # Empty jug2 into jug1
            actions.append("021")

    return actions

# Given a state, this function will return all possible actions for the 3 jug
def threeJugsGetActions(state_str, jugs_str):

    # jugs = (jug1, jug2, jug3) 
    # Possible actions:
    #   1) fill jug1   4) empty jug1  7) pour jug1 into jug2    10) pour jug2 into jug3
    #   2) fill jug2   5) empty jug2  8) pour jug1 into jug3    11) pour jug3 into jug1
    #   3) fill jug3   6) empty jug3  9) pour jug2 into jug1    12) pour jug3 into jug2

    # Turn jugs string and state into numerical tuples
    jugs = stringToTuple(jugs_str, 3, 0)
    state = stringToTuple(state_str, 3, 0)

    # Create empty actions array
    actions = []

    # Extract relevant info
    jug1 = state[0]
    jug2 = state[1] 
    jug3 = state[2]
    capacity1 = jugs[0]
    capacity2 = jugs[1]
    capacity3 = jugs[2]

    # Check if jug1 is empty
    if ( jug1 == 0 ):
        # Fill jug1 from tap
        actions.append(1)
    # Check if jug1 is not at capacity but not empty
    if ( jug1 > 0 and jug1 < capacity1 ):
        # Fill jug1 from tap
        actions.append(1)
        # Empty jug1 to ground
        actions.append(4)
        # Empty jug1 into jug2 if jug2 is empty or not at capacity
        if ( jug2 < capacity2 ):
            # Empty jug1 into jug2
            actions.append(7)
        # Empty jug1 into jug3 if jug3 is empty or not at capacity
        if ( jug3 < capacity3 ):
            # Empty jug1 into jug3
            actions.append(8)       
    # Check if jug1 is at capacity
    if ( jug1 == capacity1 ):
        # Empty jug1 to ground
        actions.append(4)
        # Empty jug1 into jug2 if jug2 is empty or not at capacity
        if ( jug2 < capacity2 ):
            # Empty jug1 into jug2
            actions.append(7)
        # Empty jug1 into jug3 if jug3 is empty or not at capacity
        if ( jug3 < capacity3 ):
            # Empty jug1 into jug3
            actions.append(8)    
    # Check if jug2 is empty
    if ( jug2 == 0 ):
        # Fill jug2 from tap
        actions.append(2)
    # Check if jug2 is not at capacity but not empty
    if ( jug2 > 0 and jug2 < capacity2 ):
        # Fill jug2 from tap
        actions.append(2)
        # Empty jug2 to ground
        actions.append(5)
        # Empty jug2 into jug1 if jug1 is empty or not at capacity
        if ( jug1 < capacity1 ):
            # Empty jug2 into jug1
            actions.append(9)
        # Empty jug2 into jug3 if jug3 is empty or not at capacity
        if ( jug3 < capacity3 ):
            # Empty jug2 into jug1
            actions.append(10)
    # Check if jug2 is at capacity
    if ( jug2 == capacity2 ):
        # Empty jug2 to ground
        actions.append(5)
        # Empty jug2 into jug1 if jug1 is empty or not at capacity
        if ( jug1 < capacity1 ):
            # Empty jug2 into jug1
            actions.append(9)
        # Empty jug2 into jug3 if jug3 is empty or not at capacity
        if ( jug3 < capacity3 ):
            # Empty jug2 into jug1
            actions.append(10)
    # Check if jug3 is empty
    if ( jug3 == 0 ):
        # Fill jug1 from tap
        actions.append(3)
    # Check if jug3 is not at capacity but not empty
    if ( jug3 > 0 and jug3 < capacity3 ):
        # Fill jug3 from tap
        actions.append(3)
        # Empty jug3 to ground
        actions.append(6)
        # Empty jug3 into jug1 if jug1 is empty or not at capacity
        if ( jug1 < capacity1 ):
            # Empty jug1 into jug2
            actions.append(11)
        # Empty jug3 into jug2 if jug2 is empty or not at capacity
        if ( jug2 < capacity2 ):
            # Empty jug1 into jug3
            actions.append(12)       
    # Check if jug3 is at capacity
    if ( jug3 == capacity3 ):
        # Empty jug3 to ground
        actions.append(6)
        # Empty jug3 into jug1 if jug1 is empty or not at capacity
        if ( jug1 < capacity1 ):
            # Empty jug3 into jug1
            actions.append(11)
        # Empty jug3 into jug2 if jug2 is empty or not at capacity
        if ( jug2 < capacity2 ):
            # Empty jug3 into jug2
            actions.append(12)    

    return actions

# Given a node, check all paths in configuration and return all possible paths to and from city.
def citiesGetActions(configuration, curr_node):
    
    city = curr_node.state
    actions = []

    # Check each tuple (city1-->city2 = cost). If curr_node.state appears, 
    # add the tuple to actions.
    for path in configuration[4:]:
        if ( city in path ):
            actions.append(path)
            
    return actions

def twoJugsGetChildNode(curr_node, jugs_str, action, heuristic):
    
    # Get node state
    state_str = curr_node.state

    # Turn jugs string and state into numerical tuples
    jugs = stringToTuple(jugs_str, 2, 0)
    state = stringToTuple(state_str, 2, 0)

    jug1 = state[0]
    jug2 = state[1] 
    capacity1 = jugs[0]
    capacity2 = jugs[1]

    if ( action[0] == '0' ): # empty the jug
        if ( action[1] == '1' ): # empty jug1
            if ( action[2] == '0' ): # empty jug1 to ground
                new_state = (0, jug2)
            elif ( action[2] == '2' ): # empty jug1 into jug2
                new_state = ( max(0, (jug1-(capacity2-jug2))), min(capacity2, (jug2+jug1)) )
        elif ( action[1] == '2' ): # empty jug2 
            if ( action[2] == '0' ): # empty jug2 to ground
                new_state = (jug1, 0)
            elif ( action[2] == '1' ): # empty jug2 into jug1
                new_state = ( min(capacity1, (jug1+jug2)), max(0, (jug2-(capacity1-jug1))) )
    elif ( action[0] == '1' ): # fill the jug
        if ( action[1] == '1' ): # fill jug1 from tap
            new_state = (capacity1, jug2)
        elif ( action[1] == '2' ): # fill jug2 from tap
            new_state = (jug1, capacity2)

    # Convert numerical tuple to string
    state_str = tupleToString(new_state, 2)

    # Create child node based on heuristic given. If = 0, then just calculate as normal.
    if ( heuristic == 0 ):
        child_node = Node(state_str, curr_node, action, curr_node.path_cost+1)

    return child_node

def threeJugsGetChildNode(curr_node, jugs_str, action, heuristic):
        
    # jugs = (jug1, jug2, jug3) 
    # Possible actions:
    #   1) fill jug1   4) empty jug1  7) pour jug1 into jug2    10) pour jug2 into jug3
    #   2) fill jug2   5) empty jug2  8) pour jug1 into jug3    11) pour jug3 into jug1
    #   3) fill jug3   6) empty jug3  9) pour jug2 into jug1    12) pour jug3 into jug2

    # Get node state
    state_str = curr_node.state

    # Turn jugs string and state into numerical tuples
    jugs = stringToTuple(jugs_str, 3, 0)
    state = stringToTuple(state_str, 3, 0)

    jug1 = state[0]
    jug2 = state[1] 
    jug3 = state[2]
    capacity1 = jugs[0]
    capacity2 = jugs[1]
    capacity3 = jugs[2]

    if ( action == 1 ):     # fill jug1 from tap
        new_state = (capacity1, jug2, jug3)
    elif ( action == 2 ):   # fill jug2 from tap
        new_state = (jug1, capacity2, jug3)
    elif ( action == 3 ):   # fill jug3 from tap
        new_state = (jug1, jug2, capacity3)
    elif ( action == 4 ):   # empty jug1 to ground
        new_state = (0, jug2, jug3)
    elif ( action == 5 ):   # empty jug2 to ground
        new_state = (jug1, 0, jug3)
    elif ( action == 6 ):   # empty jug3 to ground
        new_state = (jug1, jug2, 0)
    elif ( action == 7 ):   # pour jug1 into jug2
        new_state = ( max(0, (jug1-(capacity2-jug2))), min(capacity2, (jug2+jug1)), jug3 )
    elif ( action == 8 ):   # pour jug1 into jug3
        new_state = ( max(0, (jug1-(capacity3-jug3))), jug2, min(capacity3, (jug3+jug1)))
    elif ( action == 9 ):   # pour jug2 into jug1
        new_state = ( min(capacity1, (jug1+jug2)), max(0, (jug2-(capacity1-jug1))), jug3 )
    elif ( action == 10 ):  # pour jug2 into jug3
        new_state = ( jug1, max(0, (jug2-(capacity3-jug3))), min(capacity3, (jug3+jug2)) )
    elif ( action == 11 ):  # pour jug3 into jug1
        new_state = ( min(capacity1, (jug1+jug3)), jug2, max(0, (jug3-(capacity1-jug1))) )
    else: # action == 12      pour jug3 into jug2
        new_state = ( jug1, min(capacity2, (jug2+jug3)), max(0, (jug3-(capacity2-jug2))) )
        
    # Convert numerical tuple to string
    state_str = tupleToString(new_state, 3)

     # Create child node based on heuristic given. If = 0, then just calculate as normal.
    if ( heuristic == 0 ):
        child_node = Node(state_str, curr_node, action, curr_node.path_cost+1)

    return child_node

def citiesGetChildNode(curr_node, action, heuristic, grid):

    # Turn string tuple to actual tuple
    action_tuple = stringToTuple(action, 3, 1)

    # If our current city is in tuple position 0, add tuple position 1 as the child node's state.
    if ( action_tuple[0] == curr_node.state ):
        city = action_tuple[1]
    else:
        # If our current city is in tuple position 1, add tuple position 0 as the child node's state.
        city = action_tuple[0]

    # The new path cost = curr_node's path cost + the cost of the path from city to city
    # Create child node based on heuristic given. If = 0, then just calculate as normal.
    if ( heuristic == 0 ):
        calculated_cost = curr_node.path_cost + action_tuple[2]
    elif ( heuristic == "euclidean" ):

        # Get cities
        cities = make_tuple(action)
        city1 = cities[0]
        city2 = cities[1]

        # Find cities in grid
        city1_position = [cit for cit in grid if cit[0] == city1][0]
        city2_position = [cit for cit in grid if cit[0] == city2][0]
        
        # Create two vectors from the points on the grid
        v1 = np.array([city1_position[1],city1_position[2]])
        v2 = np.array([city2_position[1],city2_position[2]])
        
        # Calculate euclidean distance
        calculated_cost = distance.euclidean(v1,v2)

    child = Node(city, curr_node, action, calculated_cost)

    return child

def tupleToString(tup, num_args):
    if ( num_args == 2):
        tuple_str = "(" + str(tup[0]) + ", " + str(tup[1]) + ")"
    else: # num_args == 3
        tuple_str = "(" + str(tup[0]) + ", " + str(tup[1]) + ", " + str(tup[2]) + ")"

    return tuple_str

def stringToTuple(tuple_str, num_args, tup_type):

    tmp = tuple_str.replace('(', '').replace(')','').replace(' ', '').split(",")

    if ( num_args == 2):
        tup = ( int(tmp[0]), int(tmp[1]) )
    else: # num_args == 3
        if( tup_type == 0 ):
            tup = ( int(tmp[0]), int(tmp[1]), int(tmp[2]) )
        else: # tup_type == 1
            tup = ( tmp[0], tmp[1], int(tmp[2]) )


    return tup

def jugsGoalTest(state, goal_state, numJugs):

    state_numerical = stringToTuple(state, numJugs, 0)
    goal_numerical = stringToTuple(goal_state, numJugs, 0)

    if ( state_numerical == goal_numerical ):
        return True
    else:
        return False

def citiesGoalTest(state, goal_state):
    if ( state == goal_state ):
        return True
    else:
        return False

# This method will print the solution to the console.
# Inputs:
#   solution_node = node that contains the goal state. If -1, no solution found.
#   time = total number of nodes created in search algorithm
#   space_frontier = biggest size that frontier list grew
#   space_explored = biggest size that explored list grew. If algorithm did not
#                    use a frontier list, this argument should be -1.
# Outputs:
#   None
def printSolution(solution_node, time, space_frontier, space_explored):
    
    # Check if solution node = -1
    if ( solution_node.path_cost == -1 ):
        print("No solution.")
        return
    
    # Print appropirate information to console.
    print("Solution path:")

    # Hold solution path in order
    solution_path = []

    # Extract path from root to solution
    while ( solution_node is not None ):
        solution_path.append(solution_node.state)
        solution_node = solution_node.parent

    # Print solution path, one state per line.
    while ( len(solution_path) != 0 ):
        print(solution_path.pop())

    print "Time: ", time
    print "Space - Frontier: ", space_frontier

    if (space_explored == -1 ):
        space_explored = "explored list not used"

    print "Space - Explored: ", space_explored

def getActions(puzzle, configuration, curr_node):
 
     # Get actions
    if ( puzzle == 'jugs' ):
        # Check if problem is 2 jugs or 3 jugs
        num_jugs = getNumJugs(configuration)
        jugs = configuration[1].strip()

        if ( num_jugs == 2 ): 
            actions = twoJugsGetActions(curr_node.state, jugs)
        else:
            actions = threeJugsGetActions(curr_node.state, jugs)
    elif ( puzzle == "cities" ):
        actions = citiesGetActions(configuration, curr_node)


    return actions

def getChildNode(puzzle, configuration, curr_node, action, heuristic):

    if ( puzzle == "jugs" ):
        num_jugs = getNumJugs(configuration)
        jugs = configuration[1].strip()

        if ( num_jugs == 2 ):
            child = twoJugsGetChildNode(curr_node, jugs, action, heuristic)
        else: # num_jugs == 3
            child = threeJugsGetChildNode(curr_node, jugs, action, heuristic )
    elif ( puzzle == "cities" ):
        # Extract grid of cities
        grid = make_tuple(configuration[1])
        child = citiesGetChildNode(curr_node, action, heuristic, grid)

    return child

def goalTest(puzzle, configuration, curr_state, goal_state):

    if ( puzzle == "jugs" ):
        # Check if problem is 2 jugs or 3 jugs
        num_jugs = getNumJugs(configuration)
        isGoalState = jugsGoalTest(curr_state, goal_state, num_jugs)
    elif ( puzzle == "cities" ):
        isGoalState = citiesGoalTest(curr_state, goal_state)
        

    return isGoalState

# Check if problem is 2 jugs or 3 jugs
def getNumJugs(configuration):
    jugs = configuration[1].strip()
    tmp = jugs.replace('(', '').replace(')','').split(",")
    num_jugs = len(tmp)

    return num_jugs

# This method reads in the .config file and returns information.
# Inputs:
#   config_filename = name of the configuration file from command line
# Outputs:
#   configuration = every line in config file given as a list
#   puzzle = line 0 of configuration, which is always the puzzle type.
#   initial_state = line 2 of the configuration, which always gives initial state.
#   goal_stae = line 3 of the configuration, which always gives the goal_state.
def readConfigFile(config_filename):
    # Open, read in, and close it config file.
    open_configuration = open(config_filename, 'r')
    configuration = open_configuration.readlines()
    open_configuration.close()

    # Read in puzzle type
    puzzle = configuration[0].strip()
    # Read in initial state on line 3
    initial_state = configuration[2].strip()
    # Read in goal state on line 4
    goal_state = configuration[3].strip()

    return configuration, puzzle, initial_state, goal_state

# Checks whether a node's state is in the frontier already.
# Inputs:
#   node = node to search for
#   frontier = frontier list to be searched
#   list_type = how frontier is implemented. 0 = stack, 1 = PriorityQueue
# Outputs:
#   is_in_frontier = boolean value set to whether or not the input node's
#                  state is already in the frontier list.
#   parent_cost = if a node state is found in the frontier, parent_cost represents 
#                 the path cost of that node in the frontier list
#   frontier_index = the index of where the duplicate node is in the frontier list
def isNodeInFrontier(node, frontier, list_type):
    
    node_state = node.state

    # If frontier is a stack so just search it like a normal list.
    # If frontier is a PriorityQueue, convert first to a queue --> f = frontier.queue().

    if ( list_type == 1 ):   
        # listType = PriorityQueue
        f = frontier.queue
    else: 
        # listType = stack 
        f = frontier
    
    is_in_frontier = False
    parent_cost = 0
    frontier_index = -1

    for i in range(0, len(f)):
        frontier_node = f[i]
        
        if ( frontier_node.state == node_state ):
            is_in_frontier = True
            parent_cost = frontier_node.path_cost
            frontier_index = i
            break

    return is_in_frontier, parent_cost, frontier_index

# Checks whether the state of the input node appears anywhere else
# from node to root
def isNodeInPathToRoot(node):

    is_node_in_path = False
    node_state = node.state
    parent = node.parent

    while ( parent is not None ):
        if ( parent.state == node.state ):
            is_node_in_path = True
            break
        parent = parent.parent

    return is_node_in_path

def main(argv):


    #q = PriorityQueue()
    #q.put(5)
    #q.put(10)
    #q.put(1)
    #q.put(8)
    #q.put(18)
    #q.put(3)
    #rawr = q.queue
    #print(rawr)
    #print(rawr[1])
    #rawr.pop(1)
    #print(rawr)
    #print('\n')
    #print(q.get())
    #print(q.get())
    #print(q.get())
    #print(q.get())
    #print(q.get())


    #return



    # Read in user input
    config_filename = argv[1]
    search_algorithm = argv[2]
    heuristic_function = None

    if ( len(argv) > 3 ):
        heuristic_function = argv[3]


    #################################################################
    
    if ( search_algorithm == "bfs" ):
        bfs(config_filename)
    elif ( search_algorithm == "dfs" ):
        dfs(config_filename)
    elif ( search_algorithm == "unicost" ):
        unicost(config_filename)
    elif ( search_algorithm == "greedy" ):
        greedy(config_filename, heuristic_function)


    #################################################################



if ( __name__ == "__main__" ):
    main(sys.argv)
