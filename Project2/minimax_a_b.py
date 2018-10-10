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
import math

def readGameFile(config_filename):
    # Open, read in, and close it config file.
    open_configuration = open(config_filename, 'r')
    configuration = open_configuration.readlines()
    open_configuration.close()

    # Read in game tree and create tuple
    state = make_tuple( configuration[0].strip().replace(" ","") )
 
    return state

def minimax(state):

    visited = []
    visited.append(state[0])
    
    v, visited = maxValue(state,visited)

    print "Utility value: ", v
    print "Nodes in order visited: ", visited 

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


def minimax_a_b(game_tree):
    pass


def main(argv):

    # Read in user input
    config_filename = argv[1]

    state = readGameFile(config_filename)

    minimax(state)


if ( __name__ == "__main__" ):
    main(sys.argv)
