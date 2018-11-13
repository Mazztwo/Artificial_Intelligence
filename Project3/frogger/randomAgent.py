from ple import PLE
import frogger_new
import numpy as np
from pygame.constants import K_w,K_a,K_s,K_d,K_F15
from pygame import Rect
from constants import kPlayYHomeLimit, kPlayYRiverLimit
import sys
import random
import pickle


class State1:

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
    #
    #           X
    #        X frog X
    #           X

    def __init__(self, frog_x, frog_y, frog_n, frog_s, frog_e, frog_w):
        self.frog_x = frog_x
        self.frog_y = frog_y
        self.frog_n = frog_n
        self.frog_s = frog_s
        self.frog_e = frog_e
        self.frog_w = frog_w
        
    def __eq__(self, other):
        return isinstance(other, State1) and self.frog_x == other.frog_x and self.frog_y == other.frog_y and self.frog_n == other.frog_n and self.frog_s == other.frog_s and self.frog_e == other.frog_e and self.frog_w == other.frog_w

    def __hash__(self):
        return hash(str(self.frog_x) + str(self.frog_y) + str(self.frog_n) + str(self.frog_s) + str(self.frog_e) + str(self.frog_w))
  
class State2:

    # state representation:
    #  
    # 'frog_n':  value for what is directly north of frog
    # 'frog_n2': value for what is directly two north of frog
    # 'frog_s':  value for what is directly south of frog
    # 'frog_s2': value for what is directly two south of frog
    # 'frog_e':  value for what is directly east of frog
    # 'frog_e2': value for what is directly two east of frog
    # 'frog_w':  value for what is directly west of frog
    # 'frog_w2':  value for what is directly two west of frog
    #   
    #
    # possible values for frog_n,s,e,w:
    #   0 = road
    #   1 = car
    #   2 = turtle/log 
    #   3 = water
    #   4 = home
    #
    #
    ##          X
    #           X
    #      X  X frog X X
    #           X
    #           X
    #
    def __init__(self, frog_n, frog_n2, frog_s, frog_s2, frog_e, frog_e2, frog_w, frog_w2):
        self.frog_n = frog_n
        self.frog_s = frog_s
        self.frog_e = frog_e
        self.frog_w = frog_w
        self.frog_n2 = frog_n2
        self.frog_s2 = frog_s2
        self.frog_e2 = frog_e2
        self.frog_w2 = frog_w2
        
    def __eq__(self, other):
        return isinstance(other, State2) and self.frog_n == other.frog_n and self.frog_s == other.frog_s and self.frog_e == other.frog_e and self.frog_w == other.frog_w and self.frog_n2 == other.frog_n2 and self.frog_s2 == other.frog_s2 and self.frog_e2 == other.frog_e2 and self.frog_w2 == other.frog_w2

    def __hash__(self):
        return hash(str(self.frog_n) + str(self.frog_n2) + str(self.frog_s) + str(self.frog_s2) + str(self.frog_e) + str(self.frog_e2) + str(self.frog_w) + str(self.frog_w2))
    
class State3:
    
    # state representation:
    #
    #   SKIPS 12 BECAUSE THAT IS FROG 
    #
    # 'frog_0'  'frog_4'    'frog_8'   'frog_13'   'frog_17'    'frog_21'
    # 'frog_1'  'frog_5'    'frog_9'   'frog_14'   'frog_18'    'frog_22'
    # 'frog_2'  'frog_6'    'frog_10'  'frog_15'   'frog_19'    'frog_23'
    # 'frog_3'  'frog_7'    'frog_11'  'frog_16'   'frog_20'    'frog_24'
    #   
    #
    # possible values for frog_#
    #  -1 = beyond edge
    #   0 = road
    #   1 = car
    #   2 = turtle/log 
    #   3 = water
    #   4 = home
    #
    #     0  1  2  3  4
    #     5  6  7  8  9  
    #     10 11 F 13 14
    #     15 16 17 18 19
    #     20 21 22 23 24
    #    
    #     X  X  X  X  X
    #     X  X  X  X  X
    #     X  X frg X  X
    #     X  X  X  X  X
    #     X  X  X  X  X
    #
    def __init__(self, f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24):
        self.f0 = f0
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.f4 = f4
        self.f5 = f5
        self.f6 = f6
        self.f7 = f7
        self.f8 = f8
        self.f9 = f9
        self.f10 = f10
        self.f11 = f11
        self.f13 = f13
        self.f14 = f14
        self.f15 = f15
        self.f16 = f16
        self.f17 = f17
        self.f18 = f18
        self.f19 = f19
        self.f20 = f20
        self.f21 = f21
        self.f22 = f22
        self.f23 = f23
        self.f24 = f24
        
    def __eq__(self, other):
        return isinstance(other, State3) and self.f0 == other.f0 and self.f1 == other.f1 \
                                         and self.f2 == other.f2 and self.f3 == other.f3 \
                                         and self.f4 == other.f4 and self.f5 == other.f5 \
                                         and self.f6 == other.f6 and self.f7 == other.f7 \
                                         and self.f8 == other.f8 and self.f9 == other.f9 \
                                         and self.f10 == other.f10 and self.f11 == other.f11 \
                                         and self.f13 == other.f13 and self.f14 == other.f14 \
                                         and self.f15 == other.f15 and self.f16 == other.f16 \
                                         and self.f17 == other.f17 and self.f18 == other.f18 \
                                         and self.f19 == other.f19 and self.f20 == other.f20 \
                                         and self.f21 == other.f21 and self.f22 == other.f22 \
                                         and self.f23 == other.f23 and self.f24 == other.f24 

    def __hash__(self):
        return hash(str(self.f0) + str(self.f1) + str(self.f2) + str(self.f3) + str(self.f4) \
                  + str(self.f5) + str(self.f6) + str(self.f7) + str(self.f8) + str(self.f9) \
                  + str(self.f10) + str(self.f11) + str(self.f13) + str(self.f14) \
                  + str(self.f15) + str(self.f16) + str(self.f17) + str(self.f18) + str(self.f19) \
                  + str(self.f20) + str(self.f21) + str(self.f22) + str(self.f23) + str(self.f24))

class NaiveAgent():
    
    def __init__(self, actions):
        self.actions = actions
        self.step = 0
        self.NOOP = K_F15

    # This is where we will set up our Q-Learning Code
    #   reward   = reward you received for your last action/state
    #   obs      = current game state
    def pickAction(self, reward, obs):

        # Must convert obs to state, then look it up in the Q_table
        state = obsToState3(obs)

        # If state is not in Q-table, add it
        if ( state not in Q_TABLE.keys() ):
            Q_TABLE[state] = np.zeros(NUM_ACTIONS)

        # Pick a random action at first, else return the normal argmax
        # Take a random action (chosen uniformly). A larger value for EXPLORATION_FACTOR will increase exploration.
        if ( random.uniform(0, 1) < EXPLORATION_FACTOR ):
            return random.choice([0,1,2,3,4]) 
        else:
            # Return argmax
            return np.argmax(Q_TABLE[state])

def obsToState1(obs):
    
    frog_x = obs['frog_x']
    frog_y = obs['frog_y']
   
    # Check if frog is before median. If so only check car objects.
    if ( frog_y < 229 ):

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
        # East/West of frog is road
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

    return State1(frog_x,frog_y,frog_n,frog_s,frog_e,frog_w)

def obsToState2(obs):
    
    frog_x = obs['frog_x']
    frog_y = obs['frog_y']
   
    # Check if frog is before median. If so only check car objects.
    if ( frog_y < 229 ):

        # If there isn't a car, then there is road
        frog_n = 0
        frog_s = 0
        frog_e = 0
        frog_w = 0
        frog_n2 = 0
        frog_s2 = 0
        frog_e2 = 0
        frog_w2 = 0

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
            # Check frog_n2
            if ( 2*(car.y + car.h) >= frog_y ):
                frog_n2 = 1
            # Check frog_s2
            if ( 2*car.y  <= (frog_y+32) ):
                frog_s2 = 1
            # Check frog_e2
            if ( 2*(car.x + car.w) >= frog_x ):
                frog_e2 = 1
            # Check frog_w2
            if ( 2*car.x  <= (frog_x+32) ):
                frog_w2 = 1
    # Frog is one space from median, check both cars and rivers to the north
    elif ( frog_y < 261 and frog_y > 229 ):
        frog_n = 0
        frog_s = 0
        frog_e = 0
        frog_w = 0
        frog_n2 = 3 # 2 spaces up is water
        frog_s2 = 0
        frog_e2 = 0
        frog_w2 = 0  

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
            # Check frog_n2
            if ( 2*(car.y + car.h) >= frog_y ):
                frog_n2 = 1
            # Check frog_s2
            if ( 2*car.y  <= (frog_y+32) ):
                frog_s2 = 1
            # Check frog_e2
            if ( 2*(car.x + car.w) >= frog_x ):
                frog_e2 = 1
            # Check frog_w2
            if ( 2*car.x  <= (frog_x+32) ):
                frog_w2 = 1

        # Check north of frog for river object
        for riverob in obs['rivers']:
            # Check frog_n2
            if ( 2*(riverob.y + riverob.h) >= frog_y ):
                frog_n2 = 2
    # Frog is at the median
    elif (frog_y == 261):
        
        # North of frog is either river or river object
        frog_n = 3
        # South of frog is either car or road
        frog_s = 0
        # East/West of frog is road
        frog_e = 0
        frog_w = 0

        frog_n2 = 3
        frog_s2 = 0
        frog_e2 = 0
        frog_w2 = 0
        

        # Check north of frog for river object
        for riverob in obs['rivers']:
            # Check frog_n
            if ( (riverob.y + riverob.h) >= frog_y ):
                frog_n = 2
            if ( 2*(riverob.y + riverob.h) >= frog_y ):
                frog_n2 = 2

        # Check south of frog for car
        for car in obs['cars']:
            # Check frog_s
            if ( car.y  <= (frog_y+32) ):
                frog_s = 1
            if ( 2*car.y  <= (frog_y+32) ):
                frog_s2 = 1
    # Frog is somewhere in the river
    else:

        # If there isn't a river object, then there is water
        frog_n = 3
        frog_s = 3
        frog_e = 3
        frog_w = 3
        frog_n2 = 3
        frog_s2 = 3
        frog_e2 = 3
        frog_w2 = 3

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

            # Check frog_n
            if ( 2*(riverob.y + riverob.h) >= frog_y ):
                frog_n2 = 2
            # Check frog_s
            if ( 2*riverob.y  <= (frog_y+32) ):
                frog_s2 = 2
            # Check frog_e
            if ( 2*(riverob.x + riverob.w) >= frog_x ):
                frog_e2 = 2
            # Check frog_w
            if ( 2*riverob.x  <= (frog_x+32) ):
                frog_w2 = 2

        # Check if there is a home in front of frog
        for home in obs['homeR']:
            # Only need to check frog_n
            if ( (home.y + home.h) >= frog_y ):
                frog_n = 4
            if ( 2*(home.y + home.h) >= frog_y ):
                frog_n2 = 4

    return State2(frog_n,frog_n2,frog_s,frog_s2,frog_e,frog_e2,frog_w,frog_w2)

def obsToState3(obs):
    # possible values for f#
    #  -1 = beyond edge
    #   0 = road
    #   1 = car
    #   2 = turtle/log 
    #   3 = water
    #   4 = home

    frog_x = obs['frog_x']
    frog_y = obs['frog_y']

    # init all values to 0
    f = np.zeros(25)

    # Check every rectangle within 5x5 of frog 
    # Start with f0 (top left)
    left = frog_x - 64
    top = frog_y - 64
    w = h = 32
    temp = Rect(left,top,w,h)

    # Check if frog is near water set in front to water 
    if ( frog_y <= 293):
        # initialize f0-f4 to waters
        f[0] = f[1] = f[2] = f[3] = f[4] = 3
    if ( frog_y <= 261 ):
        # initialize f5-f9 to waters
        f[5] = f[6] = f[7] = f[8] = f[9] = 3
    # If frog in river, set behind to water
    if ( frog_y <= 197 ):
        # set f15-19 to waters
        f[15] = f[16] = f[17] = f[18] = f[19] = 3
    if ( frog_y <= 165 ):
        # set f20-24 to waters
        f[20] = f[21] = f[22] = f[23] = f[24] = 3


    for i in range(25):
        
        # Frog pos --> Skip this position
        if ( i == 12 ):
            # update left accordingly
            left = left + 32
            temp = Rect(left,top,w,h)
            continue

        # All other squares
        # Check edges
        if ( top < 0 or top > 517 or left < 0 or left > 448):
            f[i] = -1 

        # Check if state reaches homes
        if ( frog_y < kPlayYHomeLimit+64 ):
            collideInd = temp.collidelist(obs['homeR'])
            if ( collideInd != -1 ):
                # Theres a home in sight of frog
                # If home is not occupied, set square to home, else, set to water
                if ( obs['homes'][collideInd] == 0 ):
                    f[i] = 4
                else:
                    f[i] = 3

        # Check if state reaches river
        if ( frog_y < kPlayYRiverLimit+64 ):
            collideInd = temp.collidelist(obs['rivers'])
            if ( collideInd != -1 ):
                # Theres a log/turtle in sight of frog
                f[i] = 2

        # Check cars
        collideInd = temp.collidelist(obs['cars'])
        if ( collideInd != -1 ):
            # Theres a car in sight of frog
            f[i] = 1

        # Update X/Y
        # Reset X and Y if gone too far
        if ( i == 4 or i == 9 or i == 14 or i == 19 ):
            left = frog_x - 64
            # Increment y
            top = top + 32
        else:
            left = left + 32
        
        # recalculate temp
        temp = Rect(left,top,w,h)
        
    return State3(f[0],f[1],f[2],f[3],f[4],f[5],f[6],f[7],f[8],f[9],f[10],f[11], \
                  f[13],f[14],f[15],f[16],f[17],f[18],f[19],f[20],f[21],f[22],f[23],f[24])

def readConfigFile(config_filename):
    # Open, read in, and close it config file.
    open_configuration = open(config_filename, 'rb')
    Q_TABLE = pickle.load(open_configuration)

    return Q_TABLE

def writeConfigFile(config_filename):
    # Open, write out Q-table, and close it config file.
    open_configuration = open(config_filename, 'wb')
    pickle.dump(Q_TABLE, open_configuration)
    open_configuration.close()

# Initial start of game flag from command line
#   if command line argument = 'start', then it's the very beginning of the  game (first time running), training from scratch
#   if command line argument = 'continue', then it's some iteration of the game other than the first, training from previously calculated Q-table
cmd_arg = sys.argv[1]

if ( cmd_arg == "start" ):
    start_of_game = 1
elif ( cmd_arg == "continue" ):
    start_of_game = 0
else:
    print "Please input 'start' to begin training from scratch and 'continue' to use a config file."
    exit()

game = frogger_new.Frogger()
fps = 30
p = PLE(game, fps=fps,force_fps=False)
agent = NaiveAgent(p.getActionSet())
reward = 0.0

# PARAMATERS
###################
DISCOUNT = 0.9
ALPHA = 0.2
EXPLORATION_FACTOR = 0.4
###################

# Available actions to agent
AVAILABLE_ACTIONS = [K_w, K_s, K_a, K_d, K_F15]

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
    start_state = State3(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
  
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

    #print reward
    
    next_obs = game.getGameState()
    next_state = obsToState3(next_obs)
    reg_state = obsToState3(state)

    
    # If next_state is not in Q-table, add it
    if ( next_state not in Q_TABLE.keys() ):
        Q_TABLE[next_state] = np.zeros(NUM_ACTIONS)

    # Update curr Q in Q-table
    currQ = Q_TABLE[reg_state][action]
    Q_sample = reward +  DISCOUNT * np.max(Q_TABLE[next_state]) 
    Q_TABLE[reg_state][action] = currQ + (ALPHA * (Q_sample - currQ))

    state = next_obs


    # print game.score

