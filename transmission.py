# These are the functions involve with the transmission

from random import seed
from random import random

# constant
SEED = 1
RESERVED_CH = 0

# channel status
FREE = 0
BUSY = 1

# initial
NUM_CH_DEFAULT = 11
SOURCE_MAX_LENGTH = 0b1111
TARGET_MAX_LENGTH = 0b1111
COMMAND_MAX_LENGTH = 0b1111
PAYLOAD_MAX_LENGTH = 0b1111
MESSAGE_MAX_LENGTH = 0b1111111111111111


# CH class
class CH:
    def __init__(self, identifier, state=FREE, message=None):
        self.identifier = identifier
        self.state = state
        self.message = message

    def get_identifier(self):
        return self.identifier

    def get_state(self):
        return self.state

    def get_message(self):
        return self.message

    def set_state(self, new_state):
        self.state = new_state

    def set_message(self, new_message):
        self.message = new_message


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

    def get_ch_identifier(self, ch):
        return self.channels[ch].identifier

    def get_ch_message(self, ch):
        return self.channels[ch].message

    def get_ch_state(self, ch):
        return self.channels[ch].state

    def set_ch_state(self, ch, new_state):
        self.channels[ch].state = new_state

    def set_ch_message(self, ch, new_message):
        self.channels[ch].message = new_message


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
        return -1

    for ch in env.channels:
        ch_status(ch)

    return 1


def ch_status(ch):
    if type(ch) != CH:
        print("This is not a CH")
        return -1

    print("CH status:" +
          "\n  id: " + str(ch.identifier) +
          "\n  state: " + str(ch.state) +
          "\n message: " + str(ch.message))

    return 1


# 16 bits
# |   source    |   target  |  command   |  payload   |
# | 15 14 13 12 | 11 10 9 8 | 7  6  5  4 | 3  2  1  0 |

# encoding with simple protocol
def encode(source, target, command, payload):
    if ((source >= SOURCE_MAX_LENGTH) |
            (target >= TARGET_MAX_LENGTH) |
            (command >= COMMAND_MAX_LENGTH) |
            (payload >= PAYLOAD_MAX_LENGTH)):
        return -1

    msg = source*(2**13)+target*(2**9)+source*(2**5)+source

    return msg


# return a tuple of all the decoded info from message
def decode(message):
    if message >= MESSAGE_MAX_LENGTH:
        return -1

    source_masked = message & 0b1111000000000000
    target_masked = message & 0b111100000000
    command_masked = message & 0b11110000
    payload_masked = message & 0b1111

    return source_masked >> 12, target_masked >> 8, command_masked >> 4, payload_masked
