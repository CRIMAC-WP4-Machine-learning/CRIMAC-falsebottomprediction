#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
x = np.arange(0, 10.0, 0.001)
f = 2*x

l, = plt.plot(f, x, lw=2)

def submit(text):
    ydata = int(text)*x
    l.set_ydata(ydata)
    ax.set_ylim(np.min(ydata), np.max(ydata))
    plt.draw()

axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
input_sound_velocity = TextBox(axbox, 'f(x)', initial="1450")
input_sound_velocity.on_submit(submit)

plt.show()