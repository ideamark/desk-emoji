import pyttsx3
import serial
import time
import inquirer
import serial.tools.list_ports

from langchain.memory import ConversationBufferMemory

from settings import *


# Set conversation memory
memory = ConversationBufferMemory(memory_key="chat_history")
max_memory = 30


class CmdClient(object):

    def __init__(self, baud_rate=115200):
        self.baud_rate = baud_rate
        print("Available serial ports:")
        available_ports = self.list_serial_ports()
        if not available_ports:
            print("No serial ports found.")
            return
        self.selected_port = self.select_serial_port(available_ports)
        self.ser = serial.Serial(self.selected_port, self.baud_rate, timeout=1)
        print(f"Connected to {self.selected_port} at {self.baud_rate} baud rate.")
        time.sleep(7)

    def list_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        available_ports = []
        for port in ports:
            if "serial" in port.device.lower():
                available_ports.append(port.device)
                print(port.device)
        return available_ports

    def read_from_port(self, serial_port):
        while True:
            if serial_port.in_waiting:
                data = serial_port.read(serial_port.in_waiting)
                result = data.decode('utf-8', errors='ignore')
                print("\nReceived:", result.strip('\n').strip())

    def select_serial_port(self, available_ports):
        if len(available_ports) == 1:
            return available_ports[0]
        questions = [
            inquirer.List('port',
                        message="Select a port",
                        choices=available_ports,
                        carousel=True)
        ]
        answers = inquirer.prompt(questions)
        return answers['port']

    def send(self, msg):
        try:
            encode_msg = msg.encode('utf-8')
            self.ser.write(encode_msg)
            print(f"Sent: {msg}")
            start_time = time.time()
            received_msg = ""
            while True:
                if self.ser.in_waiting > 0:
                    received_msg += self.ser.read(self.ser.in_waiting).decode('utf-8')

                if time.time() - start_time > 10: return

                if received_msg and msg in received_msg:
                    print(f"Received: {received_msg}")
                    return received_msg

                time.sleep(0.1)
        except serial.SerialException as e:
            print(f"Error: {e}")
            return


def get_completion(model="gpt-3.5-turbo", temperature=0, history_messages=[], prompt=''):
    rule_text = """
You are a small size desktop robot.
You are funny and lovely.
Your name is 'Desk-Emoji'.
Your gender is male.
Your age is 1.
Your eyes are blue.
You have no hands and legs, stick on the desk.
I am your master.
Responses with short English sentense, with variety emotions, without emoji.
"""
    messages = [{"role": "system", "content": rule_text}]
    for message in history_messages:
        if message.startswith('Human:'):
            role = "user"
            content = message.replace('Human:', '').strip()
        elif message.startswith('AI:'):
            role = "assistant"
            content = message.replace('AI:', '').strip()
        else:
            continue
        messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


def analyze_sentence(model="gpt-3.5-turbo", temperature=0, sentence=''):
    prompt = f"""
Please analyze the sentiment of the following sentence and return only one of the following words as your response: 
'positive', 'negative', ‘normal', 'curious', 'surprised' or 'anger'.
Make sure to return only the single most appropriate emotion based on the content.
\'\'\'{sentence}\'\'\'
"""
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    emotion = response.choices[0].message.content.strip().lower()
    print(f"Emotion: {emotion}")
    return emotion


def translate_sentence(model="gpt-3.5-turbo", temperature=0, sentence=''):
    prompt = f"""
Translate the sentence below to English.
\'\'\'{sentence}\'\'\'
"""
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


def speech(text):
    engine = pyttsx3.init()
    try:
        engine.endLoop()
        del engine
        engine = pyttsx3.init()
    except:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[9].id)
        engine.setProperty('rate', 180)
        engine.startLoop()
        engine.say(text)


def chat(question):
    if not question: return
    print(f"You: {question}")
    memory_content = memory.load_memory_variables(inputs={})
    history = memory_content.get('chat_history', [])
    history_messages = history.split('\n')[max_memory*-2:]
    answer = get_completion(temperature=1, history_messages=history_messages, prompt=question)
    memory.chat_memory.add_user_message(question)
    memory.chat_memory.add_ai_message(answer)
    print(f"Bot: {answer}\n")
    return answer
