#!/usr/bin/env python3

import mpl_interactions.ipyplot as iplt
import matplotlib.pyplot as plt
import ipywidgets as widgets
import numpy as np
from matplotlib.widgets import TextBox, Slider

import pandas as pd 

import predictfalsebottom as pfb

def fx_depth(x):
    return x

def fx_first_echo(x, actual_depth, sound_velocity):
    return x*actual_depth/sound_velocity
def fx_second_echo(x, actual_depth, sound_velocity):
    return 2*x*actual_depth/sound_velocity

def example():
    bottomdepth = 400 # m
    n = 3 # n'th reflection, 3 means we will see 1st reflection (strong), 2nd reflection (moderate) and 3rd (very weak)
    m = 3
    soundspeed = 1496 # m/s
    pulseinterval = 0.45 # s

    falsebottom = pfb.predictbottom(soundspeed, pulseinterval, bottomdepth, n, m)
    
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






def draw_example():
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)

    t = np.arange(-2.0, 2.0, 0.001)
    l, = ax.plot(t, np.zeros_like(t), lw=2)

    def submit(expression):
        ydata = eval(expression)
        l.set_ydata(ydata)
        ax.relim()
        ax.autoscale_view()
        plt.draw()


    axbox = fig.add_axes([0.1, 0.05, 0.8, 0.075])
    text_box = TextBox(axbox, "Evaluate", textalignment="center")
    text_box.on_submit(submit)
    text_box.set_val("t ** 2")  # Trigger `submit` with the initial string.

    plt.show()





def main():

    draw_example()
    exit()
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    x = np.linspace(0, 2 * np.pi, 200)


    def f(x, freq):
        return np.sin(x * freq)


    axfreq = plt.axes([0.25, 0.1, 0.65, 0.03])
    slider = Slider(axfreq, label="freq", valmin=0.05, valmax=10)
    controls = iplt.plot(x, f, freq=slider, ax=ax)
    plt.show()

    exit()

    fig, ax = plt.subplots()
    x = np.linspace(0, np.pi, 200)

    def f(x, tau, beta):
        return np.sin(x * tau) * x * beta


    tau = 5.61
    tau = widgets.FloatText(value=7, step=0.1)
    # tau = ipywidgets.fixed(5.61)
    controls = iplt.plot(x, f, tau=tau, beta=(0.25, 1))
    plt.show()
    exit()
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