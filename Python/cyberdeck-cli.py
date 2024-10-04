import queue,sys,os,ijson,json
import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)
from openai import OpenAI
from pydub import AudioSegment
from network_module import *
from ConsoleWindow import *
import whisper

#IP = "192.168.1.109" # Huis
IP = "127.0.0.1"

#move_console_window(1500, 0)

client = OpenAI()

def convert_wav_to_mp3(wav_filename, mp3_filename):
    audio = AudioSegment.from_wav(wav_filename)
    audio.export(mp3_filename, format="mp3")

def process_audio_commands():
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
                    print('Recording Finished')
                    break

    convert_wav_to_mp3("output.wav","output.mp3")

    with open("output.mp3", "rb") as file:

        use_gpt = False

        if not os.path.exists('use_gpt.tmp'): 
             # if not use_gpt make transcription offline and send it as cell value
            result = model.transcribe("output.mp3")
            text = result["text"].strip()
            print(text)
            data = { "action":"setValue", "value":text }
            send_udp_message(json.dumps(data), IP, 9999)
            data = { "action":"playAudio", "value": "blooip-short.wav" }
            send_udp_message(json.dumps(data), IP, 9999)
        else:
            # run whisper online and use gpt to understand transcription
            try:
                transcription = client.audio.transcriptions.create(model="whisper-1", file=file)
                text = transcription.text
                
                print(text)

                response = client.chat.completions.create(
                    model='gpt-3.5-turbo',
                    response_format={ "type": "json_object" },
                    messages=[
                        {'role': 'system', 'content': 'you return commands in json format to mutate a spreadsheet. Examples: {"items": [{"action":"setValue","range":"A1","value":"1"}, {"action":"setFormula","range":"B5:D5","value":"=SUM(A:A)"}, { "action": "setBackground", "range":"A1:A5", "red":"255", "green": "255", "blue": "0" }, { "action": "setBorder", "range":"B1:B4", value:"All"}, {"action":"setColumnWidth", "range":"A:Z", "value":"20"},  { "action":"showMessage", "message": "hello world" }, {action:"setConditionalFormat",range:"selection",criteria:"<0",foregroundColor:{"red":255,"green":0,"blue":0} }, {action:"startSequencer"} ... ] }'},
                        {'role': 'user', 'content': text}
                    ],
                    temperature=0,  
                    stream=True
                )

                events = ijson.sendable_list()
                coro = ijson.items_coro(events, "items.item")
                seen_events = set()

                for chunk in response:
                    msg = chunk.choices[0].delta.content

                    if msg:
                        coro.send(msg.encode("utf-8"))
                    
                    if events:
                        unseen_events = [e for e in events if json.dumps(e) not in seen_events]
                        if unseen_events:
                            for event in unseen_events:
                                seen_events.add(json.dumps(event))
                                print(json.dumps(event))
                                send_udp_message(json.dumps(event), IP, 9999)
                                
            except:
                data = { "action":"playAudio", "value": "no-internet.wav" }
                send_udp_message(json.dumps(data), IP, 9999)
                



if __name__ == "__main__":
    model = whisper.load_model("base")  # Je kunt ook 'tiny', 'small', 'medium', 'large' gebruiken

    print("Cyberdeck-cli: druk op de rode knop en geef spraakcommando's")
    try:
        while True:
            if os.path.exists('is_recording.tmp'):
                print("rec")
                process_audio_commands()
            else:
                sd.sleep(100)

    except KeyboardInterrupt:
        print('\rBreak')

    except Exception as e:
        print("Error",e)