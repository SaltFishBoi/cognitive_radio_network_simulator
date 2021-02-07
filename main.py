from base_station import *
from customer_premise_equipment import *
from licensed_band_user import *
from transmission import *
from algorithm import *
from multiprocessing import Process


def main():

    # initialize environment channel list
    share_env1 = create_environment()

    # initialize license band user list
    lbu_list1 = []
    for i in range(NUM_LBU_DEFAULT):
        lbu = LBU(i, STATE_DEFAULT, i)
        lbu_list1.append(lbu)

    lbu_in_used(share_env1, lbu_list1[3])
    lbu_in_used(share_env1, lbu_list1[6])

    print(share_env1[:])

    # initialize base station
    bs = BS(0)

    # CPE action list
    # actions list (EDITABLE)
    # (delay, target)
    action_list = [[ACTION(1, 1, 10), ACTION(1, 2, 10), ACTION(1, 3, 10), ACTION(1, 4, 10), ACTION(1, 5, 10)],
                   [ACTION(2, 3, 10), ACTION(2, 2, 10), ACTION(2, 1, 10), ACTION(2, 2, 10), ACTION(2, 1, 10)],
                   [ACTION(3, 60, 10), ACTION(3, 1, 10), ACTION(3, 3, 10), ACTION(3, 4, 10), ACTION(3, 5, 10)],
                   [ACTION(4, 60, 10), ACTION(4, 5, 10), ACTION(4, 4, 10), ACTION(4, 2, 10), ACTION(4, 1, 10)],
                   [ACTION(5, 60, 10), ACTION(5, 5, 10), ACTION(5, 1, 10), ACTION(5, 1, 10), ACTION(5, 1, 10)],
                   [ACTION(6, 60, 10), ACTION(6, 6, 10), ACTION(6, 6, 10), ACTION(6, 6, 10), ACTION(6, 6, 10)],
                   [ACTION(7, 60, 10), ACTION(7, 5, 10), ACTION(7, 5, 10), ACTION(7, 5, 10), ACTION(7, 5, 10)]]

    print("Program Starts")

    # launch multiprocess for CPE
    b = Process(target=bs_process, args=(share_env1, bs))
    b.start()
    proc = []
    for i in range(NUM_CPE_DEFAULT):
        device = CPE(i)
        p = Process(target=cpe_process, args=(share_env1, i, device, action_list[i]))
        p.start()
        proc.append(p)

    print("Program runs")
    print(share_env1[:])

    # recycle all processes
    for p in proc:
        p.join()
    b.join()
    print("Program ends")

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

