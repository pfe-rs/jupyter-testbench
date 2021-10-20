from scipy.fftpack import rfft, irfft, fft, ifft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
import time
import sounddevice as sd
from scipy import signal



# Formirati funkciju koja predstavlja signal kao zbir tri 
# sinusoide frekvencija frekv1, frekv2 i frekv3 redom; i amplituda
# a1, a2 i a3 istim redosledom. Svaki signal traje sec sekundi i 
# frekvencije odabiranja su fs Hz.

# Primer nekih konkretnih vrednosti je:
# frekv1 = 2, frekv2 = 500 i frekv3 = 7000 Hz
# a1 =  10, a2 = 5 i a3 = 3
# sec = 3s i fs = 50 Hz

def formiranje_signala(int: frekv1, int: frekv2, int: frekv3, int: a1, int: a2, int: a3, int: sec, int: fs) -> np.array:

    t = np.linspace(0, sec, fs * sec)
    y1 = a1 * np.sin(2 * np.pi * frekv1 * t)
    y2 = a2 * np.sin(2 * np.pi * frekv2 * t)
    y3 = a3 * np.sin(2 * np.pi * frekv3 * t) 
    y = y1 + y2 + y3

    return y




plt.plot(t,y)
plt.show()



#skaliranje datog signala za koeficijent 0.3
a = 0.3
y_skalirano = a*y
plt.plot(t,y)
plt.plot(t,y_skalirano)
plt.show()




#kasnjenje signala za 5
def shiftSignal(x, n0):
    N = len(x)
    y = np.zeros(N)
    if n0 < 0:
        y[:N + n0] = x[-n0:N]
    else:
        y[n0:N] = x[:N-n0]
    return y

y_pomereno = shiftSignal(y, 5)
plt.plot(t,y)
plt.plot(t[5:],y_pomereno[5:])
plt.show()




#threshold
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