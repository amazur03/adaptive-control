import numpy as np
import matplotlib.pyplot as plt

# Define the time range from 0 to 6π
t = np.linspace(0, 6 * np.pi, 1000)

# Signal frequency
f = 2 / (2 * np.pi)

# Generate the triangular signal over this interval
signal = 2 * np.abs(2 * (t * f - np.floor(t * f + 0.5))) - 1

# Parameters for noise
d = 0.1  # Variance of the noise

# Adding noise to the signal
noise = signal + (np.sqrt(d) * np.random.randn(len(t)))

# Store MSE values for different H
mse_values = []

# Calculate MSE for different horizons H from 1 to 15
for H in range(1, 16):
    denoised = []
    for i in range(len(t)):
        if i >= H:
            denoised.append(np.average(noise[i-H:i]))
        else:
            denoised.append(np.average(noise[:i+1]))

    # Calculate MSE between original and denoised signal
    mse_denoised = np.mean((signal - denoised) ** 2)
    mse_values.append(mse_denoised)

    # Plot for each H
    plt.figure(figsize=(10, 5))
    plt.scatter(t, signal, label='Original Signal', color='blue', s=4)
    plt.scatter(t, noise, color='red', label='Noisy Signal', s=4)
    plt.plot(t, denoised, label=f'Denoised Signal (H={H})', color='green')
    plt.title(f"Signal Denoising for H={H}")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.show()

# Print MSE values
for H, mse in zip(range(1, 16), mse_values):
    print(f'Mean Squared Error for H={H}: {mse:.4f}')

# Plotting MSE values
plt.figure(figsize=(10, 5))
plt.plot(range(1, 16), mse_values, marker='o')
plt.title("MSE vs Horizon (H)")
plt.xlabel("H (Horizon)")
plt.ylabel("Mean Squared Error")
plt.xticks(range(1, 16))
plt.grid(True)
plt.show()