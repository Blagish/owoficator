import re
from random import choice, randint
from config import *
import vk


faces = ["(・`ω´・)", ";;w;;", "owo", "UwU", ">w<", "^w^", ":з"]


def owovify(s):
    s = re.sub(r'[rl]', 'w', s)
    s = re.sub(r'[RL]', 'W', s)
    s = re.sub(r'n[aeiou]', 'ny', s)
    s = re.sub(r'N[aeiou]', 'Ny', s)
    s = re.sub(r'N[AEIOU]', 'NY', s)
    s = re.sub(r'ove', 'uv', s)
    symb = ','
    for i in range(s.count(symb)):
        face = choice(faces)
        s = s.replace(symb, f' {face} ', 1)
    return s


def owovify_ru(s):
    s = re.sub(r'[рл]', 'в', s)
    s = re.sub(r'[РЛ]', 'В', s)
    s = re.sub(r'н[аеёиоуыэю]', 'ня', s)
    s = re.sub(r'Н[аеёиоуыэю]', 'Ня', s)
    s = re.sub(r'Н[АЕЁИОУЫЭЮ]', 'НЯ', s)
    symb = ','
    for i in range(s.count(symb)):
        face = choice(faces)
        s = s.replace(symb, f' {face} ', 1)
    return s


def random_id():
    return randint(1, 2147483647)


session = vk.Session()
api = vk.API(session, v=5.95)


def cut_appeal(command):
    if command == '' or command == '/':
        return None
    if command[0] == '/':
        command = command[1:]
    if command[0] == '[':
        command = command[command.index(']') + 1:]
    while command[0] == ' ':
        command = command[1:]
    return command


def message_splitter(m):
    while len(m[-1]) > 4095:
        m.append(m[-1][4095:])
        m[-2] = m[-2][:4095]
    return m


def send_message(peer_id, message, attachment=""):
    print(type(message), message)
    api.messages.send(access_token=token, peer_id=str(peer_id), message=message, attachment=attachment, random_id=random_id())


def process(data):
    if data['object'].get('reply_message'):
        fwd_msg = [data['object']['reply_message']['text']]
    else:
        fwd_msg = list(map(lambda x: x['text'], data['object']['fwd_messages']))
    if fwd_msg:
        output = []
        for command in fwd_msg:
            print("received command", command)
            command = cut_appeal(command)
            output.append(owovify_ru(command))
        output_m = message_splitter(output)
    else:
        command = data['object']['text']
        print("received command", command)
        command = cut_appeal(command)
        output = owovify_ru(command)
        output_m = message_splitter([output])
    return output_m
