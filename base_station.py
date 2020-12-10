import algorithm

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

TIMEOUT = 10

# default
COUNTER_DEFAULT = 1
STATE_DEFAULT = IDLE


# BS class
class BS:
    def __init__(self, identifier, state=STATE_DEFAULT, counter=COUNTER_DEFAULT):
        self.identifier = identifier
        self.state = state
        self.counter = counter

    def get_identifier(self):
        return self.identifier

    def get_state(self):
        return self.state

    def get_counter(self):
        return self.counter

    def set_state(self, new_state):
        self.state = new_state

    def increment_counter(self):
        if self.counter == TIMEOUT:
            self.counter = 1
        else:
            self.counter += 1

# These are the functions involve with the base_station


def function():
    print("this is a base station function")
    return 0


def function2():
    algorithm.function()
    return 0


def bs_status(bs):
    if type(bs) != bs:
        print("This is not a BS")
        return 0

    print("BS status:" +
          "\n  id: " + str(bs.identifier) +
          "\n  state: " + str(bs.state) +
          "\n  signal_strength: " + str(bs.signal_strength) +
          "\n  privilege: " + str(bs.privilege) +
          "\n  counter: " + str(bs.counter))

    return 1


def bs_initialization():
    # TODO
    return 1


def bs_sense(env):
    # TODO
    return 1



