import time
import random

from utils.logger import logger
from utils.constants import Status

def initial_delay(sleep_from: int, sleep_to: int):
    delay_secs = random.randint(sleep_from, sleep_to)
    logger.log(Status.DELAY, f"- waiting for {delay_secs} to start wallet activities")
    time.sleep(delay_secs)

def sleep(sleep_from: int, sleep_to: int):
    delay_secs = random.randint(sleep_from, sleep_to)
    logger.log(Status.DELAY, f"- waiting for {delay_secs}")
    time.sleep(delay_secs)