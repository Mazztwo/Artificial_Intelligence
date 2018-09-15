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
    if(puzzle == "jugs"):
        isGoalState = jugsGoalTest(root, goal_state)

        if ( isGoalState ):
            print("Jugs goal state found at root!")
            return root
        else:
            print("Jugs goal state NOT found at root!")


    # Frontier needs to be a FIFO queue.
    # New nodes go to back of queue.
    # Old nodes get expanded first from the front of the queue.
    
    #frontier <- a FIFO queue with node as the only element
    frontier = Queue()
    frontier.put(root)

    # Explored needs to be a hash table of some sort.

    # Goal test for each node done when node is generated 
    # and NOT when it is selected for expansion.

    # For each new puzzle type, you should only need to modify the functions 
    # relevant to setting up its state space search (e.g., get-successor-states, and goal-test, etc.)


def jugsGoalTest(node, goal_state):
    if(node.state == goal_state):
        return True
    else:
        return False

    



def main(argv):

    # Read in user input
    config_filename = argv[1]
    search_algorithm = argv[2]
    heuristic_function = None

    if(len(argv) > 3 ):
        heuristic_function = argv[3]

    print("\n")
    print("Configuration file name: %s" % config_filename)
    print("Search algorithm name: %s" % search_algorithm)
    if(heuristic_function != None):
        print("Heuristic function: %s" % heuristic_function)
    print("\n")

    
    #################################################################
    

    bfs(config_filename)


    #################################################################



if __name__ == "__main__":
    main(sys.argv)
