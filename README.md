# Music to Vibration
An app that help deaf people to enjoy music using AI

### Install the necessary packages
``$ pip install -r requirements.txt``

### Try the real-time spectrogram analyzer
``$ python spectrogram_analyzer.py``

If you have any trouble installing PyAudio, try to install igt using conda:

``$ conda install PyAudio``


# Python components

### 1.1 Raw Beat Generator

Input: Songs in mp3 (or other)

Output: JSON following X format

Reference: http://tommymullaney.com/projects/rhythm-games-neural-networks

### 1.2 Rhythm Generator

Input: JSON following X format

Output: JSON following X format

### 1.3 Model Input Data Generator

Input: Songs in mp3

Output: Image spectrogram in jpg (or other)
- 100px by 50px (or other)
- The X axis rate is 44100 (or other)
- The Y axis are the frequencies, linearly (or logarithmically) growing by 20HZ (or other)

### 1.4 Model Generator

Input: Spectrogram

Output: Boolean 1D Array with 100 columns (or other)

### 1.5 Model Inferer
Input: Spectrogram

Output: Boolean 1D Array with 100 columns (or other)

### 1.6 Model Translator
Using coremltools to translate the PyTorch model to CoreML -> https://github.com/apple/coremltools

# iOS components

### 2.1 Model Input Data Generator

Reference: https://albanperli.github.io/iOS-Spectrogram/

### 2.2 Model Inferer

### 2.3 Model Output Adaptation
