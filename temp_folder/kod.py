from scipy.fftpack import rfft, irfft, fft, ifft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
import time
import sounddevice as sd
from scipy import signal



#formiranje signala kao zbir 3 sinusoide
fs = 50 # frekvencija odabiranja
sec = 3 # duzina u sekundama
t = np.linspace(0, sec, fs * sec)
y1 = 10 * np.sin(2 * np.pi * 2 * t)
y2 = 5 * np.sin(2 * np.pi * 500 * t)
y3 = 3 * np.sin(2 * np.pi * 7000 * t) 
y = y1 + y2 + y3
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