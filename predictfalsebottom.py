#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

def predictbottom(soundspeed, pulseinterval, maxdepth, n=3, m=3):
    # All times in s
    bottomdepth = range(0, maxdepth, 1)
    #fb = []
    fb = pd.DataFrame(columns=['bottomdepth', 'n', 'm', 'depth'])
    for i, _depth in enumerate(bottomdepth):
        # When does the n'th order bottom signal appear after send pulse
        bt = falsebottom(_depth, pulseinterval, soundspeed, n, m)
        fb = pd.concat([fb, pd.DataFrame(bt)])
    return fb


def falsebottom(_depth, pulseinterval, soundspeed, n, m): # Detect single false bottom
    bt = []
    dt_bottom = 2*_depth/soundspeed
    for j, _n in enumerate(range(0, n)):
        for k, _m in enumerate(range(0, m)):
            dt_false = ((_n+1)*dt_bottom - _m*pulseinterval)
            _bt = dt_false*soundspeed/2
            if _bt > 0 and _bt <= pulseinterval*soundspeed/2.:
                bt.append({"bottomdepth": _depth, "n": _n+1, "m": _m, "depth": _bt})
    return bt

def example():
    bottomdepth = 400 # m
    n = 3 # n'th reflection, 3 means we will see 1st reflection (strong), 2nd reflection (moderate) and 3rd (very weak)
    m = 3
    soundspeed = 1496 # m/s
    pulseinterval = 0.45 # s

    falsebottom = predictbottom(soundspeed, pulseinterval, bottomdepth, n, m)
    
    print(falsebottom)

    cmap_reversed = plt.get_cmap('Blues_r')
    ax = falsebottom.plot.scatter(x='bottomdepth', y='depth', c='n',
                                  colormap=cmap_reversed, vmax = 4)
    ax.invert_yaxis()
    ax.set(xlabel='Actual bottomdepth [m]',
           ylabel='Depth where false bottom is present in echogram [m]',
           title='Pulse interval: '+str(pulseinterval)+', soundspeed: '+str(soundspeed))
    f = plt.gcf().get_axes()[1].set_ylabel('Times the signal hits the bottom')
    #plt.clim(1, 4)
    plt.show()

if __name__ == "__main__":
    # Run example if not imported
    example()
