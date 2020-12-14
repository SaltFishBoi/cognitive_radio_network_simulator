from algorithm import *
from transmission import *
from customer_premise_equipment import *
import threading
import time


# Macro/Defines
# for states and global variables

# state constants
IDLE = 0
REQUEST = 1
RESPONSE = 2
SEND = 3
RECEIVE = 4

# responses
ACK = 1
NACK = 0

BS_TIMEOUT = 10

# default
COUNTER_DEFAULT = 1
STATE_DEFAULT = IDLE
ID_DEFAULT = 1


# BS class
class BS:
    def __init__(self, identifier, state=STATE_DEFAULT):
        self.identifier = identifier
        self.state = state

    def get_identifier(self):
        return self.identifier

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state


# These are the functions involve with the base_station


def function():
    print("this is a base station function")
    return 0


def bs_status(bs):
    if type(bs) != bs:
        print("This is not a BS")
        return -1

    print("BS status:" +
          "\n  id: " + str(bs.identifier) +
          "\n  state: " + str(bs.state))

    return 1


def bs_initialization():
    # TODO
    bs = BS(ID_DEFAULT)
    print("Base station initialized.")
    return bs


# modify empty list lt by appending channel id with free state
def bs_sense(env, lt):
    # TODO
    if type(env) != ENV:
        print("This is not a ENV")
        return -1
    if (type(lt) != list) | (lt.length() != 0):
        print("This is not a empty list")
        return -1

    for ch in range(NUM_CH_DEFAULT):
        if env.get_ch_state(ch) == FREE:
            lt = lt + env.get_ch_identifier(ch)

    return 1


# make a request phrase to a CR device
def bs_request(env, source, target, ch):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("Source and target are not CPE")
        return -1

    send(env, source, target, REQUEST, ch, RESERVED_CH)
    return 1


# make a response phrase to a CR device
def bs_response(env, source, target, ch):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("Source and target are not CPE")
        return -1

    send(env, source, target, RESPONSE, ch, RESERVED_CH)

    return 1


def bs_send(env, source, target, ch):
    # TODO

    return 1


def bs_receive(en, source, target, ch):
    # TODO

    return 1


# pure send message at any channel to CR devices
def send(env, source, target, command, payload, ch):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("Source and target are not CPE")
        return -1

    msg_send = encode(source, target, command, payload)
    env.set_ch_message(ch, msg_send)

    return 1


# pure receive message at a channel
def receive(env, ch):
    # TODO
    if type(env) != ENV:
        print("This is not a ENV")
        return -1

    msg_receive = env.get_ch_message(ch)

    return decode(msg_receive)



