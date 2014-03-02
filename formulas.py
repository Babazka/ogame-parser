#! coding: utf-8
import math

def R(value):
    return int(math.floor(value))

def energy_consumption(thing, level):
    mult = {
        'metal': -10,
        'crystal': -10,
        'deuterium': -20,
        'energy': 20,
    }[thing]
    return R(mult * level * (1.1 ** level))

# Рудник по добыче металла: 60*1,5^(уровень-1) металла и 15*1,5^(уровень-1) кристалла
# Рудник по добыче кристалла: 48*1,6^(уровень-1) металла и 24*1,6^(уровень-1) кристалла
# Синтезатор дейтерия: 225*1,5^(уровень-1) металла и 75*1,5^(уровень-1) кристалла
# Солнечная электростанция: 75*1,5^(уровень-1) металла и 30*1,5^(уровень-1) кристалла


def build_price(thing, level):
    mult1, mult2 = {
        'metal':     (60, 15),
        'crystal':   (48, 24),
        'deuterium': (225, 75),
        'energy':    (75, 30),
    }[thing]
    base1, base2 = {
        'metal':     (1.5, 1.5),
        'crystal':   (1.6, 1.6),
        'deuterium': (1.5, 1.5),
        'energy':    (1.5, 1.5),
    }[thing]
    return R(mult1 * (base1 ** (level - 1))), R(mult2 * (base2 ** (level - 1)))


def production(thing, level):
    mult = {
        'metal':     30,
        'crystal':   20,
        'deuterium': 10,
        'energy':    20,
    }[thing]
    return R(mult * level * (1.1 ** level))
