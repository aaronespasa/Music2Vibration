# Music to Vibration
An app that help deaf people to enjoy music using AI

### Install the necessary packages
``$ pip install -r requirements.txt``

### Try the real-time spectrogram analyzer
``$ python spectrogram_analyzer.py``

If you have any trouble installing PyAudio, try to install igt using conda:

``$ conda install PyAudio``


# Python components

### 0. Raw Beat Generator

Input: Songs in mp3 (or other)

Output: JSON following X format

### 1. Training Data Generator

Input: JSON following X format

Output: JSON following X format

### 2. Model Input Data Generator

Input: Songs in mp3

Output: Image spectrogram in jpg (or other)
- 100px by 50px (or other)
- The X axis rate is 44100 (or other)
- The Y axis are the frequencies, linearly (or logarithmically) growing by 20HZ (or other)

### 3. Model Generator

Input: Spectrogram

Output: Boolean 1D Array with 100 columns (or other)

### 4. Model Inferer
Input: Spectrogram

Output: Boolean 1D Array with 100 columns (or other)

### 5. Model Translator
Using coremltools to translate the PyTorch model to CoreML -> https://github.com/apple/coremltools

# iOS components

### 1. Model Input Data Generator

### 2. Model Inferer

### 3. Model Output Adaptation
