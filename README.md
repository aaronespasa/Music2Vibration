# Music to Vibration
An app that help deaf people to enjoy music using AI

### Install the necessary packages
``$ pip install -r requirements.txt``

### Try the real-time spectrum analyzer
``$ python spectrum_analyzer.py``

If you have any trouble installing PyAudio, try to install using conda:

``$ conda install PyAudio``


# Python components

# 1. Training Data Generator

Input 1: Songs in mp3.

Output 2: JSON following this format ??

# 2. Model Input Data Generator

Input 1: Songs in mp3

Output: Image spectrogram in jpb
- 100px by 50px
- The X axis rate is 44100
- The Y axis are the frequencies, linearly growing by 20HZ

# 3. Model Generator

Input: Spectrogram
Output: Beats at X second

# 4. Model Inferer
Input: Spectrogram
Output: Bests at X second

# iOS components

# 1. Model Input Data Generator

# 2. Model Inferer

# 3. Model Output Adaptation
