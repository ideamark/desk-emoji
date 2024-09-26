import random
import threading

from common import *


def act_introduce(cmd):
    text = '''
        Hello! I'm Desk-Emoji, your friendly desktop robot here to bring joy and efficiency to your workspace.
        With my vibrant personality and helpful features, I aim to assist you in daily tasks while keeping you entertained.
        Whether you need a quick reminder, an inspirational quote, or just a smile, I'm here to lighten up your day and make your desktop experience more delightful.
        Let's optimize productivity together while adding a touch of fun and color to your work environment.
        Ready to explore the world of emojis and creativity with me? Let's get started!
        '''
    thread = threading.Thread(target=speech, args=(text,))
    thread.start()
    cmd.send('eye_happy')
    cmd.send('head_roll')
    cmd.send('eye_blink')
    cmd.send('head_move 20, 15, 30')
    cmd.send('eye_right')
    cmd.send('head_move -40, 0, 20')
    cmd.send('eye_left')
    cmd.send('head_center')
    cmd.send('eye_blink')
    act_happy(cmd)
    cmd.send('head_move 20 0 10')
    cmd.send('head_nod')
    cmd.send('head_move -40 0 10')
    cmd.send('head_nod')
    cmd.send('head_center')
    cmd.send('eye_blink')


def act_random(cmd, loop=False):
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
    while loop:
        act()
        time.sleep(random.randint(0, 8))


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
    for i in range(3):
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
    cmd.send(f'head_move {x_offset * -2} 0 20')
    look_side(x_offset * -2)
    cmd.send('head_center')
    cmd.send('eye_blink')


def act_emotion(cmd, emotion):
    if 'positive' in emotion:
        act_happy(cmd)
    elif 'negative' in emotion:
        act_sad(cmd)
    elif 'anger' in emotion:
        act_anger(cmd)
    elif 'surprise' in emotion:
        act_surprise(cmd)
    elif 'curious' in emotion:
        act_curiosity(cmd)
    else:
        act_random(cmd)


if __name__ == '__main__':
    cmd = CmdClient()

    # act_introduce(cmd)
    act_happy(cmd)
    time.sleep(1)
    act_sad(cmd)
    time.sleep(1)
    act_anger(cmd)
    time.sleep(1)
    act_surprise(cmd)
    time.sleep(1)
    act_curiosity(cmd)
    time.sleep(1)
    # act_random(cmd, loop=True)