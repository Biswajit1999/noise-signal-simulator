import numpy as np
import matplotlib.pyplot as plt


def generate_signal(x):
    """
    Generate a damped sinusoidal signal.
    This is a simple proxy for a scientific signal that fades with time.
    """
    return np.sin(2 * np.pi * x) * np.exp(-0.18 * x)


def moving_average(y, window_size):
    """
    Apply a simple moving average smoothing filter.
    """
    if window_size < 1:
        return y

    kernel = np.ones(window_size) / window_size
    return np.convolve(y, kernel, mode="same")


def calculate_snr(true_signal, noise):
    """
    Estimate signal-to-noise ratio using standard deviations.
    """
    signal_power = np.std(true_signal)
    noise_power = np.std(noise)

    if noise_power == 0:
        return np.inf

    return signal_power / noise_power


def main():
    print("Noise + Signal Simulator")
    print("------------------------")

    noise_level = float(input("Enter noise level, e.g. 0.2: "))
    smoothing_window = int(input("Enter smoothing window size, e.g. 25: "))

    np.random.seed(42)

    x = np.linspace(0, 10, 1200)

    true_signal = generate_signal(x)
    noise = np.random.normal(0, noise_level, size=len(x))
    noisy_signal = true_signal + noise
    smoothed_signal = moving_average(noisy_signal, smoothing_window)

    snr = calculate_snr(true_signal, noise)

    plt.figure(figsize=(11, 5.5))
    plt.plot(x, true_signal, label="True signal", linewidth=2)
    plt.plot(x, noisy_signal, label="Noisy observation", alpha=0.45)
    plt.plot(x, smoothed_signal, label="Smoothed signal", linewidth=2)

    plt.xlabel("Time / sample index")
    plt.ylabel("Signal amplitude")
    plt.title(f"Noise + Signal Simulator | Estimated SNR = {snr:.2f}")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig("outputs/noise_signal_simulation.png", dpi=300)
    plt.show()

    print(f"\nNoise level: {noise_level}")
    print(f"Smoothing window: {smoothing_window}")
    print(f"Estimated SNR: {snr:.2f}")
    print("Plot saved to outputs/noise_signal_simulation.png")


if __name__ == "__main__":
    main()
