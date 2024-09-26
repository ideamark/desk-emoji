import threading

from common import *
from action import *


def main():
    question = record.recognize()
    answer, emotion = chat(question)
    speech.say(answer)
    threading.Thread(target=act_emotion, args=(cmd, emotion)).start()


if __name__ == '__main__':
    logger.info('Initializing...')
    record = SpeechRecognition()
    speech = Speech()
    cmd = CmdClient()
    logger.info("Initialization complete.")
    try:
        while True:
            main()
    except KeyboardInterrupt:
        logger.info("Stopped.")
