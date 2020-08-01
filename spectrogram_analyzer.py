""""
Display the waveform, the spectrum and the spectrogram
using the pyqtgraph package.
"""

import sys
import struct
import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import pyaudio

class SpectrogramAnalyzer(object):
    """Display a real-time spectrogram analyzer
       that uses the microphone as input

       Template: https://gist.github.com/Overdrivr/ed140520493e5d0f248d
    """
    def __init__(self):
        
        self.CHUNK = 1024 * 2          # samples per frame
        self.FORMAT = pyaudio.paInt16  # audio format
        self.CHANNELS = 1              # single channel for microphone
        self.RATE = 44100              # samples per second
        self.NFFT = 4096               # samples for fft
        self.SPECTROGRAM_FRAMES = int(1000 * 2048 // self.NFFT)

        self.TIME = np.arange(self.CHUNK) / self.RATE # time vector
        self.TIMEOUT = self.TIME.max()

        # waveform and spectrum points
        self.X = np.arange(0, 2 * self.CHUNK, 2)
        self.FREQ = np.linspace(0, int(self.RATE / 2), int(self.CHUNK / 2))

        # pyqtgraph
        self.traces = dict()

        self.phase = 0
        self.t = np.arange(0, 3.0, 0.01)

        self.app = QtGui.QApplication([])
        
        # enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        # main pyqtgraph configuration
        self.win = pg.GraphicsWindow(title="Spectrogram Analyzer")
        self.win.resize(1000,600)
        self.win.setWindowTitle('SPECTROGRAM ANALYZER')
        
        # waveform configuration
        wf_xlabels = [(0, '0'), (2048, '2048'), (4096, '4096')]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, '0'), (128, '128'), (255, '255')]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        self.waveform = self.win.addPlot(title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis})
        
        # spectrum configuration
        sp_xlabels = [(np.log10(10), '10'), (np.log10(100), '100'),
                      (np.log10(1000), '1000'), (np.log10(22050), '22050')]
        sp_xaxis = pg.AxisItem(orientation='bottom')
        sp_xaxis.setTicks([sp_xlabels])

        self.spectrum = self.win.addPlot(title='SPECTRUM', row=2, col=1, axisItems={'bottom': sp_xaxis})

        # spectrogram configuration
        self.spectrogram = self.win.addPlot(title='SPECTROGRAM', row=3, col=1)
        self.spectrogram.setLabel('left', 'Frequency', units='Hz')
        self.spectrogram.setLabel('bottom', 'Time', units='s')
        
        self.colormap = 'viridis'
        self.image_data = np.random.rand(20, 20)
        self.spectrogram_img = pg.ImageItem()
        self.spectrogram.addItem(self.spectrogram_img)
        self.spectrogram_img.setImage(self.image_data)
        self.pg_cmap = self.pg_colormap(self.colormap)
        self.spectrogram_img.setLookupTable(self.pg_cmap)

        # set scale: x (time, s) and y (frequency, Hz)
        self.spectrogram_img.scale(self.CHUNK / self.RATE, self.FREQ.max() * 2. / self.NFFT)

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

    def pg_colormap(self, cmap_name):
        """Converts a matplotlib colormap to a pyqtgraph colormap.
        
        Source: https://github.com/pyqtgraph/pyqtgraph/issues/561
        """
        # matplotlib color map
        plt_cmap = plt.get_cmap(cmap_name)
        plt_cmap._init()

        # Convert matplotlib colormap from 0-1 to 0 -255 for Qt
        pg_cmap = (plt_cmap._lut * 255).view(np.ndarray)
        
        return pg_cmap

    def set_plotdata(self,name,dataset_x,dataset_y):
        """Draw the data on the graph"""
        if name in self.traces:
            self.traces[name].setData(dataset_x,dataset_y)
        else:
            if name == 'waveform':
                self.traces[name] = self.waveform.plot(pen='c', width=3)
                self.waveform.setYRange(0, 255, padding=0)
                self.waveform.setXRange(0, 2 * self.CHUNK, padding=0.005)
            if name == 'spectrum':
                self.traces[name] = self.spectrum.plot(pen='m', width=3)
                # self.spectrum.setLogMode(x=True, y=True)
                # self.spectrum.setYRange(-4, 0, padding=0)
                # self.spectrum.setXRange(np.log10(20), np.log10(self.RATE / 2), padding=0.005)
                # self.spectrum.setXRange(20, self.RATE / 2, padding=0.005)
            if name == 'spectrogram':
                self.traces[name] = self.spectrogram.plot(pen='c', width=3)
                self.spectrogram.setXRange(0, self.SPECTROGRAM_FRAMES * self.TIMEOUT)
    
    def update(self):
        """Update the values of the function everytime it's executed"""
        # waveform binary data
        wf_data = self.stream.read(self.CHUNK)

        # convert data to integers, make np array, then offset it by 127
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)

        # create np array and offset by 128
        wf_data = np.array(wf_data, dtype='b')[::2] + 128

        # plot waveform data
        self.set_plotdata(name='waveform', dataset_x= self.X, dataset_y=wf_data)

        # spectrum data (convert wf_data to int and remove the offset)
        sp_data = fft(np.array(wf_data, dtype='int8') - 128)
        sp_data = np.abs(sp_data[0:int(self.CHUNK / 2)]) * 2 / (128 * self.CHUNK)

        # plot spectrum data
        self.set_plotdata(name='spectrum', dataset_x=self.FREQ, dataset_y=sp_data)

        # spectrogram

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)

        self.start()

if __name__ == '__main__':
    SpectrogramAnalyzer().animation()
