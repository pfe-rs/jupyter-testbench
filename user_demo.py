#!/usr/bin/env python

import numpy as np
from testbench import Testbench
from scipy.fft import fft
from testbench.tests.meanPower import meanPower

Testbench.author('Petar Petrović')


def heart_beats(data: np.array) -> int:
    signal = np.diff(data)
    br = 0
    i = 0
    while i < np.size(signal)-1:
        if signal[i] > 500000:
            br = br+1
            i = i + 100
        else:
            i = i + 1
    return br


def signalFormation(f1: float, f2: float, f3: float, A1: float, A2: float, A3: float) -> np.array:
    t = np.linspace(0, 3, 3 * 10000)
    x1 = A1 * np.sin(f1 * 2 * np.pi * t)
    x2 = A2 * np.sin(f2 * 2 * np.pi * t)
    x3 = A3 * np.sin(f3 * 2 * np.pi * t)
    return x1 + x2 + x3

def shiftSignal(x, K):
    N = len(x)
    y = np.zeros(N)
    if K < 0:
        y[:N + K] = x[-K:N]
    else:
        y[K:N] = x[:N-K]
    return y

def cutShiftSignal(x: np.array, K: float, S: float) -> np.array:
    y = x[S:]
    y1 = shiftSignal(y, K)
    return y1

def skaliranje_signala(signal: np.array, koef: float) -> np.array:
    return koef * signal

def squarePower(x: np.array) -> np.array:
    return x**2

def returnAmpCharacteristic(x: np.array) -> np.array:
    amp_spectrum = np.abs(fft(x))
    return amp_spectrum

def returnPhaseCharacteristic(x: np.array) -> np.array:
    phase_spectrum = np.angle(fft(x))
    return phase_spectrum
def meanPower(x: np.array) -> int:
    return np.mean(x) 

def movingAverage(x: np.array, w: int) -> np.array:
    smoothed = np.zeros(len(x) - w + 1)
    # ovde je potrebno implementirati zadatu funkciju
    for i in range(len(x) - w + 1):
        smoothed[i] = np.mean(x[i:i+w])
    return smoothed

if __name__ == '__main__':
    Testbench(heart_beats)
    Testbench(signalFormation)
    Testbench(cutShiftSignal)
    Testbench(skaliranje_signala)
    Testbench(squarePower)
    Testbench(cutShiftSignal)
    Testbench(returnAmpCharacteristic)
    Testbench(returnPhaseCharacteristic)
    Testbench(meanPower)
    Testbench(movingAverage)
    
