# These are the functions involve with the transmission

from random import seed
from random import random

# constant
SEED = 1

# channel status
FREE = 0
BUSY = 1

# initial
NUM_CH_DEFAULT = 11


# CH class
class CH:
    def __init__(self, identifier, state=FREE):
        self.identifier = identifier
        self.state = state

    def get_identifier(self):
        return self.identifier

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state


# ENV class
# information about the air
class ENV:
    def __init__(self, channels=None, num_channel=NUM_CH_DEFAULT):
        self.channels = channels
        self.num_channel = num_channel

    def get_channels(self):
        return self.channels

    def get_num_channel(self):
        return self.num_channel


def function():
    print("this is a transmission function")
    return 0


# rate from 0.0 - 1.0
def get_random_drop(rate):
    # TODO
    seed(SEED)
    r = random()

    if r < rate:
        return 1
    else:
        return 0


def e_initialization(env):
    env.channels = []
    for c in range(env.num_channel):
        env.channels.append(CH(c))


def e_report(env):
    if type(env) != ENV:
        print("This is not a ENV")
        return 0

    for ch in env.channels:
        ch_status(ch)

    return 1


def ch_status(ch):
    if type(ch) != CH:
        print("This is not a CH")
        return 0

    print("CH status:" +
          "\n  id: " + str(ch.identifier) +
          "\n  state: " + str(ch.state))

    return 1


