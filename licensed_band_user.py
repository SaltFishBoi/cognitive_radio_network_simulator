from transmission import *
# These are the functions involve with the customer_premise_equipment

# state constants
IDLE = 0
IN_USED = 1

# default
STATE_DEFAULT = IDLE
BAND_DEFAULT = 0
SIGNAL_STRENGTH_DEFAULT = 1
PRIVILEGE_DEFAULT = 0
NUM_LBU_DEFAULT = 11

TIME_DIVISION = 24

INTERRUPT_FLAG = 0


# LBU class
class LBU:
    def __init__(self, identifier,
                 state=STATE_DEFAULT,
                 band=BAND_DEFAULT,
                 signal_strength=SIGNAL_STRENGTH_DEFAULT,
                 privilege=PRIVILEGE_DEFAULT):
        self.identifier = identifier
        self.band = band
        self.state = state
        self.signal_strength = signal_strength
        self.privilege = privilege

    def get_identifier(self):
        return self.identifier

    def get_state(self):
        return self.state

    def get_band(self):
        return self.band

    def get_signal_strength(self):
        return self.signal_strength

    def get_privilege(self):
        return self.privilege

    def set_state(self, new_state):
        self.state = new_state

    def set_signal_strength(self, new_signal_strength):
        self.signal_strength = new_signal_strength

    def set_privilege(self, new_privilege):
        self.privilege = new_privilege


def function():
    print("this is a licensed band user function")
    return 0


def lbu_process(env, source_num, device, schedule):
    device.set_state(IDLE)
    start_time = time.time()

    print("LBU " + str(source_num) + " process begins")

    while INTERRUPT_FLAG == 0:
        if device.get_state() == IN_USED:
            lbu_in_used(env, device)
            print("LBU " + str(source_num) + " uses channel " + str(device.get_band()))
            time.sleep(60)
            lbu_not_in_used(env, device)
            print("LBU " + str(source_num) + " leaves channel " + str(device.get_band()))
        else:
            time_div = (int(time.time() - start_time)//60) % TIME_DIVISION
            if time_div in schedule:
                device.set_state(IN_USED)

        time.sleep(1)
    return 0


def lbu_status(lbu):
    if type(lbu) != LBU:
        print("This is not a LBU")
        return -1

    print("LBU status:" +
          "\n  id: " + str(lbu.identifier) +
          "\n  licensed band: " + str(lbu.band) +
          "\n  state: ", end='')
    if lbu.state == IDLE:
        print("IDLE", end='')
    else:
        print("IN_USED", end='')

    print("\n  signal_strength: " + str(lbu.signal_strength) +
          "\n  privilege: " + str(lbu.privilege))

    return 1


def lbu_in_used(env, source):
    if type(source) != LBU:
        print("This is not a LBU")
        return -1

    source.set_state(IN_USED)
    set_ch_state(env, source.get_band(), BUSY)

    return 1


def lbu_not_in_used(env, source):
    if type(source) != LBU:
        print("This is not a LBU")
        return -1

    source.set_state(IDLE)
    set_ch_state(env, source.get_band(), FREE)

    return 1



