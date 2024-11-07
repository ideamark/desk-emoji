import threading

from common import *
from action import *


def main():
    input("\n按回车开始说话 ")
    question = listener.hear()
    answer, emotion = chat(question)
    speaker.say(answer)
    threading.Thread(target=act_emotion, args=(emotion,)).start()


if __name__ == '__main__':
    if not chat_gpt.check_status(): exit(1)
    cmd.select_port()
    cmd.connect()
    try:
        while True:
            main()
    except KeyboardInterrupt:
        logger.info("Stopped.")
