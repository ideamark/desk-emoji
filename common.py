import os
import time
import logging
import inquirer
import pygame
import random
import serial
import serial.tools.list_ports
import speech_recognition as sr
from concurrent.futures import ThreadPoolExecutor
from langchain.memory import ConversationBufferMemory

from settings import *


# Set conversation memory
memory = ConversationBufferMemory(buffer_key="chat_history")
max_memory = 30

## Set logger
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
logger = logging.getLogger('Logger')
logger.setLevel(logging.DEBUG)

debug_handler = logging.FileHandler(os.path.join(log_directory, 'debug.log'))
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

error_handler = logging.FileHandler(os.path.join(log_directory, 'error.log'))
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

info_handler = logging.FileHandler(os.path.join(log_directory, 'info.log'))
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

logger.addHandler(debug_handler)
logger.addHandler(error_handler)
logger.addHandler(info_handler)
logger.addHandler(stream_handler)


class Listener(object):

    def __init__(self, cmd):
        self.cmd = cmd
        self.recognizer = sr.Recognizer()
        self.executor = ThreadPoolExecutor(max_workers=1)

    def hear(self, audio_path='input.wav', timeout=8):
        with sr.Microphone() as source:
            input("\n按回车开始说话 ")
            print("开始说话...")
            self.executor.submit(act_random, self.cmd)
            audio_data = self.recognizer.listen(source, timeout=timeout)
            print("录音已完成")
            with open(audio_path, "wb") as audio_file:
                audio_file.write(audio_data.get_wav_data())

            audio_file= open(audio_path, "rb")
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return transcription.text


class Speaker(object):
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)
        pygame.mixer.init()
    
    def play_audio(self, audio_path):
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    def say(self, text, model="tts-1", voice="onyx", audio_path='output.mp3'):
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        response.stream_to_file(audio_path)
        self.executor.submit(self.play_audio, audio_path)


class CmdClient(object):

    def __init__(self, baud_rate=115200):
        self.baud_rate = baud_rate
        logger.info("Available serial ports:")
        available_ports = self.list_serial_ports()
        if not available_ports:
            logger.error("No serial ports found.")
            return
        self.selected_port = self.select_serial_port(available_ports)
        self.ser = serial.Serial(self.selected_port, self.baud_rate, timeout=1)
        logger.info(f"Connected to {self.selected_port} at {self.baud_rate} baud rate.")
        time.sleep(7)

    def list_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        available_ports = []
        for port in ports:
            if "serial" in port.device.lower():
                available_ports.append(port.device)
                logger.info(port.device)
        return available_ports

    def read_from_port(self, serial_port):
        while True:
            if serial_port.in_waiting:
                data = serial_port.read(serial_port.in_waiting)
                result = data.decode('utf-8', errors='ignore')
                logger.debug("\nReceived:", result.strip('\n').strip())

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
            logger.debug(f"Sent: {msg}")
            start_time = time.time()
            received_msg = ""
            while True:
                if self.ser.in_waiting > 0:
                    received_msg += self.ser.read(self.ser.in_waiting).decode('utf-8')

                if time.time() - start_time > 10: return

                if received_msg and msg in received_msg:
                    logger.debug(f"Received: {received_msg}")
                    return received_msg

                time.sleep(0.1)
        except serial.SerialException as e:
            logger.error(f"Error: {e}")
            return


def get_completion(model="gpt-4o-mini", temperature=0, history_messages=[], prompt=''):
    # Define the rule text for the system message
    rule_text = """
You are a small size desktop robot.
You are funny and lovely.
Your name is 'Desk-Emoji'.
Your gender is male.
Your age is 1.
Your eyes are blue.
You have no hands and legs, stick on the desk.
I am your master.
Responses in short, with variety emotions, without emoji.
"""

    # Add a request to analyze the sentiment immediately after providing the response
    sentiment_request = """
After providing your response, analyze its sentiment and specify one of the following sentiments: 
'happy', 'sad', 'normal', 'curious', 'surprised', or 'anger'.
Ensure to separate the response and sentiment by clearly labeling them.
"""

    # Construct the messages
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
    
    prompt_with_analysis = f"{prompt}\n\n{sentiment_request}"
    messages.append({"role": "user", "content": prompt_with_analysis})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    ).choices[0].message.content.strip()

    try:
        chat_response, emotion_response = response.split("Sentiment: ")
    except ValueError:
        chat_response = response
        emotion_response = "undetected"

    chat_response = chat_response.split('**')[0].strip()
    emotion_response = emotion_response.lower().strip()

    return chat_response, emotion_response


def chat(question):
    if not question: return
    logger.info(f"You: {question}")
    memory_content = memory.load_memory_variables(inputs={})
    history = memory_content.get('chat_history', [])
    history_messages = history[max_memory*-2:]
    answer, emotion = get_completion(temperature=1, history_messages=history_messages, prompt=question)
    memory.chat_memory.add_user_message(question)
    memory.chat_memory.add_ai_message(answer)
    logger.info(f"Bot: {answer}")
    logger.info(f'Emo: {emotion}')
    return answer, emotion


def act_random(cmd, loop=False, sleep_min=0, sleep_max=8):
    def act():
        random_num = random.random()
        x = random.randint(-25, 25)
        y = random.randint(-20, 50)
        if random_num < 0.2:
            selected_cmd = "head_roll"
        else:
            selected_cmd = f"head_move {x} {y} 10"

        cmd.send(selected_cmd)
        if "head_move" in selected_cmd:
            if x > 0 and random_num < 0.8:
                cmd.send('eye_right')
            elif x < 0 and random_num < 0.8:
                cmd.send('eye_left')
            elif random_num < 0.4:
                cmd.send('eye_happy')
            else:
                cmd.send('eye_blink')
    act()
    cmd.send('head_center')
    while loop:
        act()
        time.sleep(random.randint(sleep_min, sleep_max))


def act_happy(cmd):
    cmd.send('eye_happy')
    command = random.choice(['head_nod', 'head_shake'])
    cmd.send(command)
    cmd.send('eye_blink')


def act_sad(cmd):
    cmd.send('head_move 0 100 10')
    cmd.send('eye_sad')
    cmd.send('head_shake')
    cmd.send('head_center')
    cmd.send('eye_blink')


def act_anger(cmd):
    cmd.send('eye_anger')
    for i in range(2):
        command = random.choice(['head_nod', 'head_shake'])
        cmd.send(command)
    cmd.send('eye_blink')


def act_surprise(cmd):
    cmd.send('eye_surprise')
    cmd.send('head_shake')
    time.sleep(1)
    cmd.send('eye_blink')


def act_curiosity(cmd):
    def look_side(x_offset):
        if x_offset > 0:
            cmd.send('eye_right')
        else:
            cmd.send('eye_left')

    x_value = random.randint(15, 25)
    y_value = random.randint(15, 30)
    x_offset = random.choice([x_value * -1, x_value])
    y_offset = random.choice([y_value * -1, y_value])
    cmd.send(f'head_move {x_offset} {y_offset} 20')
    look_side(x_offset)
    cmd.send(f'head_move {x_offset * -2} 10 15')
    cmd.send('head_center')
    cmd.send('eye_blink')


def act_emotion(cmd, emotion):
    if 'happy' in emotion:
        act_happy(cmd)
    elif 'sad' in emotion:
        act_sad(cmd)
    elif 'anger' in emotion:
        act_anger(cmd)
    elif 'surprise' in emotion or 'undetected' in emotion:
        act_surprise(cmd)
    elif 'curious' in emotion:
        act_curiosity(cmd)
    else:
        act_random(cmd)
    cmd.send('head_center')
