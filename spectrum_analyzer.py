import sys
import struct
import numpy as np
from scipy.fftpack import fft
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import pyaudio

class SpectrumAnalyzer(object):
    """Display a real-time spectrum analyzer
       that uses the microphone as input

       Template: https://gist.github.com/Overdrivr/ed140520493e5d0f248d
    """
    def __init__(self):
        
        # pyqtgraph
        self.traces = dict()

        self.phase = 0
        self.t = np.arange(0, 3.0, 0.01)

        self.app = QtGui.QApplication([])
        
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        self.win = pg.GraphicsWindow(title="Spectrum Analyzer")
        self.win.resize(1000,600)
        self.win.setWindowTitle('SPECTRUM ANALYZER')
        self.canvas = self.win.addPlot(title="Pytelemetry")

        # PyAudio constants
        self.CHUNK = 1024 * 2          # samples per frame
        self.FORMAT = pyaudio.paInt16  # audio format
        self.CHANNELS = 1              # single channel for microphone
        self.RATE = 44100              # samples per second

        # # instantiate PyAudio
        # self.p = pyaudio.PyAudio()

        # self.stream = self.p.open(
        #     format=self.FORMAT,
        #     channels=self.CHANNELS,
        #     rate=self.RATE,
        #     input=True,
        #     output=True,
        #     frames_per_buffer=self.CHUNK,
        # )
        
        # # waveform and spectrum x points
        # self.x = np.arange(0, 2 * self.CHUNK, 2)
        # self.f = np.linspace(0, self.RATE / 2, self.CHUNK / 2)

    def start(self):
        """Execute the analyzer"""
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def trace(self,name,dataset_x,dataset_y):
        if name in self.traces:
            self.traces[name].setData(dataset_x,dataset_y)
        else:
            self.traces[name] = self.canvas.plot(pen='y')
    
    def update(self):
        """Update the values of the function everytime it's executed"""
        sin = np.sin(2 * np.pi * self.t + self.phase)
        cos = np.cos(2 * np.pi * self.t + self.phase)
        self.trace("sin", self.t, sin)
        self.trace("cos", self.t, cos)
        self.phase += 0.1
    
    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(30)

        self.start()

if __name__ == '__main__':
    SpectrumAnalyzer().animation()
