import random

from common import *


def act_introduce(cmd, speech):
    text = '''
Hello 你好呀！我是Desk-Emoji，你的友好桌面机器人，致力于为你的工作空间带来快乐和效率。
凭借我充满活力的个性和实用的功能，我的目标是在辅助你完成日常任务的同时，为你带来乐趣。
无论你需要讲个笑话、一句励志名言，还是仅仅一个微笑，我都在这里为你增添一天的光彩，让你的桌面体验更加愉悦。
准备好与我一起探索 emoji 的创意世界了吗？让我们开始吧。
'''
    speech.say(text)
    cmd.send('eye_happy')
    cmd.send('head_roll')
    cmd.send('eye_blink')
    cmd.send('head_move 20, 15, 30')
    cmd.send('eye_right')
    cmd.send('head_move -40, 0, 20')
    cmd.send('eye_blink')
    cmd.send('head_center')
    cmd.send('eye_blink')
    cmd.send('eye_happy')
    cmd.send('head_shake')
    cmd.send('head_roll')
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
    cmd.send('head_center')
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


if __name__ == '__main__':
    cmd = CmdClient()
    speech = Speech()

    act_introduce(cmd, speech)
    act_random(cmd, loop=True)