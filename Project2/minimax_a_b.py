#################################################################
#
# Alessio Mazzone
# ALM388@pitt.edu
#
# CS 1571 Aritificial Intelligence
#
# Project 2
#
#################################################################

import sys
from ast import literal_eval as make_tuple
from numpy import inf

# Reads game file config and returns a list of lists/tuples
def readGameFile(config_filename):
    # Open, read in, and close it config file.
    open_configuration = open(config_filename, 'r')
    configuration = open_configuration.readlines()
    open_configuration.close()

    # Read in game tree and create tuple
    state = make_tuple( configuration[0].strip().replace(" ","") )
 
    return state

# Vanilla minimax algorithm
def minimax(state):

    # Keep track of nodes visited
    visited = []
    visited.append(state[0])
    
    # Start recursion
    v, visited = maxValue(state, visited)

    print "MINIMAX:"
    print "Utility value: ", v
    print "Nodes in order visited: ", visited 
    print "\n"

# Minimax with alpha beta pruning
def minimax_a_b(state):
    
    # Keep track of nodes visited
    visited = []
    visited.append(state[0])
    
    # Start recursion
    v, visited = maxValueAB(state, visited, -inf, inf)

    print "MINIMAX_a_b:"
    print "Utility value: ", v
    print "Nodes in order visited: ", visited 

# maxValue method for vanillia minimax as per the book's algorithm
def maxValue(state, visited):
    # Terminal test
    if ( terminalTest(state) ):
        return utility(state), visited
    
    v = -inf

    for s in successors(state):
        visited.append(s[0])
        v_temp, visited_temp = minValue(s,visited)
        v = max(v, v_temp)
        visited = visited_temp

    return v, visited

# maxValue method for alpha beta pruning as per the book's algorithm
def maxValueAB(state, visited, alpha, beta):
    # Terminal test
    if ( terminalTest(state) ):
        return utility(state), visited
    
    v = -inf

    for s in successors(state):
        visited.append(s[0])
        v_temp, visited_temp = minValueAB(s,visited, alpha, beta)
        v = max(v, v_temp)
        visited = visited_temp

        if ( v >= beta ):
            return v, visited

        alpha = max(alpha, v)

    return v, visited

# minValue method for vanillia minimax as per the book's algorithm
def minValue(state, visited):
    # Terminal test
    if ( terminalTest(state) ):
        return utility(state), visited
    
    v = inf
  
    for s in successors(state):
        visited.append(s[0])
        v_temp, visited_temp = maxValue(s,visited)
        v = min(v, v_temp)
        visited = visited_temp

    return v, visited

# minValue method for alpha beta pruning as per the book's algorithm
def minValueAB(state, visited, alpha, beta):
    # Terminal test
    if ( terminalTest(state) ):
        return utility(state), visited
    
    v = inf

    for s in successors(state):
        visited.append(s[0])
        v_temp, visited_temp = maxValueAB(s,visited, alpha, beta)
        v = min(v, v_temp)
        visited = visited_temp

        if ( v <= alpha ):
            return v, visited

        beta = min(beta, v)

    return v, visited

# Given a state, return all children of that state from left to right
def successors(state):

    # Case 1:
    # regular state = [name, arrray1, array2, ...]
    #
    # Case 2:
    # state with leaves = [name, tuple1, tuple2, ...]
    #
    # Case 3: 
    # terminal state = (tuple) 

    return state[1:len(state)]
  
# Check if a state is a leaf node. 
# If it is, return true. Else return false
def terminalTest(state):
    if ( isinstance(state, tuple) ):
        return True
    else:
        return False

# Given a leaf node tuple, return its utility value
def utility(state):
    # Leaf node is always a tuple in the form (name, utility value)
    return state[1]

def main(argv):

    # Read in user input
    config_filename = argv[1]

    # Create game state
    state = readGameFile(config_filename)

    # Call both algorithms
    minimax(state)
    minimax_a_b(state)


if ( __name__ == "__main__" ):
    main(sys.argv)
