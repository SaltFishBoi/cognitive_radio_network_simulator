from algorithm import *
from transmission import *
from customer_premise_equipment import *
import threading
import time


# Macro/Defines
# for states and global variables

# state constants
IDLE = 0
CR_REQUEST = 1
CR_RESPONSE = 2
CR_SEND = 3
CR_RECEIVE = 4
DONE = 5
BS_REQUEST = 6
BS_RESPONSE = 7

# responses
ACK = 1
NACK = 0

BS_TIMEOUT = 3

# default
COUNTER_DEFAULT = 1
STATE_DEFAULT = IDLE
ID_DEFAULT = 1


# BS class
class BS:
    def __init__(self, identifier, client_list=None, state=STATE_DEFAULT):
        self.identifier = identifier
        self.client_list = client_list
        self.state = state

    def get_identifier(self):
        return self.identifier

    def get_client_list(self):
        return self.client_list

    def set_client_list(self, client_id, ch):
        self.client_list[client_id].set_channel(ch)

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state


# These are the functions involve with the base_station


def function():
    print("this is a base station function")
    return 0


def bs_process(env, station):
    # TODO
    station.set_state(IDLE)
    m = receive(env, RESERVED_CH)
    ch = 0

    #print("what")
    #print(env[:])
    #print(env.get_channels()[RESERVED_CH])
    #print(str(env.get_ch_message(RESERVED_CH)))

    while INTERRUPT_FLAG == 0:
        if station.get_state() == BS_REQUEST:
            #print("pre-assign ch " + str(ch))
            bs_request(env, m[0], m[1], station, ch)
        else:
            m = receive(env, RESERVED_CH)
            time.sleep(0.5)
            if m[2] == CR_REQUEST:
                station.set_state(BS_REQUEST)
                ch = select_channel(env, station)

    return 0


def bs_status(bs):

    print("BS status:" +
          "\n  id: " + str(bs.identifier) +
          "\n  state: " + str(bs.state))

    return 1


# Timer expire
def bs_timer_handler(timer, delay):
    timer.value = TIMER_DEFAULT
    time.sleep(delay)
    timer.value = TIME_OUT
    return 0


def bs_initialization():
    bs = BS(ID_DEFAULT)
    print("Base station initialized.")
    return bs


# modify empty list lt by appending channel id with free state
def bs_sense(env, lt):

    for ch in range(NUM_CH_DEFAULT):
        if env.get_ch_state(ch) == FREE:
            lt = lt + env.get_ch_identifier(ch)

    return 1


# make a request phrase to a CR device
def bs_request(env, source, target, station, ch):
    print("BS repeat CPE " + str(source) + " -> " + str(target) + " request begins")

    # if the source still active and receive not response from other device, it keeps sending request
    while station.get_state() == BS_REQUEST:
        # send request
        print("BS assign ch " + str(ch))
        send(env, source, target, BS_REQUEST, ch, RESERVED_CH)
        print("BS repeat CPE " + str(source) + " -> " + str(target) + " request sends")
        time.sleep(TIME_INTERVAL)

        # start timer

        timer = Value('i', TIMER_DEFAULT)
        t = Process(target=bs_timer_handler, args=(timer, BS_TIMEOUT))
        t.start()

        # loop through these while source's timer times up
        while timer.value != TIME_OUT:

            # extract msg from the air
            msg = receive(env, RESERVED_CH)
            time.sleep(TIME_INTERVAL)
            # match the message expected
            if (msg[0] == target) and (msg[1] == source) and (msg[2] == CR_RESPONSE):
                bs_response(env, source, target, station, ch)
                print("BS update client list")

                # selected channel is in the msg[3]
                # source.set_channel(msg[3])
                # need to record the CR device channel here
                station.set_client_list(source, ch)
                station.set_client_list(target, ch)

                # environment update
                set_ch_state(env, ch, LEASE)


                # need to set it to time out to get out of this loop
                # end the timer
                timer.value = TIME_OUT
                t.terminate()
                t.join()

    return 1


# make a response phrase to a CR device
def bs_response(env, source, target, station, ch):
    print("BS repeat CPE " + str(source) + " <- " + str(target) + " respond begins")

    send(env, target, source, BS_RESPONSE, ch, RESERVED_CH)
    print("BS repeat CPE " + str(source) + " -> " + str(target) + " request sends")
    time.sleep(TIME_INTERVAL)
    station.set_state(IDLE)

    return 1


# probably no need
def bs_idle(env, source, target):
    # TODO

    return 1