import random
import logging


def dice():
    roll = random.randint(1, 6)
    logging.debug("1d6=%s", roll)
    return roll
