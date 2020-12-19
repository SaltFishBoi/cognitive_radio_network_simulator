from transmission import *
import threading
import time
# These are the functions involve with the customer_premise_equipment or AP (Access points for BS)

# state constants
IDLE = 0
REQUEST = 1
RESPONSE = 2
SEND = 3
RECEIVE = 4

# responses
ACK = 1
NACK = 0

CPE_TIMEOUT = 10
TIMER_DEFAULT = 0
TIME_OUT = 1
RECEIVE_TIME_INTERVAL = 1

# default
COUNTER_DEFAULT = 1
STATE_DEFAULT = IDLE
SIGNAL_STRENGTH_DEFAULT = 1
PRIVILEGE_DEFAULT = 0


# CPE class
class CPE:
    def __init__(self, identifier,
                 state=STATE_DEFAULT,
                 signal_strength=SIGNAL_STRENGTH_DEFAULT,
                 channel=RESERVED_CH,
                 timer=TIMER_DEFAULT):

        self.identifier = identifier
        self.state = state
        self.signal_strength = signal_strength
        self.channel = channel
        self.timer=timer

    def get_identifier(self):
        return self.identifier

    def get_state(self):
        return self.state

    def get_signal_strength(self):
        return self.signal_strength

    def get_channel(self):
        return self.channel

    def get_timer(self):
        return self.timer

    def set_state(self, new_state):
        self.state = new_state

    def set_signal_strength(self, new_signal_strength):
        self.signal_strength = new_signal_strength

    def set_channel(self, new_channel):
        self.channel = new_channel

    def set_timer(self, new_timer):
        self.timer = new_timer

def function():
    print("this is a customer premise equipment function")
    return 0


def cpe_status(cpe):
    if type(cpe) != CPE:
        print("This is not a CPE")
        return -1

    print("CPE status:" +
          "\n  id: " + str(cpe.identifier) +
          "\n  state: " + str(cpe.state) +
          "\n  signal_strength: " + str(cpe.signal_strength) +
          "\n  channel: " + str(cpe.channel) +
          "\n  timer: " + str(cpe.timer))

    return 1


# Timer expire
def cpe_timer_handler(cpe):
    cpe.set_timer(TIMER_DEFAULT)
    time.sleep(CPE_TIMEOUT)
    cpe.set_timer(TIME_OUT)
    return 0


# make a request phrase to a CR device through BS
def cpe_request(env, source, target, ch):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("Source and target are not CPE")
        return -1

    # if the source still active and receive not response from other device, it keeps sending request
    while source.get_state() == REQUEST:
        # send request
        send(env, source, target, REQUEST, ch, RESERVED_CH)
        # start timer
        t = threading.Thread(target=cpe_timer_handler, args=[source])
        t.start()

        # loop through these while source's timer times up
        while source.get_timer() != TIME_OUT:
            # extract msg from the air
            msg = receive(env, RESERVED_CH)
            # match the message expected
            if (msg[0] == target) and (msg[1] == source) and (msg[2] == RESPONSE) and (msg[3] == ACK):
                source.set_state(SEND)
                source.set_channel(ch)
                # need to set it to time out to get out of this loop
                source.set_timer(TIME_OUT)

                # end the timer
                t.join()

            time.sleep(RECEIVE_TIME_INTERVAL)

    return 1


# make a response phrase to a CR device through BS
# receiver side never set a timer (either on setup or communication)
def cpe_response(env, source, target, ch):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("Source and target are not CPE")
        return -1

    send(env, source, target, RESPONSE, ACK, RESERVED_CH)
    source.set_state(RECEIVE)
    source.set_channel(ch)

    return 1


# timer thread is require
def cpe_send(env, source, target, ch, message):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("Source and target are not CPE")
        return -1

    index = 0

    # if the source still active and receive not response from other device, it keeps sending request
    while source.get_state() == SEND:
        # send request
        send(env, source, target, REQUEST, message[index], ch)
        # start timer
        t = threading.Thread(target=cpe_timer_handler, args=[source])
        t.start()

        # loop through these while source's timer times up
        while source.get_timer() != TIME_OUT:
            # extract msg from the air
            msg = receive(env, ch)
            # match the message expected
            if (msg[0] == target) and (msg[1] == source) and (msg[2] == RECEIVE) and (msg[3] == ACK):
                # need to set it to time out to get out of this loop
                source.set_timer(TIME_OUT)

                # send next character
                index = index + 1

                # end the timer
                t.join()

            time.sleep(RECEIVE_TIME_INTERVAL)

        if index == len(message):
            source.set_state(IDLE)

    return 1


def cpe_receive(env, source, target, ch):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("Source and target are not CPE")
        return -1

    message = []

    # if the source still active and receive not response from other device, it keeps sending request
    while source.get_state() == RECEIVE:
        # check for valid receive message

        #
        msg = receive(env, ch)
        if (msg[0] == target) and (msg[1] == source) and (msg[2] == SEND) and (msg[3] == 0):
            source.set_state(IDLE)

        message.append(msg)

        # send ACK for receive knowledge
        send(env, source, target, RECEIVE, ACK, ch)

        # extract msg from the air in the reserved channel, see for any interruption
        msg = receive(env, RESERVED_CH)
        # match the message expected
        if (msg[0] == target) and (msg[1] == source) and (msg[2] == REQUEST) and (msg[3] == ACK):
            source.set_state(RESPONSE)

    return 1


def cpe_idle(env, source, target):
    # TODO

    return 1


# pure send message at any channel to CR devices through BS
def send(env, source, target, command, payload, ch):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("Source and target are not CPE")
        return -1

    msg_send = encode(source, target, command, payload)
    env.set_ch_message(ch, msg_send)

    return 1


# pure receive message at a channel through BS
def receive(env, ch):
    # TODO
    if type(env) != ENV:
        print("This is not a ENV")
        return -1

    msg_receive = env.get_ch_message(ch)

    return decode(msg_receive)




