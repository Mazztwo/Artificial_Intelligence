from ple import PLE
import frogger_new
import numpy as np
from pygame.constants import K_w,K_a,K_s,K_d,K_F15
import sys
import random
from ast import literal_eval as make_dictionary



# state representation:
#  
# 'frog_x':  x position of frog
# 'frog_y':  y position of frog
# 'frog_n':  value for what is directly north of frog
# 'frog_s':  value for what is directly south of frog
# 'frog_e':  value for what is directly east of frog
# 'frog_w':  value for what is directly west of frog
#   
#
# possible values for frog_n,s,e,w:
#  -1 = edge
#   0 = nothing
#   1 = car
#   2 = turtle --> how to tell between water and blank....?
#   3 = water
#   4 = log
#   5 = home
class State:
    
    def __init__(self, frog_x, frog_y, frog_n, frog_s, frog_e, frog_w):
        self.frog_x = frog_x
        self.frog_y = frog_y
        self.frog_n = frog_n
        self.frog_s = frog_s
        self.frog_e = frog_e
        self.frog_w = frog_w
        
    def __eq__(self, other):
        return isinstance(other, State) and self.frog_x == other.frog_x and self.frog_y == other.frog_y and self.frog_n == other.frog_n and self.frog_s == other.frog_s and self.frog_e == other.frog_e and self.frog_w == other.frog_w

    def __hash__(self):
        return hash(str(self.frog_x) + str(self.frog_y) + str(self.frog_n) + str(self.frog_s) + str(self.frog_e) + str(self.frog_w))
    



class NaiveAgent():
    def __init__(self, actions):
        self.actions = actions
        self.step = 0
        self.NOOP = K_F15

    # This is where we will set up our Q-Learning Code
    #   reward   = reward you received for your last action/state
    #   obs      = current game state
    def pickAction(self, reward, curr_game_state):

        return K_F15
        #return K_d

        # We must write some sort of obs to state converter in here...




        # return K_a, K_w, K_s, K_d, or self.NOOP

        #Uncomment the following line to get random actions
        #return self.actions[np.random.randint(0,len(self.actions))]

def readConfigFile(config_filename):
    # Open, read in, and close it config file.
    open_configuration = open(config_filename, 'r')
    configuration = open_configuration.readlines()
    open_configuration.close()

    # Create dictionary from string
    Q_TABLE = make_dictionary(configuration[0].strip())

    return Q_TABLE

def writeConfigFile(config_filename):
    # Open, read in, and close it config file.
    open_configuration = open(config_filename, 'w')
    configuration = open_configuration.writelines()
    open_configuration.close()

    # Read in puzzle type
    puzzle = configuration[0].strip()
    # Read in initial state on line 3
    initial_state = configuration[2].strip()
    # Read in goal state on line 4
    goal_state = configuration[3].strip()

    return configuration, puzzle, initial_state, goal_state

game = frogger_new.Frogger()
fps = 30
p = PLE(game, fps=fps,force_fps=False)
agent = NaiveAgent(p.getActionSet())
reward = 0.0

# PARAMATERS
###################
discount = 0.9
alpha = 0.5
###################

# Initial start of game flag from command line
#   if flag = 1, then it's the very beginning of the game (first time running), training from scratch
#   if flag = 0, then it's some iteration of the game other than the first, training from previously calculated Q-table
start_of_game = int(sys.argv[1])

# no-op, up, down, left, right
NUM_ACTIONS = 5

# File where Q-table is stored
config_filename = 'FROG.config'

# Initial vanilla game state
state = game.getGameState()

if ( start_of_game ):
    # Initialize Q-table as an empty dictionary

    # Q-Table structure
    # 
    #   state | K_F15 | K_w | K_s | K_a | K_d |
    #   ------|-------|-----|-----|-----|-----|
    #    s1   |  0.0  | 0.0 | 0.0 | 0.0 | 0.0 |  
    #    s2   |  0.0  | 0.0 | 0.0 | 0.0 | 0.0 | 
    #    s3   |  0.0  | 0.0 | 0.0 | 0.0 | 0.0 | 
    #    
    # etc..
    Q_TABLE = dict()

    # Initialize start state - modified
    start_state = State(state['frog_x'], state['frog_y'], 0, -1, 0, 0 )
  
     # Create Q0 here for every possible action
    #   Q0(start_state,K_F15) = 0
    #   Q0(start_state,K_w) = 0
    #   Q0(start_state,K_s) = 0
    #   Q0(start_state,K_a) = 0  
    #   Q0(start_state,K_d) = 0
    Q_TABLE[start_state] = np.zeros(NUM_ACTIONS)

else:

    # Read in Q_TABLE from FROG.config
    Q_TABLE = readConfigFile(config_filename)
    pass


# Game loop
while ( True ):
    if ( p.game_over() ):
        # Save Q_TABLE to file

        p.reset_game()

    action = agent.pickAction(reward, state)
    reward = p.act(action)
    curr_state = game.getGameState()

    # Calculate all Q's down here
    # Read in Q from some table, etc.



    state = curr_state

    # print game.score


# Close config file?