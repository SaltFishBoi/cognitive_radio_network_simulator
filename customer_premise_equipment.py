# These are the functions involve with the customer_premise_equipment

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
SIGNAL_STRENGTH_DEFAULT = 1
PRIVILEGE_DEFAULT = 0


# CPE class
class CPE:
    def __init__(self, identifier,
                 state=STATE_DEFAULT,
                 signal_strength=SIGNAL_STRENGTH_DEFAULT,
                 privilege=PRIVILEGE_DEFAULT,
                 counter=COUNTER_DEFAULT):
        self.identifier = identifier
        self.state = state
        self.signal_strength = signal_strength
        self.privilege = privilege
        self.counter = counter

    def get_identifier(self):
        return self.identifier

    def get_state(self):
        return self.state

    def get_signal_strength(self):
        return self.signal_strength

    def get_privilege(self):
        return self.privilege

    def get_counter(self):
        return self.counter

    def set_state(self, new_state):
        self.state = new_state

    def set_signal_strength(self, new_signal_strength):
        self.signal_strength = new_signal_strength

    def set_privilege(self, new_privilege):
        self.privilege = new_privilege

    def increment_counter(self):
        if self.counter == TIMEOUT:
            self.counter = 1
        else:
            self.counter += 1


def function():
    print("this is a customer premise equipment function")
    return 0


def cpe_status(cpe):
    if type(cpe) != CPE:
        print("This is not a CPE")
        return 0

    print("CPE status:" +
          "\n  id: " + str(cpe.identifier) +
          "\n  state: " + str(cpe.state) +
          "\n  signal_strength: " + str(cpe.signal_strength) +
          "\n  privilege: " + str(cpe.privilege) +
          "\n  counter: " + str(cpe.counter))

    return 1


def cpe_request(source, target):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("This is not a CPE")
        return 0

    return 1


def cpe_response(source, target):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("This is not a CPE")
        return 0

    return 1


def cpe_send(source, target):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("This is not a CPE")
        return 0

    return 1


def cpe_receive(source, target):
    # TODO
    if (type(source) != CPE) | (type(target) != CPE):
        print("This is not a CPE")
        return 0

    return 1



