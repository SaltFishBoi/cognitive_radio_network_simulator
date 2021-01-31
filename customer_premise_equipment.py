from transmission import *
from multiprocessing import Process, Value
import time
# These are the functions involve with the customer_premise_equipment or AP (Access points for BS)

# task 1/9 need to double check the state, can't be at request all time. Need to come out to listen

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

CPE_TIMEOUT = 10
TIMER_DEFAULT = 0
TIME_OUT = 1
RECEIVE_TIME_INTERVAL = 0.25

# default
COUNTER_DEFAULT = 1
STATE_DEFAULT = IDLE
SIGNAL_STRENGTH_DEFAULT = 1
PRIVILEGE_DEFAULT = 0
NUM_CPE_DEFAULT = 7

# message constant
SEND_MESSAGE = [1, 2, 3, 4, 5, 6]

INTERRUPT_FLAG = 0


# CPE class
class CPE:
    def __init__(self, identifier,
                 state=STATE_DEFAULT,
                 signal_strength=SIGNAL_STRENGTH_DEFAULT,
                 channel=RESERVED_CH,
                 target=None):

        self.identifier = identifier
        self.state = state
        self.signal_strength = signal_strength
        self.channel = channel
        self.target = target

    def get_identifier(self):
        return self.identifier

    def get_state(self):
        return self.state

    def get_signal_strength(self):
        return self.signal_strength

    def get_channel(self):
        return self.channel

    def set_state(self, new_state):
        self.state = new_state

    def set_signal_strength(self, new_signal_strength):
        self.signal_strength = new_signal_strength

    def set_channel(self, new_channel):
        self.channel = new_channel

    def get_target(self):
        return self.target

    def set_target(self, new_target):
        self.target = new_target


class ACTION:
    def __init__(self, target,
                 delay):
        self.target = target
        self.delay = delay

    def get_target(self):
        return self.target

    def get_delay(self):
        return self.delay

    def set_delay(self, new_delay):
        self.delay = new_delay


# actions is construct of list of actions to be execute after certain amount of delay


def function():
    print("this is a customer premise equipment function")
    return 0


def cpe_process(env, source_num, device_list, actions):
    # TODO
    device = device_list[source_num]
    device.set_state(IDLE)
    i = 0

    print("how")
    #print(env.get_channels()[RESERVED_CH])
    #print(str(env.get_ch_message(RESERVED_CH)))

    while INTERRUPT_FLAG == 0:
        if device.get_state() == CR_REQUEST:
            delay = actions[i].get_delay()
            # clear out delay
            actions[i].set_delay(0)
            cpe_request(env, device, actions[i].get_target(), delay)
            print(str(device.get_identifier()) + " done " + str(device.get_state()))
        elif device.get_state() == CR_SEND:
            print("SEND SEND SEND")
            cpe_send(env, device, actions[i].get_target(), device.get_channel(), SEND_MESSAGE)
        elif device.get_state() == CR_RECEIVE:
            m = cpe_receive(env, device, device.get_target(), device.get_channel())
            # print(m)
        # IDLE state
        elif device.get_state() == DONE:
            cpe_done(device)
            i = i + 1
        else:
            if i < len(actions):
                device.set_state(CR_REQUEST)

    return 0


def cpe_status(cpe):

    print("CPE status:" +
          "\n  id: " + str(cpe.identifier) +
          "\n  state: " + str(cpe.state) +
          "\n  signal_strength: " + str(cpe.signal_strength) +
          "\n  channel: " + str(cpe.channel) +
          "\n  timer: " + str(cpe.timer))

    return 1


# Timer expire
def cpe_timer_handler(timer, delay):
    timer.value = TIMER_DEFAULT
    time.sleep(delay)
    timer.value = TIME_OUT
    return 0


# make a request phrase to a CR device through BS
# request with unknown ch, let BS decide
def cpe_request(env, source, target, delay):
    print("cpe " + str(source.get_identifier()) + " requesting " + str(target))

    timer = Value('i', TIMER_DEFAULT)
    d = Process(target=cpe_timer_handler, args=(timer, delay))
    d.start()
    # setup time before the time out.
    # loop through these while source's timer times up

    while timer.value != TIME_OUT:
        # extract msg from the air
        msg = receive(env, RESERVED_CH)
        print(str(source.get_identifier()), msg[:])
        # this won't raise a death lock because only one request BS is processing.
        # in this case, BS picked up other CPE's request.
        if (msg[1] == source.get_identifier()) and (msg[2] == BS_REQUEST):
            cpe_response(env, source, msg[0], msg[3])
            print("get a request from bs and cpe")
            source.set_state(CR_RECEIVE)
            source.set_channel(msg[3])

            # end the timer
            timer.value = TIME_OUT
            d.terminate()
            d.join()

        time.sleep(RECEIVE_TIME_INTERVAL)
    #d.join()

    # start to send out the request
    # if the source still active and receive not response from other device, it keeps sending request
    while source.get_state() == CR_REQUEST:
        print("hi")
        # send request
        # channel is 0 because it doesn't know what channel to be selected yet
        send(env, source.get_identifier(), target, CR_REQUEST, 0, RESERVED_CH)

        # start timer
        timer.value = TIMER_DEFAULT
        t = Process(target=cpe_timer_handler, args=(timer, CPE_TIMEOUT))
        t.start()

        # loop through these while source's timer times up
        while timer.value != TIME_OUT:
            #print("cpe loop")
            # extract msg from the air
            msg = receive(env, RESERVED_CH)
            print(str(source.get_identifier()), msg[:])
            # match the message expected
            if (msg[0] == target) and (msg[1] == source.get_identifier()) and (msg[2] == BS_RESPONSE):
                source.set_state(CR_SEND)
                # selected channel is in the msg[3]
                source.set_channel(msg[3])
                # need to set it to time out to get out of this loop

                # end the timer
                print("PRE SEND SEND SEND")
                print(str(source.get_identifier()) + " done " + str(source.get_state()))
                timer.value = TIME_OUT
                t.terminate()
                t.join()
                print("PRE SEND...")

            # this won't raise a death lock because only one request BS is processing.
            # in this case, BS picked up other CPE's request.
            elif (msg[1] == source.get_identifier()) and (msg[2] == BS_REQUEST):
                cpe_response(env, source, msg[0], msg[3])
                # source.set_state(CR_RECEIVE)
                # source.set_channel(msg[3])

                # need to set it to time out to get out of this loop
                # end the timer
                timer.value = TIME_OUT
                t.terminate()
                t.join()
                print("PRE RECEIVE RECEIVE")

            time.sleep(RECEIVE_TIME_INTERVAL)
    return 1


# make a response phrase to a CR device through BS
# receiver side never set a timer (either on setup or communication)
def cpe_response(env, source, target, ch):
    print("cpe " + str(source.get_identifier()) + " responding " + str(target))

    send(env, source.get_identifier(), target, CR_RESPONSE, ch, RESERVED_CH)
    source.set_state(CR_RECEIVE)
    source.set_target(target)
    source.set_channel(ch)

    return 1


# timer thread is require
def cpe_send(env, source, target, ch, message):
    print("cpe " + str(source.get_identifier()) + " sending to " + str(target))

    index = 0

    # if the source still active and receive not response from other device, it keeps sending request
    while source.get_state() == CR_SEND:
        # send request
        print("send loop")
        if index == len(message):
            send(env, source.get_identifier(), target, CR_SEND, 0, ch)
        else:
            send(env, source.get_identifier(), target, CR_SEND, message[index], ch)

        # start timer
        timer = Value('i', TIMER_DEFAULT)
        t = Process(target=cpe_timer_handler, args=(timer, CPE_TIMEOUT))
        t.start()

        # loop through these while source's timer times up
        while timer.value != TIME_OUT:
            # extract msg from the air
            msg = receive(env, ch)

            # if the channel is occupied by LBU
            if get_ch_state(env, ch) == BUSY:
                source.set_state(CR_REQUEST)
                # send next character
                index = index + 1
                # end the timer
                timer.value = TIME_OUT
                t.terminate()
                t.join()

            # match the message expected
            elif (msg[0] == target) and (msg[1] == source) and (msg[2] == CR_RECEIVE) and (msg[3] == ACK):
                # need to set it to time out to get out of this loop

                # send next character
                index = index + 1

                # end the timer
                timer.value = TIME_OUT
                t.terminate()
                t.join()

            time.sleep(RECEIVE_TIME_INTERVAL)

        if index > len(message):
            source.set_state(DONE)
        elif index == 0:
            source.set_state(CR_REQUEST)

    return 1


def cpe_receive(env, source, target, ch):
    print("cpe " + str(source.get_identifier()) + " receiving from " + str(target))

    message = []

    # if the source still active and receive not response from other device, it keeps sending request
    while source.get_state() == CR_RECEIVE:
        # check for valid receive message

        msg = receive(env, ch)
        # check end of the message
        if (msg[0] == target) and (msg[1] == source) and (msg[2] == CR_SEND) and (msg[3] == 0):
            source.set_state(IDLE)
            print(msg)

        message.append(msg)

        # send ACK for receive knowledge
        send(env, source.get_identifier(), target, CR_RECEIVE, ACK, ch)

        # extract msg from the air in the reserved channel, see for any interruption
        msg = receive(env, RESERVED_CH)
        # match the message expected
        if (msg[0] == target) and (msg[1] == source) and (msg[2] == CR_REQUEST) and (msg[3] == ACK):
            source.set_state(CR_RESPONSE)

        time.sleep(RECEIVE_TIME_INTERVAL)

    return 1


# probably no need
def cpe_idle(env, source, target):
    # TODO

    return 1


def cpe_done(source):

    source.set_state(IDLE)
    return 1