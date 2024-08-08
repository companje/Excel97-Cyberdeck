import sounddevice as sd
import numpy as np
import soundfile as sf
import keyboard
from pydub import AudioSegment

# Parameters
samplerate = 44100  # Sample rate in Hertz
channels = 1  # Number of audio channels


# Function to record audio
def record_audio(serialReader):
    print("Druk op de Cmd-toets om de opname te starten...")
    while not keyboard.is_pressed('cmd'):
        pass
    
    print("Opname gestart. Laat de Cmd-toets los om de opname te stoppen.")
    recording = []
    #is_recording = True
    
    def callback(indata, frames, time, status):
        nonlocal serialReader
        if serialReader._talk:
            recording.append(indata.copy())
            if not keyboard.is_pressed('cmd'):
                is_recording = False
                raise sd.CallbackStop()

    with sd.InputStream(samplerate=samplerate, channels=channels, dtype='int16', callback=callback):
        while serialReader._talk:
            sd.sleep(100)
    
    recording = np.concatenate(recording, axis=0)
    return recording

# Function to save the recording to a WAV file
def save_to_wav(recording, filename):
    sf.write(filename, recording, samplerate, subtype='PCM_16')

# Function to convert WAV to MP3
def convert_wav_to_mp3(wav_filename, mp3_filename):
    audio = AudioSegment.from_wav(wav_filename)
    audio.export(mp3_filename, format="mp3")
