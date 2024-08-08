#!/usr/bin/env python3

# from openai import OpenAI
#from record_audio import *
# import whisper
# from chat_module import *
# from network_module import *
# import sys,os,time,json,openai,ijson,socket
# import argparse
import sys
from SerialReader import SerialReader
# from AudioRecorder import AudioRecorder

serial_reader = SerialReader('/dev/tty.usbmodem101', 9600)
serial_reader.start_reading()

# client = OpenAI()   #   sudo --preserve-env ./cyberdeck-cli.py

# controls = SerialReader()
# reader = SerialReader('COM3', 115200)
# reader.start()

# audio = AudioRecorder()

# try:
#     while True:

#         if not audio.is_recording and reader.is_talking:
#             audio.start()
            
#         # print(".",end="",flush=True)
#         print(reader.is_talking)
#         time.sleep(.01)

# except KeyboardInterrupt:
#     print("Stopping...")
#     reader.stop()


print("end")
sys.exit()

IP = "192.168.0.104" # TUINHUISJE
# IP = "10.0.2.15"
# IP = "172.16.88.35" # @ SETUP

while True:


    audio = record_audio()
    wav_filename = "tmp.wav"
    mp3_filename = "tmp.mp3"
    save_to_wav(audio, wav_filename)
    convert_wav_to_mp3(wav_filename, mp3_filename)

    audio_file = open("tmp.mp3", "rb")
    
    filesize = os.path.getsize("tmp.mp3")

    if filesize < 10000:
        print("skip")
        continue
    
    try:
        transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        print(transcription.text)

        continue

        # history = chat(transcription.text)
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            response_format={ "type": "json_object" },
            messages=[
                {'role': 'system', 'content': 'you return commands in json format to mutate a spreadsheet. Examples: {"items": [{"action":"setValue","range":"A1","value":"1"}, {"action":"setFormula","range":"B5:D5","value":"=SUM(A:A)"}, { "action": "setBackground", "range":"A1:A5", "red":"255", "green": "255", "blue": "0" }, { "action": "setBorder", "range":"B1:B4", value:"All"}, {"action":"setColumnWidth", "range":"A:Z", "value":"20"},  { "action":"showMessage", "message": "hello world" }, {action:"setConditionalFormat",range:"selection",criteria:"<0",foregroundColor:{"red":255,"green":0,"blue":0} }, {action:"startSequencer"} ... ] }'},
                {'role': 'user', 'content': transcription.text}
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
                        
                

        # if len(history)>1:
        #     message = history[-1] # alleen de laatste response versturen.
        #     cmd = message["content"]
        #     print("verstuur naar Cyberdeck:", cmd)

        #     send_udp_message(cmd, "192.168.0.104", 9999)
    
    except Exception as e:
        print(e)

    # print("commando aan ChatGPT: ",result["text"])


#     print("result:",history)

#     if len(history)>1:
#         message = history[-1] # alleen de laatste response versturen.
# # for message in history:
# #     if message["role"]=="assistant":
#         print("verstuur naar Cyberdeck:", message["content"])

