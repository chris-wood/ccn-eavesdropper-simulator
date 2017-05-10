import os
import random

def random_string(n):
    return os.urandom(n).encode("hex")

def random_range(l, h):
    return random.randint(l, h)

def random_flag(p = 0.5):
    val = random.random()
    if val <= p:
        return True
    else:
        return False
