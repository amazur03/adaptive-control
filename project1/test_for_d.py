import numpy as np
import matplotlib.pyplot as plt

# Fixed value for H
H = 7

# Time range from 0 to 6π
t = np.linspace(0, 6 * np.pi, 1000)

# Signal frequency
f = 2 / (2 * np.pi)

# Generate the triangular signal
signal = 2 * np.abs(2 * (t * f - np.floor(t * f + 0.5))) - 1

# List to store MSE values for different variances
mse_values = []

# Iterate over variance values from 0 to 0.5 with a step of 0.05
for d in np.arange(0, 0.55, 0.05):
    # Add noise with the specified variance
    noise = signal + (np.sqrt(d) * np.random.randn(len(t)))

    # Denoise the signal using a fixed H
    denoised = []
    for i in range(len(t)):
        if i >= H:
            denoised.append(np.average(noise[i-H:i]))
        else:
            denoised.append(np.average(noise[:i+1]))

    # Calculate MSE between original and denoised signal
    mse_denoised = np.mean((signal - denoised) ** 2)
    mse_values.append(mse_denoised)

    # Plot for each variance
    plt.figure(figsize=(10, 5))
    plt.scatter(t, signal, label='Original Signal', color='blue', s=4)
    plt.scatter(t, noise, color='red', label='Noisy Signal', s=4)
    plt.plot(t, denoised, label=f'Denoised Signal (Variance={d:.2f})', color='green')
    plt.title(f"Signal Denoising for Variance={d:.2f}")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.show()

# Display MSE values for each variance
for d, mse in zip(np.arange(0, 0.55, 0.05), mse_values):
    print(f'Mean Squared Error for Variance={d:.2f}: {mse:.4f}')

# Plot MSE values as a function of noise variance
plt.figure(figsize=(10, 5))
plt.plot(np.arange(0, 0.55, 0.05), mse_values, marker='o')
plt.title("MSE vs Variance of Noise")
plt.xlabel("Variance")
plt.ylabel("Mean Squared Error")
plt.grid(True)
plt.show()
