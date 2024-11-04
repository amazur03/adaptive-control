import numpy as np
import matplotlib.pyplot as plt

# Function to generate a triangle signal
def generate_signal(t, frequency):
    return 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1

# Function to denoise the signal
def denoise_signal(noisy_signal, H):
    denoised = []
    for i in range(len(noisy_signal)):
        if i >= H:
            denoised.append(np.average(noisy_signal[i-H:i]))
        else:
            denoised.append(np.average(noisy_signal[:i+1]))
    return np.array(denoised)

# Parameter settings
signal_frequency = 2 / (2 * np.pi)
t = np.linspace(0, 6 * np.pi, 1000)
signal = generate_signal(t, signal_frequency)

# List of variances for analysis
variances = np.arange(0, 1.55, 0.05)
optimal_h_values = []

# MSE analysis for different variances
for d in variances:
    mse_values_horizon = []
    
    # Adding noise to the signal
    noise = signal + (np.sqrt(d) * np.random.randn(len(t)))
    
    # Calculating MSE for different values of H
    for H in range(1, 50):
        denoised = denoise_signal(noise, H)
        mse_denoised = np.mean((signal - denoised) ** 2)
        mse_values_horizon.append(mse_denoised)

     # Find the optimal H for the given variance
    optimal_h_index = np.argmin(mse_values_horizon)
    optimal_h_values.append(optimal_h_index + 1)  # +1 to get the correct H



# Plot of optimal H as a function of variance
plt.figure(figsize=(10, 5))
plt.plot(variances, optimal_h_values, marker='o')
plt.title("Optimal H vs Noise Variance")
plt.xlabel("Variance")
plt.ylabel("Optimal H")
plt.grid(True)
plt.show()

# Displaying optimal H values for each variance
for d, optimal_h in zip(variances, optimal_h_values):
    print(f'Optymalne H dla wariancji={d:.2f}: {optimal_h}')
