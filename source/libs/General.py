
import numpy as np
import pandas as pd
import time



def timer(func):
    def f(*args, **kwargs):
        before = time.time()
        rv = func(*args, **kwargs)
        after = time.time()
        print('elapsed', after - before)
        return rv
    return f


