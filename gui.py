#!/usr/bin/env python3

import sys
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
import matplotlib.cm as cm
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import predictfalsebottom as pfb
from matplotlib import cm

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)



def calculate_false_bottoms(soundspeed = 1496, bottomdepth = 400, pulseinterval = 0.45):
    #bottomdepth = 400 # m
    n = 3 # n'th reflection, 3 means we will see 1st reflection (strong), 2nd reflection (moderate) and 3rd (very weak)
    m = 3
    #soundspeed = 1496 # m/s
    #pulseinterval = 0.45 # s

    falsebottom = pfb.predictbottom(soundspeed, pulseinterval, bottomdepth, n, m)

    return falsebottom


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("False Bottom Prediction")
        self.setMinimumSize(800,800)

        hbox = QtWidgets.QHBoxLayout()

        label_sound_velocity = QtWidgets.QLabel("Sound velocity [m/s]", self)
        self.input_sound_velocity = QtWidgets.QLineEdit()
        self.input_sound_velocity.setText("1465")
        hbox.addWidget(label_sound_velocity)
        hbox.addWidget(self.input_sound_velocity)

        label_actual_depth = QtWidgets.QLabel("Actual depth [m]", self)
        self.input_actual_depth = QtWidgets.QLineEdit()
        self.input_actual_depth.setText("400")
        hbox.addWidget(label_actual_depth)
        hbox.addWidget(self.input_actual_depth)

        label_pulse_interval = QtWidgets.QLabel("Pulse interval [s]", self)
        self.input_pulse_interval = QtWidgets.QLineEdit()
        self.input_pulse_interval.setText("0.45")
        hbox.addWidget(label_pulse_interval)
        hbox.addWidget(self.input_pulse_interval)

        vbox = QtWidgets.QVBoxLayout()
        self.sc = MplCanvas(self, width=5, height=4, dpi=100) # Set up canvas
        vbox.addWidget(self.sc)

        toolbar = NavigationToolbar(self.sc, self)
        vbox.addWidget(toolbar)
        vbox.addLayout(hbox)

        self.okButton = QtWidgets.QPushButton("Redraw")
        self.okButton.clicked.connect(self.redraw)
        vbox.addWidget(self.okButton)

        widget = QtWidgets.QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)
        
        #plt.ion()
        self.redraw()
        self.show()

    def redraw(self):
        sound_velocity = int(self.input_sound_velocity.text())
        actual_depth = int(self.input_actual_depth.text())
        pulse_interval = float(self.input_pulse_interval.text())
        #try:
        #    sound_velocity = int(sound_velocity)
        #except ValueError:
        #    sound_velocity = 0
        #print(sound_velocity)

        self.sc.axes.cla() # Clear plot
        plt.clf()
        
        my_bottoms = calculate_false_bottoms(sound_velocity, actual_depth, pulse_interval)

        cmap_reversed = plt.get_cmap('Blues_r')
    
        myaxes = self.sc.axes
        myplot = my_bottoms.plot.scatter(ax=self.sc.axes, x='bottomdepth', y='depth', c='n',colormap=cmap_reversed,vmax = 4) # , c='n',colormap=cmap_reversed,vmax = 4
        # self.sc.fig.colorbar(self.sc.axes)

        y = np.array([1, 4, 3, 2, 7, 11])
        colors = plt.cm.hsv(y / float(max(y)))
        sm = plt.cm.ScalarMappable(cmap=plt.cm.hsv, norm=plt.Normalize(vmin=0, vmax=1))
        
        # Need to fix this colorbar
        #plt.colorbar(sm, ax=self.sc.axes)
        
        
        #cb = test.clear()
        #test.remove()
        
        self.sc.axes.invert_yaxis()
        self.sc.axes.set(xlabel='Actual bottomdepth [m]',
            ylabel='Depth where false bottom is present in echogram [m]',
            title='Pulse interval: '+str(pulse_interval)+', soundspeed: '+str(sound_velocity))
        
        # Needs a colorbar
        f = self.sc.fig.get_axes()[1].set_ylabel('Times the signal hits the bottom')

        #plt.show()
        self.sc.draw()
        self.sc.flush_events()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()