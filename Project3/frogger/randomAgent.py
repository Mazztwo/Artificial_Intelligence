from ple import PLE
import frogger_new
import numpy as np
from pygame.constants import K_w,K_a,K_s,K_d,K_F15
from pygame import Rect
import sys
import random
import pickle


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
#   0 = road
#   1 = car
#   2 = turtle/log 
#   3 = water
#   4 = home
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
    def pickAction(self, reward, obs):

        # return K_F15

        # Pick a random action at first, else return the normal argmax
        # Take a random action (chosen uniformly). A larger value for EXPLORATION_FACTOR will increase exploration.
        if ( random.uniform(0, 1) < EXPLORATION_FACTOR ):
            return random.choice([0,1,2,3,4]) 
        else:
            # Must convert obs to state, then look it up in the Q_table
            state = obsToState(obs)
             # If state is not in Q-table, add it
            if ( state not in Q_TABLE.keys() ):
                Q_TABLE[state] = np.zeros(NUM_ACTIONS)
            # If state is in Q-table, then return argmax of that state
            return np.argmax(Q_TABLE[state])
                        
def obsToState(obs):
    
    frog_x = obs['frog_x']
    frog_y = obs['frog_y']
   
    # Check if frog is before median. If so only check car objects.
    if ( frog_y < 261 ):

        # If there isn't a car, then there is road
        frog_n = 0
        frog_s = 0
        frog_e = 0
        frog_w = 0

        # Check the position of every car
        for car in obs['cars']:
            # Check frog_n
            if ( (car.y + car.h) >= frog_y ):
                frog_n = 1
            # Check frog_s
            if ( car.y  <= (frog_y+32) ):
                frog_s = 1
            # Check frog_e
            if ( (car.x + car.w) >= frog_x ):
                frog_e = 1
            # Check frog_w
            if ( car.x  <= (frog_x+32) ):
                frog_w = 1
    # Frog is at the median
    elif (frog_y == 261):
        
        # North of frog is either river or river object
        frog_n = 3
        # South of frog is either car or road
        frog_s = 0
        # East/West of car is road
        frog_e = 0
        frog_w = 0

        # Check north of frog for river object
        for riverob in obs['rivers']:
            # Check frog_n
            if ( (riverob.y + riverob.h) >= frog_y ):
                frog_n = 2

        # Check south of frog for car
        for car in obs['cars']:
            # Check frog_s
            if ( car.y  <= (frog_y+32) ):
                frog_s = 1
    # Frog is somewhere in the river
    else:

        # If there isn't a river object, then there is water
        frog_n = 3
        frog_s = 3
        frog_e = 3
        frog_w = 3

        # Must check all river objects W
        for riverob in obs['rivers']:
            # Check frog_n
            if ( (riverob.y + riverob.h) >= frog_y ):
                frog_n = 2
            # Check frog_s
            if ( riverob.y  <= (frog_y+32) ):
                frog_s = 2
            # Check frog_e
            if ( (riverob.x + riverob.w) >= frog_x ):
                frog_e = 2
            # Check frog_w
            if ( riverob.x  <= (frog_x+32) ):
                frog_w = 2

        # Check if there is a home in front of frog
        for home in obs['homeR']:
            # Only need to check frog_n
            if ( (home.y + home.h) >= frog_y ):
                frog_n = 4

    return State(frog_x,frog_y,frog_n,frog_s,frog_e,frog_w)

def readConfigFile(config_filename):
    # Open, read in, and close it config file.
    open_configuration = open(config_filename, 'rb')
    Q_TABLE = pickle.load(open_configuration)
    open_configuration.close()

    return Q_TABLE

def writeConfigFile(config_filename):
    # Open, write out Q-table, and close it config file.
    open_configuration = open(config_filename, 'wb')
    pickle.dump(Q_TABLE, open_configuration)
    open_configuration.close()

game = frogger_new.Frogger()
fps = 30
p = PLE(game, fps=fps,force_fps=False)
agent = NaiveAgent(p.getActionSet())
reward = 0.0

# PARAMATERS
###################
DISCOUNT = 1
ALPHA = 0.5
EXPLORATION_FACTOR = 0.7
###################

# Available actions to agent
AVAILABLE_ACTIONS = [K_F15, K_w, K_s, K_a, K_d]

# no-op, up, down, left, right
NUM_ACTIONS = 5

# Initial start of game flag from command line
#   if flag = 1, then it's the very beginning of the game (first time running), training from scratch
#   if flag = 0, then it's some iteration of the game other than the first, training from previously calculated Q-table
start_of_game = int(sys.argv[1])

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
    start_state = State(state['frog_x'], state['frog_y'], 0, 0, 0, 0 )
  
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

# Game loop
while ( True ):
    if ( p.game_over() ):
        # Save Q_TABLE to file
        writeConfigFile(config_filename)
        p.reset_game()

    action = agent.pickAction(reward, state)
    reward = p.act(AVAILABLE_ACTIONS[action])

    #reward = p.act(action)
    #print reward
    #continue

    next_obs = game.getGameState()
    next_state = obsToState(next_obs)
    reg_state = obsToState(state)

    # If next_state is not in Q-table, add it
    if ( next_state not in Q_TABLE.keys() ):
        Q_TABLE[next_state] = np.zeros(NUM_ACTIONS)

    # Update curr Q in Q-table
    currQ = Q_TABLE[reg_state][action]
    Q_TABLE[reg_state][action] = currQ + (ALPHA * ((reward + (DISCOUNT * (np.max(Q_TABLE[next_state]))))-currQ))

    state = next_obs

    # print game.score

