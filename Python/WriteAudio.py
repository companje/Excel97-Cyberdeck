import queue,sys,os
import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

def record():
    q = queue.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    device_info = sd.query_devices(None, 'input')
    samplerate = int(device_info['default_samplerate'])
    filename = "output.wav"
    channels = 1

    with sf.SoundFile(filename, mode='w', samplerate=samplerate, channels=channels, subtype=None) as file:
        with sd.InputStream(samplerate=samplerate, device=None,  channels=channels, callback=callback):
            print('Recording...')
            while True:
                file.write(q.get())

                if not os.path.exists('is_recording.tmp'):
                    print('Done')
                    break


if __name__ == "__main__":
    try:
        while True:
            if os.path.exists('is_recording.tmp'):
                record()
            else:
                sd.sleep(100)

    except KeyboardInterrupt:
        print('\rBreak')

    except Exception as e:
        print("Error",e)