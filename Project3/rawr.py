import sys
import numpy as np
import pickle

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


Q_TABLE = dict()
start_state = State(666, 666, 0, 0, 0, 0 )  
start_state2 = State(444, 444, 1, 1, 1, 1 )  
Q_TABLE[start_state] = np.zeros(5)
Q_TABLE[start_state2] = np.ones(5)


# writeConfigFile("RAWR.config")

Q_2 = readConfigFile("FROG.config")

print Q_2.values()

#print Q_TABLE[start_state2]
#print Q_2[start_state2]


