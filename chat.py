import numpy as np
import re
import sounddevice as sd
from faster_whisper import WhisperModel

from common import *
from action import *


active = True
frequency = 15

samplerate = 16000
block_duration = 0.5
block_size = int(samplerate * block_duration)
silence_threshold = 0.02
silence_duration_threshold = 3.0


def callback(indata, frames, time2, status):
    global audio_buffer, silence_duration, is_capturing, last_activity_time

    if status: print(status)
    audio_buffer = np.concatenate([audio_buffer, indata[:, 0]])
    volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))
    
    current_time = time.time()

    if volume_norm < silence_threshold:
        silence_duration += block_duration
        if silence_duration >= silence_duration_threshold and is_capturing:
            is_capturing = False
            print("Silence detected. Capture stopped.")
            segments, info = model.transcribe(audio_buffer, beam_size=5, language=model_language)
            audio_buffer = np.zeros((0,), dtype=np.float32)
            print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
            for segment in segments:
                question = segment.text.strip()
                answer = chat(question)
                if re.search(r'[\u4e00-\u9fa5]', answer):
                    answer = translate_sentence(sentence=answer)
                emotion = analyze_sentence(sentence=answer)
                speech(answer)
                act_emotion(cmd=cmd, emotion=emotion)
                cmd.send('head_center')
                last_activity_time = current_time
                break

    else:
        if not is_capturing:
            print("Sound detected. Starting capture.")
        silence_duration = 0.0
        is_capturing = True
        last_activity_time = current_time

    if current_time - last_activity_time > random.randint(frequency, frequency * 2):
        if active:
            act_random(cmd=cmd, loop=False)
            cmd.send('head_center')
        last_activity_time = current_time


if __name__ == '__main__':

    audio_buffer = np.zeros((0,), dtype=np.float32)
    silence_duration = 0.0
    is_capturing = False
    cmd = CmdClient()
    last_activity_time = time.time()

    with sd.InputStream(callback=callback, channels=1, samplerate=samplerate, dtype=np.float32):
        print(f"Loading whisper model {model_size}...")
        model = WhisperModel(model_size, device=model_device, compute_type=compute_type)
        print("Initialization complete.")
        print("\nListening...\n")
        try:
            while True:
                sd.sleep(1000)
        except KeyboardInterrupt:
            print("Stopped.")
