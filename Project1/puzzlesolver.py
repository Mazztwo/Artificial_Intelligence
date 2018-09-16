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
from Queue import *

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
    print("Puzzle type: %s" % puzzle)

    # Read in initial state on line 3
    initial_state = configuration[2].strip()
    print("Initial state: %s" % initial_state)

    # Read in goal state on line 4
    goal_state = configuration[3].strip()
    print("Goal state: %s" % goal_state)

    # node <- a node with STATE = problem.initial-state, pathcost = 0
    root = Node(initial_state,None,None,0)

    # if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    if ( puzzle == "jugs" ):
        isGoalState = jugsGoalTest(root, goal_state)

        if ( isGoalState ):
            print("Jugs goal state found at root!")
            return root
        else:
            print("Jugs goal state NOT found at root!")


    # Frontier needs to be a FIFO queue.
    # New nodes go to back of queue.
    # Old nodes get expanded first from the front of the queue.
    # frontier <- a FIFO queue that stores nodes
    frontier = Queue()
    frontier.put(root)
    print("Frontier size: %d" % frontier.qsize())

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
    #   for each action in problem.ACTIONS(curr_node.STATE) do
    #       child <-- CHILD-NODE(problem,curr_node,action)
    #       if child.STATE is not in explored or frontier then
    #           if problem.GOAL-TEST(child.STATE) then return SOLUTION(child) 
    #           frontier <-- INSERT(child,frontier)
    keep_going = True
    while ( keep_going ):
        if ( frontier.empty() ): 
            return "No solution."
        
        # Get the current node from frontier
        curr_node = frontier.get()

        # Add current node's state to explored
        explored[counter] = curr_node.state
        counter += 1

        # Get actions
        if ( puzzle == 'jugs' ):
            jugs = configuration[1].strip()
            actions = twoJugsGetActions(curr_node.state, jugs)

        print "Actions: ", actions




    # Goal test for each node done when node is generated 
    # and NOT when it is selected for expansion.

    # For each new puzzle type, you should only need to modify the functions 
    # relevant to setting up its state space search (e.g., get-successor-states, and goal-test, etc.)


# Given a state, this function will return all possible actions for the jug puzzle
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
def twoJugsGetActions(state_str, jugs_str):

    # Turn jugs string and state into numerical tuples
    tmp = jugs_str.replace('(', '').replace(')','').split(",")
    jugs = ( int(tmp[0]), int(tmp[1]) )

    tmp = state_str.replace('(', '').replace(')','').split(",")
    state = ( int(tmp[0]), int(tmp[1]) )

    # Create empty actions array
    actions = []

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
        if ( jug2 < capacity ):
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
        if ( jug1 < capacity ):
            # Empty jug1 into jug2
            actions.append("021")

    return actions

def threeJugsGetActions(state, jugs):
    pass

def jugsGoalTest(node, goal_state):
    if ( node.state == goal_state ):
        return True
    else:
        return False

    



def main(argv):

    # Read in user input
    config_filename = argv[1]
    search_algorithm = argv[2]
    heuristic_function = None

    if ( len(argv) > 3 ):
        heuristic_function = argv[3]

    print("\n")
    print("Configuration file name: %s" % config_filename)
    print("Search algorithm name: %s" % search_algorithm)
    if ( heuristic_function != None ):
        print("Heuristic function: %s" % heuristic_function)
    print("\n")

    
    #################################################################
    

    bfs(config_filename)


    #################################################################



if ( __name__ == "__main__" ):
    main(sys.argv)
