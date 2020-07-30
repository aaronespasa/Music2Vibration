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

        # Plot design
        self.win = pg.GraphicsWindow(title="Spectrum Analyzer")
        self.win.resize(1000,600)
        self.win.setWindowTitle('SPECTRUM ANALYZER')
        
        wf_xlabels = [(0, '0'), (2048, '2048'), (4096, '4096')]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, '0'), (128, '128'), (255, '255')]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        self.waveform = self.win.addPlot(title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis})
        
        sp_xlabels = [(np.log10(10), '10'), (np.log10(100), '100'),
                      (np.log10(1000), '1000'), (np.log10(22050), '22050')]
        sp_xaxis = pg.AxisItem(orientation='bottom')
        sp_xaxis.setTicks([sp_xlabels])

        self.spectrum = self.win.addPlot(title='SPECTRUM', row=2, col=1, axisItems={'bottom': sp_xaxis})

        # PyAudio constants
        self.CHUNK = 1024 * 2          # samples per frame
        self.FORMAT = pyaudio.paInt16  # audio format
        self.CHANNELS = 1              # single channel for microphone
        self.RATE = 44100              # samples per second

        # waveform and spectrum points
        self.x = np.arange(0, 2 * self.CHUNK, 2)
        self.freq = np.linspace(0, int(self.RATE / 2), int(self.CHUNK / 2))

        # instantiate PyAudio
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )

    def start(self):
        """Execute the analyzer"""
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self,name,dataset_x,dataset_y):
        if name in self.traces:
            self.traces[name].setData(dataset_x,dataset_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(0, 255, padding=0)
                self.waveform.setXRange(0, 2 * self.CHUNK, padding=0.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='m', width=3)
                self.spectrum.setLogMode(x=True, y=True)
                self.spectrum.setYRange(-4, 0, padding=0)
                self.spectrum.setXRange(
                    np.log10(20), np.log10(self.RATE / 2), padding=0.005)
    
    def update(self):
        """Update the values of the function everytime it's executed"""
        # waveform binary data
        wf_data = self.stream.read(self.CHUNK)

        # convert data to integers, make np array, then offset it by 127
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)

        # create np array and offset by 128
        wf_data = np.array(wf_data, dtype='b')[::2] + 128

        # plot waveform data
        self.set_plotdata(name='waveform', dataset_x= self.x, dataset_y=wf_data)

        # spectrum data (convert wf_data to int and remove the offset)
        sp_data = fft(np.array(wf_data, dtype='int8') - 128)
        sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]) * 2 / (128 * self.CHUNK)

        # plot spectrum data
        self.set_plotdata(name='spectrum', dataset_x=self.freq, dataset_y=sp_data)

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)

        self.start()

if __name__ == '__main__':
    SpectrumAnalyzer().animation()
