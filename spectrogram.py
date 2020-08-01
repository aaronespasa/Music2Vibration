import os
import numpy as np
from pydub import AudioSegment
import librosa
import matplotlib.pyplot as plt

class CreateSpectogram(object):
    """Given an mp3 or wav audio, return
       its spectogram using matplotlib
    """
    def __init__(self, audio_dir, audio_name):
        self.audio_dir = audio_dir
        self.audio_name = audio_name
    
    def mp3_to_wav(self, audio_dir, audio_name):
        """Convert MP3 files into WAV files"""
        path = os.path.join(self.audio_dir, self.audio_name)
        wav_file = path + '.wav'

        # Check if the wav file already exists
        if not os.path.isfile(wav_file):
            mp3_file = AudioSegment.from_mp3(path + '.mp3')
            mp3_file.export(wav_file, format='.wav')

        return wav_file
    
    def plot_spectogram(self):
        """Plot the spectogram using matplotlib"""
        wav_file = self.mp3_to_wav(self.audio_dir, self.audio_name)
        y, sr = librosa.load(wav_file)

        plt.rcParams['figure.figsize'] = [12, 8]
        plt.rcParams.update({'font.size': 18})
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Time (s)")
        plt.specgram(y[0:100000], NFFT=5000, Fs=sr, noverlap=400, cmap='jet_r')
        plt.colorbar()
        plt.show()

if __name__ == '__main__':
    audio_dir = "music-examples"
    audio_name = "come-and-get-your-love"

    CreateSpectogram(audio_dir, audio_name).plot_spectogram()
