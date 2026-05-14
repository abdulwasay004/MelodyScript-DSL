import pygame

import numpy as np

instructions = [
    ('=', '375', None, 'beat'),
    ('=', '750', None, 'half'),
    ('=', '1500', None, 'whole'),
    ('PARAM', '262', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('/', 'beat', '2', 't1'),
    ('PARAM', '262', None, None),
    ('PARAM', 't1', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '294', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '262', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '349', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '330', None, None),
    ('PARAM', 'half', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '262', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('/', 'beat', '2', 't2'),
    ('PARAM', '262', None, None),
    ('PARAM', 't2', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '294', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '262', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '392', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '349', None, None),
    ('PARAM', 'half', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '262', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('/', 'beat', '2', 't3'),
    ('PARAM', '262', None, None),
    ('PARAM', 't3', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '523', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '440', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '349', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '330', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '294', None, None),
    ('PARAM', 'half', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '466', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('/', 'beat', '2', 't4'),
    ('PARAM', '466', None, None),
    ('PARAM', 't4', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '440', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '349', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '392', None, None),
    ('PARAM', 'beat', None, None),
    ('CALL', 'play', '2', None),
    ('PARAM', '349', None, None),
    ('PARAM', 'half', None, None),
    ('CALL', 'play', '2', None),
]

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

label_positions = {}
for i, ins in enumerate(instructions):
    if ins[0] == 'label':
        label_positions[ins[1]] = i

env = {}
params = []
pc = 0


def value(x):
    if x is None:
        return None
    if isinstance(x, int):
        return x
    if isinstance(x, str) and x.lstrip('-').isdigit():
        return int(x)
    return env.get(x, 0)


def generate_tone(freq, duration_ms):
    sample_rate = 44100
    n_samples = int(sample_rate * (duration_ms / 1000.0))
    t = np.linspace(0, duration_ms / 1000.0, n_samples, False)
    wave = np.sin(2 * np.pi * freq * t) * 4096
    wave = wave.astype(np.int16)
    return np.column_stack((wave, wave))


while pc < len(instructions):
    op, a1, a2, res = instructions[pc]

    if op == 'label':
        pc += 1
        continue

    if op == '=':
        env[res] = value(a1)

    elif op in ('+', '-', '*', '/'):
        v1 = value(a1)
        v2 = value(a2)
        if op == '+':
            env[res] = v1 + v2
        elif op == '-':
            env[res] = v1 - v2
        elif op == '*':
            env[res] = v1 * v2
        else:
            env[res] = v1 // v2 if v2 != 0 else 0

    elif op in ('>', '<', '=='):
        v1 = value(a1)
        v2 = value(a2)
        if op == '>':
            env[res] = 1 if v1 > v2 else 0
        elif op == '<':
            env[res] = 1 if v1 < v2 else 0
        else:
            env[res] = 1 if v1 == v2 else 0

    elif op == 'PARAM':
        params.append(value(a1))

    elif op == 'CALL':
        if a1 == 'play':
            freq = params[-2]
            dur = params[-1]
            if freq > 0:
                tone = generate_tone(freq, dur)
                sound = pygame.sndarray.make_sound(tone)
                sound.play()
            pygame.time.wait(int(dur))
            params.clear()

        elif a1 == 'rest':
            dur = params[-1]
            pygame.time.wait(int(dur))
            params.clear()

    elif op == 'jumpt':
        if value(a1) != 0:
            pc = label_positions[a2]
            continue

    elif op == 'jump':
        pc = label_positions[a1]
        continue

    pc += 1

pygame.quit()
