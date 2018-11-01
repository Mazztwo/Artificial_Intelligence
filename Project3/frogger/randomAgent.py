from ple import PLE
import frogger_new
import numpy as np
from pygame.constants import K_w,K_a,K_s,K_d,K_F15
import sys

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

    # Read in puzzle type
    puzzle = configuration[0].strip()
    # Read in initial state on line 3
    initial_state = configuration[2].strip()
    # Read in goal state on line 4
    goal_state = configuration[3].strip()

    return configuration, puzzle, initial_state, goal_state

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



# PARAMATERS
###################
discount = 0.9
alpha = 0.5
###################

# Initial start of game flag
#   if flag = 0, then it's the very beginning of the game (first time running)
#   if flag > 0, then it's some iteration of the game other than the first
start_of_game = 0
game = frogger_new.Frogger()
fps = 30
p = PLE(game, fps=fps,force_fps=False)
agent = NaiveAgent(p.getActionSet())
reward = 0.0

config_filename = 'FROG.config'


# p.init()
# initialize all values here
starting_state = game.getGameState()

# state representation:
# some_state = 
# {
#    'frog_x':  x position of frog,
#    'frog_y':  y position of frog,
#    'frog_n':  value for what is directly north of frog,
#    'frog_s':  value for what is directly north of frog,
#    'frog_e':  value for what is directly north of frog,
#    'frog_w':  value for what is directly north of frog,
#    'actions': array of possible actions at this state
#    'N':       number of times this state has been visited
# }
# 
#
# possible values for frog_n,s,e,w:
#  -1 = edge
#   0 = nothing
#   1 = car
#   2 = turtle
#   3 = water
#   4 = log
#   5 = home
#
#
# actions array can look something like this if the frog is on the left edge:
#   actions = [K_F15, K_w, K_s, k_d]



vanilla_state = {
    'frog_x': starting_state['frog_x'],
    'frog_y': starting_state['frog_y'],
    'frog_n': 0,
    'frog_s': -1,
    'frog_e': 0,
    'frog_w': 0,

}

# Create Q0 here for every possible action
#   Q0(vanilla_state,K_F15) = 0
#   Q0(vanilla_state,K_a) = 0
#   Q0(vanilla_state,K_s) = 0
#   Q0(vanilla_state,K_d) = 0
#   Q0(vanilla_state,K_w) = 0



# Game loop
while ( True ):
    if ( p.game_over() ):
        # Save current learned values some how

        p.reset_game()

    # We need to hijack this. We can use the getGameState() function, but we need to scrub it
    # in order to set our state to something much smaller.
    curr_game_state = game.getGameState()
    #print "X: ", curr_game_state["frog_x"]
    #print "Y:", curr_game_state["frog_y"]

    action = agent.pickAction(reward, curr_game_state)
    reward = p.act(action)
    #print game.score


# Close config file?