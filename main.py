from base_station import *
from customer_premise_equipment import *
from licensed_band_user import *
from transmission import *
from algorithm import *
from multiprocessing import Process
import time
#import sys

INTERRUPT_FLAG = 0


def main():

    # initialize environment channel list
    share_env1 = create_environment()

    # initialize base station
    bs = BS(0)

    # CPE action list
    # actions list (EDITABLE)
    # (delay, target)
    action_list = [[ACTION(1, 1, 10), ACTION(1, 11, 10)],
                   [ACTION(2, 2, 10), ACTION(2, 12, 10)],
                   [ACTION(3, 3, 10), ACTION(3, 13, 10)],
                   [ACTION(4, 4, 10), ACTION(4, 14, 10)],
                   [ACTION(5, 5, 10), ACTION(5, 15, 10)],
                   [ACTION(6, 6, 10), ACTION(6, 16, 10)],
                   [ACTION(1, 7, 10), ACTION(1, 17, 10)]]

    schedule_list = [[6, 6, 7, 8, 9],
                     [6, 6, 7, 8, 9],
                     [6, 6, 7, 8, 9],
                     [6, 6, 7, 8, 9],
                     [6, 6, 7, 8, 9],
                     [6, 6, 7, 8, 9],
                     [6, 6, 7, 8, 9],
                     [6, 6, 7, 8, 9],
                     [6, 6, 7, 8, 9],
                     [6, 6, 7, 8, 9],
                     [6, 6, 7, 8, 9]]

    print("Program Starts")

    # launch multiprocess

    t = Process(target=timing)
    t.start()

    b = Process(target=bs_process, args=(share_env1, bs))
    print("Program runs")
    cpe_proc = []
    lbu_proc = []
    b.start()

    # initialize and launch license band user list
    for i in range(1, NUM_LBU_DEFAULT+1):
        device = LBU(i, STATE_DEFAULT, i)
        l = Process(target=lbu_process, args=(share_env1, i, device, schedule_list[i-1]))
        l.start()
        lbu_proc.append(l)

    # initialize and launch customer premise equipment list
    for i in range(NUM_CPE_DEFAULT):
        device = CPE(i)
        c = Process(target=cpe_process, args=(share_env1, i, device, action_list[i]))
        c.start()
        cpe_proc.append(c)

    # recycle all processes
    for c in cpe_proc:
        c.join()

    for l in lbu_proc:
        l.join()

    b.join()
    t.join()
    print("Program ends")

    return 0


def timing():
    i = 0
    while True:
        print("    Time: ", i)
        time.sleep(1)
        i += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #stdoutOrigin = sys.stdout
    #sys.stdout = open("log.txt", "w")
    main()

