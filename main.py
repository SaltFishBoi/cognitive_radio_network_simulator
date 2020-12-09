from base_station import *
from customer_premise_equipment import *
from licensed_band_user import *
from transmission import *
from algorithm import *


def main():

    # base_station.function()
    # base_station.function2()
    # customer_premise_equipment.function()
    # transmission.function()
    # algorithm.function()
    # print(transmission.get_random_drop(transmission.SEED))

    cpe1 = CPE(1, IDLE, 0.1, 1)
    lbu1 = LBU(2, IDLE, 0.2, 2)
    cpe_status(cpe1)
    lbu_status(lbu1)

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

