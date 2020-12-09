# These are the functions involve with the transmission

from random import seed
from random import random

# constant
SEED = 1


def function():
    print("this is a transmission function")
    return 0


def get_random_drop(s):
    # TODO
    seed(s)
    r = random()
    return r
