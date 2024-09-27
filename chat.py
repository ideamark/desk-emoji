import threading

from common import *
from action import *


def main():
    question = listener.hear()
    answer, emotion = chat(question)
    speaker.say(answer)
    threading.Thread(target=act_emotion, args=(cmd, emotion)).start()


if __name__ == '__main__':
    logger.info('Initializing...')
    cmd = CmdClient()
    listener = Listener(cmd)
    speaker = Speaker()
    logger.info("Initialization complete.")
    try:
        while True:
            main()
    except KeyboardInterrupt:
        logger.info("Stopped.")
