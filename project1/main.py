import numpy as np
import matplotlib.pyplot as plt

# Define the time range from 0 to 2π
t = np.linspace(0, 2 * np.pi, 300)

# Signal frequency
f = 2 / (2 * np.pi)

# Generate the triangular signal over this interval
signal = 2 * np.abs(2 * (t * f - np.floor(t * f + 0.5))) - 1

noise = []
denoised = []
d = 0.25  # Amplitude of the noise
H = 10    # Horizon (number of previous samples to average)

# Adding noise to the signal
for i in range(len(t)):
    noise.append(signal[i] + d * np.random.randn())

# Calculate the moving average with a horizon of H
for i in range(len(t)):
    if i >= H:
        # Calculate the average of the last H noise values
        denoised.append(np.average(noise[i-H:i]))
    else:
        # For the first H samples, calculate the average of the available samples
        denoised.append(np.average(noise[:i+1]))

# Plot the original signal, noisy signal, and denoised signal
plt.figure(figsize=(8, 4))
plt.plot(t, signal, label='Original Signal', color='blue')

# Scatter plot of the noisy signal in red with smaller dots
plt.scatter(t, noise, color='red', label='Noisy Signal', s=10)

# Plot the denoised signal in green
plt.plot(t, denoised, label='Denoised Signal', color='green')

plt.title("Triangular Signal with Noise and Denoised Signal (Moving Average)")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.show()
