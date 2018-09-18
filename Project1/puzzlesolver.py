#################################################################
#
# Alessio Mazzone
# ALM388@pitt.edu
#
#
# CS 1571 Aritificial Intelligence
#
#
# Project 1 
#
#################################################################


import sys
from collections import deque

class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    # maybe..
    def printNode(self):
        print("NODE -- state: , parent: ")
     
def bfs(config_filename):

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

    # Time --> Total number of nodes created
    time = 0

    # node <- a node with STATE = problem.initial-state, pathcost = 0
    root = Node(initial_state,None,None,0)
    time += 1

    # if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    isGoalState = goalTest(puzzle, configuration, root.state, goal_state)
    if ( isGoalState ):
        printSolution(root, time, 0, 0)
 
    # biggest size that frontier list grows to
    space_frontier = 0

    # Frontier needs to be a FIFO queue.
    # New nodes go to back of queue.
    # Old nodes get expanded first from the front of the queue.
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
            printSolution(-1,0,0,0)
            return

        # Get the current node from frontier
        curr_node = frontier.popleft()

        # Add current node's state to explored
        explored[counter] = curr_node.state
        counter += 1

        actions = getActions(puzzle, configuration, curr_node)

        for action in actions:
            # child <-- CHILD-NODE(problem,curr_node,action)
            child = getChildNode(puzzle, configuration, curr_node, action)
            time += 1

            # if child.STATE is not in explored or frontier then
            #   if problem.GOAL-TEST(child.STATE) then return SOLUTION(child) 
            #   frontier <-- INSERT(child,frontier)
            child_state = child.state

            # Check that state is not in explored --> or frontier...? How to check for value in queue...?
            if ( child_state not in explored.values() ):
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
    jugs = stringToTuple(jugs_str, 2)
    state = stringToTuple(state_str, 2)

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
    jugs = stringToTuple(jugs_str, 3)
    state = stringToTuple(state_str, 3)

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

def twoJugsGetChildNode(curr_node, jugs_str, action):
    
    # Get node state
    state_str = curr_node.state

    # Turn jugs string and state into numerical tuples
    jugs = stringToTuple(jugs_str, 2)
    state = stringToTuple(state_str, 2)

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

    # Create child node
    child_node = Node(state_str, curr_node, action, 0)

    return child_node

def threeJugsGetChildNode(curr_node, jugs_str, action):
        
    # jugs = (jug1, jug2, jug3) 
    # Possible actions:
    #   1) fill jug1   4) empty jug1  7) pour jug1 into jug2    10) pour jug2 into jug3
    #   2) fill jug2   5) empty jug2  8) pour jug1 into jug3    11) pour jug3 into jug1
    #   3) fill jug3   6) empty jug3  9) pour jug2 into jug1    12) pour jug3 into jug2

    # Get node state
    state_str = curr_node.state

    # Turn jugs string and state into numerical tuples
    jugs = stringToTuple(jugs_str, 3)
    state = stringToTuple(state_str, 3)

    jug1 = state[0]
    jug2 = state[1] 
    jug3 = state[2]
    capacity1 = jugs[0]
    capacity2 = jugs[1]
    capacity3 = jugs[2]

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

    elif ( action == 9 ):   # pour jug2 into jug1

    elif ( action == 10 ):  # pour jug2 into jug3
        
    elif ( action == 11 ):  # pour jug3 into jug1
        pass
    else: # action == 12      pour jug3 into jug2
        pass
        


    # Convert numerical tuple to string
    state_str = tupleToString(new_state, 2)

    # Create child node
    child_node = Node(state_str, curr_node, action, 0)

    return child_node

def tupleToString(tup, num_args):
    if ( num_args == 2):
        tuple_str = "(" + str(tup[0]) + ", " + str(tup[1]) + ")"
    else: # num_args == 3
        tuple_str = "(" + str(tup[0]) + ", " + str(tup[1]) + ", " + str(tup[2]) + ")"

    return tuple_str

def stringToTuple(tuple_str, num_args):
    if ( num_args == 2):
        tmp = tuple_str.replace('(', '').replace(')','').split(",")
        tup = ( int(tmp[0]), int(tmp[1]) )
    else: # num_args == 3
        tmp = tuple_str.replace('(', '').replace(')','').split(",")
        tup = ( int(tmp[0]), int(tmp[1]), int(tmp[2]) )

    return tup

def jugsGoalTest(state, goal_state):
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
    if ( solution_node == -1 ):
        print("No solution.")
        return
    
    # Print appropirate information to console.
    print("Solution path:")

    # Hold solution path in order
    solution_path = []

    # Extract path from root to solution
    while ( solution_node != None ):
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
        jugs = configuration[1].strip()
        tmp = jugs.replace('(', '').replace(')','').split(",")
        num_jugs = len(tmp)

        if ( num_jugs == 2 ): 
            actions = twoJugsGetActions(curr_node.state, jugs)
        else:
            actions = threeJugsGetActions(curr_node.state, jugs)


    return actions

def getChildNode(puzzle, configuration, curr_node, action):

    if ( puzzle == "jugs" ):
        jugs = configuration[1].strip()
        child = twoJugsGetChildNode(curr_node, jugs, action)

    return child

def goalTest(puzzle, configuration, curr_state, goal_state):

    if ( puzzle == "jugs" ):
        isGoalState = jugsGoalTest(curr_state, goal_state)
        

    return isGoalState


def main(argv):

    # Read in user input
    config_filename = argv[1]
    search_algorithm = argv[2]
    heuristic_function = None

    if ( len(argv) > 3 ):
        heuristic_function = argv[3]

    
    #################################################################
    
    if ( search_algorithm == "bfs" ):
        bfs(config_filename)


    #################################################################



if ( __name__ == "__main__" ):
    main(sys.argv)
