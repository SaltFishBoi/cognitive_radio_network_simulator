import base_station
import customer_premise_equipment
import transmission
import algorithm


def main():

    base_station.function()
    base_station.function2()
    customer_premise_equipment.function()
    transmission.function()
    algorithm.function()

    print(transmission.get_random_drop())

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

