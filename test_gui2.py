#!/usr/bin/env python3

import mpl_interactions.ipyplot as iplt
import matplotlib.pyplot as plt
import ipywidgets as widgets
import numpy as np
from matplotlib.widgets import TextBox

def fx_depth(x):
    return x

def fx_first_echo(x, actual_depth, sound_velocity):
    return x*actual_depth/sound_velocity
def fx_second_echo(x, actual_depth, sound_velocity):
    return 2*x*actual_depth/sound_velocity

def main():
    max_depth = 400 # X axis

    # List of depths
    x = np.linspace(0, max_depth, 100) # start, stop, num
    #tau = np.linspace(0.5, 1, 100) # start, stop, num

    actual_depth = np.linspace(0.1, 200, 100) # start, stop, num
    sound_velocity = np.linspace(1400, 1500, 100) # start, stop, num

    input_sound_velocity = widgets.FloatText(value=7, step=0.1)

    fig, ax = plt.subplots()

    controls = iplt.plot(
        x,
        fx_first_echo,
        actual_depth=actual_depth,
        sound_velocity=sound_velocity,
        label="f1"
    )
    
    _ = iplt.plot(
        x,
        fx_second_echo,
        controls=controls,
        label="f2"
    )

    plt.plot(x, -x, label="Depth")
    _ = plt.legend()
    
    plt.xlabel("Actual depth [m]")
    plt.ylabel("Depth of echo [m]")
 
    #plt.xlim([0, 1000])
    #plt.ylim([-100, 100])

    plt.show()


if __name__ == "__main__":
    main()