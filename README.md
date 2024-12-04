# Excel 97 Cyberdeck
![Microsoft Excel 1997 Cyberdeck](https://github.com/user-attachments/assets/54127bf0-03a0-4611-bc85-48a0d74e7727)

The **Microsoft Excel 1997 Cyberdeck** is a one-of-a-kind project created by me Rick Companje for **Stichting SETUP** as part of their *Old Timer Tech* research initiative. This Cyberdeck combines retro hardware, innovative software, and cyberpunk aesthetics to deliver a fully functional, portable device for spreadsheet management without traditional input devices like a keyboard or mouse. It offers a fresh perspective on how we can creatively engage with old technology in new ways.

---

## Cyberdeck Overview

### Objectives
- **Reimagining old technology**: The Cyberdeck runs Microsoft Excel 1997 and enables users to input data, manage spreadsheets, and even create invoices using alternative input methods.
- **Local and secure operation**: The deck can function entirely offline, ensuring that all processing happens locally without any dependency on cloud services.
- **Aesthetic and functional**: Inspired by the cyberpunk ethos of the 1980s and office-core aesthetics of the 1990s, the device is rugged yet visually intriguing.

### Key Features
- **Alternative input**: The Cyberdeck features 18 buttons, 2 rotary encoders, 2 sliders, and 1 potentiometer.
  - **Rotary encoders**: Adjust numeric values in cells or switch between pre-selected cells.
  - **Sliders**: Scroll horizontally and vertically between spreadsheet fields.
  - **Buttons**: Includes an online/offline switch for the LLM (Large Language Model) functionality and a dedicated print button.
- **Audio**: Audio cues, including synthesized and sampled retro sounds, guide users through tasks.
  - Examples include spoken feedback for online/offline switching or saving an invoice.
- **Visual output**:
  - A **1440x1440** square touchscreen for navigation and display.
  - A **720x720** display embedded in a vintage Halina Diaviewer, magnified and distorted through a lens.

---

![Excel97-Cyberdeck](https://github.com/user-attachments/assets/00e298ec-89fb-430c-ac6f-e1f87c7dddb2)

## Online and Offline Modes

### Offline Mode
When offline, the Cyberdeck utilizes a local instance of OpenAI Whisper for speech-to-text transcription. You can dictate simple commands such as:

- "Enter 100 in cell A1."
- "Clear the contents of column B."

### Online Mode
In online mode, activated by the red LLM button, the Cyberdeck connects to OpenAI's ChatGPT 3.5 via API. This unlocks powerful natural language capabilities, allowing users to describe complex actions, such as:

- "Set the background of cells A5:F15 to yellow with a dashed border."
- "Generate a list of 15 random cities in the Netherlands in column E."

ChatGPT interprets these commands and generates JSON instructions for seamless execution in Excel.

---

## Technical Details

### Hardware
The Cyberdeck combines a **retro aluminum casing** from the 1970s, a vintage intercom front panel, and modern components. Key hardware features include:
- **Input**: Buttons, rotary encoders, sliders, and a microphone.
- **Output**: Dual displays and audio feedback for a tactile and engaging user experience.
- **Connections**: Arduino MEGA for sensor management and serial communication.

A detailed [materials list](./materials.pdf) is included in this repository for a complete breakdown of the hardware.

![connectors](doc/connectors.jpg)

---

## Software Components
The Cyberdeck software integrates Arduino firmware, Python scripts, and VBA macros to bridge the gap between hardware and Microsoft Excel 1997.

### Arduino Firmware
The Arduino MEGA handles input from all sensors and sends the data over serial communication.

- Example: Reading input from buttons and sliders**
```cpp
for (int i = 0; i < nButtons; i++) {
  (*all_buttons[i]).pressed = !digitalRead((*all_buttons[i]).pin);
  Serial.print((*all_buttons[i]).pressed ? (*all_buttons[i]).name : '.');
}
Serial.print(" ");
Serial.print(analogRead(POT));
Serial.print(" ");
Serial.print(analogRead(H_SLIDER));
Serial.print(" ");
Serial.print(analogRead(V_SLIDER));
Serial.println();
```

- Sleep mode and talk lamp brightness control:

```cpp
if (btn_talk.pressed) {
  timeBtnTalk = millis();
}
sleep = millis() - timeBtnTalk > 2000;
int brightness = btn_talk.pressed ? 255 : sleep ? max(a, 150) : 0;
analogWrite(LAMP_TALK, brightness);
```

### Python Scripts
####  SerialReader.py
This script processes data from the Arduino and communicates with Excel via UDP sockets.

- Field navigation using the rotary encoder:

```python
field = fields[field_index]
data = {"action": "select", "range": field}
send_udp_message(json.dumps(data), "127.0.0.1", 9999)
```

-  Audio feedback for printing invoices:

```python
if 'P' in value:
    filename = datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
    send_udp_message(json.dumps({"action": "saveCopyAndPrint", "value": filename + ".xls"}), "127.0.0.1", 9999)
    play("saved-to-usb")
```

#### Cyberdeck-cli.py
This script manages audio input and integrates Whisper and ChatGPT functionality.

- Offline transcription with Whisper:

```python
result = model.transcribe("output.mp3")
text = result["text"].strip()
data = { "action": "setValue", "value": text }
send_udp_message(json.dumps(data), IP, 9999)
Online natural language commands with ChatGPT:
```

```python
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'system', 'content': 'You are an Excel assistant generating JSON commands...'},
        {'role': 'user', 'content': text}
    ],
    temperature=0,
    stream=True
)
```

### VBA scripts in Excel 97
The VBA code processes JSON commands from Python to execute actions within Excel.

- Execute basic actions:

```vba
If action = "setValue" Then
    rng.value = value
ElseIf action = "increaseValue" Then
    rng.value = rng.value + value
End If
```

- Cell formatting:
```vba
If action = "setBackground" Then
    rng.Interior.color = RGB(msg("obj.red"), msg("obj.green"), msg("obj.blue"))
End If
```

![Screenshot 2024-12-04 at 15 38 52 copy](https://github.com/user-attachments/assets/c5e7cc29-4729-455b-9dcb-9b8bca52db45)

---

## Installation and Setup

### Requirements
**Hardware**: Arduino MEGA, sensors, buttons, and displays wired as per the documentation.
**Software**:
 - Arduino IDE: To upload the firmware.
 - Python 3.x: Install dependencies (pyserial, whisper, pyautogui, etc.).
 - Microsoft Excel: Add the VBA macros for processing commands.

### Step-by-Step Instructions
 1. Hardware Assembly:
     - Connect all components and verify wiring.
     - Use the provided materials list for reference.
 2. Upload Firmware:
     - Use the Arduino IDE to upload the firmware to the Arduino MEGA.
 3. Configure Software:
     - Install required Python packages using pip install -r requirements.txt.
     - Load the VBA macros into Excel.
 4. Launch the Cyberdeck:
     - Start SerialReader.py to process input from the Arduino.
     - Run Cyberdeck-cli.py for audio input and LLM processing.

---

## Licensing
- **Hardware and non-software components**: Licensed under CC BY-SA 4.0.
- **Software**: Distributed under the MIT License.

---

## Contributions
This project is open-source, and contributions are welcome! Feel free to submit pull requests, report issues, or share your ideas for improvement.

---

## Various notes
### audio generation
* sounds from the Speak & Spell toy
* sound produced with `say` command in MacOS.
```bash
say -v Zarvox "Welcome to the SETUP Utrecht  Microsoft Excel 97 CYBERDECK........[[rate 50]]enjoy your time[[rate 100]].......ha-ha-ha" -o welcome.aiff
```
* convert
```bash
ffmpeg -i saved2.aiff -filter:a "volume=2.0" /Volumes/Cyberdeck/github-repo/Excel/audio/saved2.wav -y
```
