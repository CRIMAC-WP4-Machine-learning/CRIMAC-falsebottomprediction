import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

falsebottom = []
def predictbottom(soundspeed, pulseinterval, maxdepth, n=3, m=3):
    # All times in s
    bottomdepth = range(0, maxdepth, 1)
    fb = []
    for i, _depth in enumerate(bottomdepth):
        # When does the n'th order bottom signal appear after send pulse
        bt = falsebottom(_depth, pulseinterval, soundspeed, n, m)
        fb.append((bt))
    return fb


def falsebottom(_depth, pulseinterval, soundspeed, n, m):
    bt = []
    dt_bottom = 2*_depth/soundspeed  # s
    for j, _n in enumerate(range(0, n)):
        for k, _m in enumerate(range(0, m)):
            dt_false = ((_n+1)*dt_bottom - _m*pulseinterval)
            _bt = dt_false*soundspeed/2
            if _bt > 0 and _bt <= pulseinterval*soundspeed/2.:
                bt.append((_depth, _n, _m, _bt))
    return bt


bottomdepth = 300 # m
n = 3 
m = 3
soundspeed = 1496 # m/s
pulseinterval = 0.45 # s

falsebottom = predictbottom(soundspeed, pulseinterval, bottomdepth, n, m)

