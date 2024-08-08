#import whisper
import os,json,xlwt,sys
import pandas as pd
from pprint import pprint
from openai import OpenAI
from record_audio import *
from pprint import pprint


history_filename = "history2.json"
history = [] #json.loads(open(history_filename).read())

client = OpenAI() # sudo --preserve-env ./cyberdeck-cli.py

def chat(new_question, history=[]):

    if len(history)>1 and history[-2]["content"]==new_question:
        print("SKIP: ",new_question)
        return history

    history.append({"role": "user", "content": new_question})
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", #"gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=[

            {"role": "system", 
            "content": "ik geef tekstuele commando's om een spreadsheet te bewerken. kun je deze commando's omzetten naar gestructureerde acties (in een JSON array) die op cellen moeten worden toegepast. geef bij het genereren van een reeks of meerdere waarden geen array terug maar een waarde per losse cel. Het JSON object heeft de volgende vorm: { actions: [ { action: setValue, range: A1, value: 5 }, { action: setBackground, range:A1:A5, value:#ffff00 }, { action: setFormula, range: A3, value:=A1+A2 }, { action: setBorder, range:B1:B4, value:'All'} ] }"}] +
            history
    )

    assistant_response = completion.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_response})
    return history
