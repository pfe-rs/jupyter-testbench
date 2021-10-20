from scipy.fftpack import rfft, irfft, fft, ifft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
import time
import sounddevice as sd
from scipy import signal



# Formirati funkciju koja predstavlja signal kao zbir tri 
# sinusoide frekvencija frekv1, frekv2 i frekv3 redom; i amplituda
# a1, a2 i a3 istim redosledom. Svaki signal traje 3 sekunde i 
# frekvencije odabiranja su 50 Hz.

# Primer nekih konkretnih vrednosti je:
# frekv1 = 2, frekv2 = 500 i frekv3 = 7000 Hz
# a1 =  10, a2 = 5 i a3 = 3

def formiranje_signala(int: frekv1, int: frekv2, int: frekv3, int: a1, int: a2, int: a3, np.array: t) -> np.array:
    y1 = a1 * np.sin(2 * np.pi * frekv1 * t)
    y2 = a2 * np.sin(2 * np.pi * frekv2 * t)
    y3 = a3 * np.sin(2 * np.pi * frekv3 * t) 
    y = y1 + y2 + y3

    return y

# pozivanje funkcije
fs = 50
sec = 3
t = np.linspace(0, sec, fs * sec)
signal = formiranje_signala(2, 500, 7000, 10, 5, 3, t)
plt.plot(t, signal)
plt.show()



#Skalirati oformljeni signal sa koeficijentom koef

def skaliranje_signala(np.array: signal, float: koef) -> np.array:
    y_skalirano = koef*signal

    return y_skalirano

# pozivanje funkcije
koef = 0.3
skalirani_signal = skaliranje_signala(signal, koef)
plt.plot(t,signal)
plt.plot(t,skalirani_signal)
plt.show()


#Implementirati kasnjenje oformljenog signala za kas

def shiftSignal(x, n0):
    N = len(x)
    y = np.zeros(N)
    if n0 < 0:
        y[:N + n0] = x[-n0:N]
    else:
        y[n0:N] = x[:N-n0]
    return y

def kasnjenje_signala(np.array: signal, float: kas) -> np.array:
    kasniji_signal = shiftSignal(signal, kas)

    return kasniji_signal

kasniji_signal = kasnjenje_signala(signal, 5)
plt.plot(t,y)
plt.plot(t[5:],y_pomereno[5:])
plt.show()




#thrashold
koeficijenti = signal.butter(10, 3, 'hp', fs=fs, output='sos')
filtrirani_signal = signal.sosfilt(koeficijenti, y)
spektar1 = np.abs(fft(y))
spektar2 = np.abs(fft(filtrirani_signal))
x_spektar = np.linspace(0, fs//2, len(y)//2)

fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(t, y)
ax1.plot(t, filtrirani_signal)
ax2.plot(x_spektar, spektar1[:len(spektar1) // 2])
ax2.plot(x_spektar, spektar2[:len(spektar2) // 2])
plt.title('Visokopropusni filtar')
plt.xlabel('Vreme [s]')
plt.show()




#plotovanje x**2 snage prvobitnog i filtriranog signala
ps = np.abs(np.fft.fft(y))**2
time_step = 1 / fs
freqs = np.fft.fftfreq(y.size, time_step)
idx = np.argsort(freqs)

ps1 = np.abs(np.fft.fft(filtrirani_signal))**2
freqs1 = np.fft.fftfreq(filtrirani_signal.size, time_step)
idx1 = np.argsort(freqs1)

plt.plot(freqs[idx], ps[idx])
plt.plot(freqs1[idx1], ps1[idx1])
plt.show()