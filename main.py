from base_station import *
from customer_premise_equipment import *
from licensed_band_user import *
from transmission import *
from algorithm import *
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager


def main():

    # initialize channel list
    channel_list1 = []
    for i in range(NUM_CH_DEFAULT):
        channel = CH(i)
        channel_list1.append(channel)
    # initialize environment
    env1 = ENV(channel_list1)

    # initialize license band user list
    lbu_list1 = []
    for i in range(NUM_LBU_DEFAULT):
        lbu = LBU(i, STATE_DEFAULT, i)
        lbu_list1.append(lbu)

    lbu_in_used(env1, lbu_list1[3])
    lbu_in_used(env1, lbu_list1[6])

    #for lbu in lbu_list1:
    #    lbu_status(lbu)

    #e_report(env1)

    # initialize customer premise equipment
    cpe_list1 = []
    for i in range(NUM_CPE_DEFAULT):
        cpe = CPE(i)
        cpe_list1.append(cpe)

    # initialize base station
    bs = BS(0, cpe_list1)

    # CPE action list
    # actions list (EDITABLE)
    # (delay, target)
    action_list = [[ACTION(1, 1), ACTION(1, 1), ACTION(1, 1), ACTION(1, 1), ACTION(1, 1), ACTION(1, 1)],
                   [ACTION(2, 0), ACTION(2, 2), ACTION(2, 0), ACTION(2, 2), ACTION(2, 0), ACTION(2, 2)],
                   [ACTION(3, 0), ACTION(3, 1), ACTION(3, 3), ACTION(3, 4), ACTION(3, 5), ACTION(3, 6)],
                   [ACTION(4, 6), ACTION(4, 5), ACTION(4, 4), ACTION(4, 2), ACTION(4, 1), ACTION(4, 0)],
                   [ACTION(5, 5), ACTION(5, 5), ACTION(5, 1), ACTION(5, 1), ACTION(5, 0), ACTION(5, 0)],
                   [ACTION(6, 6), ACTION(6, 6), ACTION(6, 6), ACTION(6, 6), ACTION(6, 6), ACTION(6, 6)],
                   [ACTION(7, 5), ACTION(7, 5), ACTION(7, 5), ACTION(7, 5), ACTION(7, 5), ACTION(7, 5)]]

    print("starting")

    # launch multiprocess for CPE
    BaseManager.register('ENV', ENV)
    manager = BaseManager()
    manager.start()
    inst = manager.ENV()

    # sharable_bs = Value('bs', bs)
    b = Process(target=bs_process, args=(inst, bs))
    b.start()
    proc = []
    for i in range(1):
        p = Process(target=cpe_process, args=(inst, i, cpe_list1, action_list[i]))
        p.start()
        proc.append(p)

    print("running")
    print(inst)
    #print(inst.get_channels()[RESERVED_CH])
    #print(str(inst.get_ch_message(RESERVED_CH)))

    # recycle all processes
    for p in proc:
        p.join()
    b.join()
    print("ending")

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

