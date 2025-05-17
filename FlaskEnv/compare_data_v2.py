import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data from both files
df_telemetry = pd.read_csv("telemetry_data_v3.csv")
df_all_lead = pd.read_excel("1_sample_all_lead_v3.xlsx")

# Limit to the first 1000 data points
df_telemetry = df_telemetry.head(350)
df_all_lead = df_all_lead.head(350)

# Constants for voltage conversion (for telemetry_data.csv)
V_REF = 2.4  # Reference voltage for ADS1298 (in volts)
MAX_24BIT = 2**23 - 1  # Maximum positive value for 24-bit (8,388,607)
LSB_VOLTAGE = V_REF / MAX_24BIT  # Voltage per LSB (approx 0.2861 µV)

# Function to convert 24-bit two's complement hex to signed integer
def hex_to_signed_int(hex_str):
    try:
        value = int(hex_str, 16)
        if value & 0x800000:  # Check MSB for negative number
            value -= 0x1000000  # Subtract 2^24
        return value
    except (ValueError, TypeError):
        return 0  # Return 0 for invalid hex values

# Function to convert signed integer to voltage (in volts)
def int_to_voltage(signed_int):
    return signed_int * LSB_VOLTAGE

# Convert telemetry data (hex) to millivolts
channels = [f"channel{i}" for i in range(1, 9)]
for channel in channels:
    df_telemetry[channel] = df_telemetry[channel].apply(hex_to_signed_int)
    df_telemetry[channel] = df_telemetry[channel].apply(int_to_voltage)
    df_telemetry[channel] = df_telemetry[channel] * 1000  # Convert volts to millivolts

# Apply a scaling factor to ALL_LEAD.xlsx data to test if units or gain are incorrect
scaling_factor = 6000  # Adjust this value to test (e.g., 1000, 6000, etc.)
all_lead_channels = [f"CH{i}" for i in range(1, 9)]
for channel in all_lead_channels:
    df_all_lead[channel] = df_all_lead[channel] * scaling_factor

# Calculate Mean Squared Error (MSE) for each channel
mse_values = {}
for i, (telemetry_col, all_lead_col) in enumerate(zip(channels, all_lead_channels)):
    mse = np.mean((df_telemetry[telemetry_col] - df_all_lead[all_lead_col]) ** 2)
    mse_values[telemetry_col] = mse

# Create a figure with 8 subplots (one for each channel)
fig, axes = plt.subplots(8, 1, figsize=(12, 20), sharex=True)
fig.suptitle(f"ECG Data Comparison", fontsize=21)

# Plot each channel
for i, (telemetry_col, all_lead_col) in enumerate(zip(channels, all_lead_channels)):
    # Plot telemetry data in blue
    axes[i].plot(df_telemetry.index, df_telemetry[telemetry_col], label=f"Database", color="red")
    # Plot ALL_LEAD data in red
    axes[i].plot(df_all_lead.index, df_all_lead[all_lead_col], label=f"Software", color="blue", alpha=0.7)
    # Add MSE to the plot
    # axes[i].text(0.01, 0.65, f"CH{i+1}", transform=axes[i].transAxes, fontsize=11, color="black")

    axes[i].text(0.02, 0.85, f"MSE: {mse_values[telemetry_col]:.6f}", transform=axes[i].transAxes, fontsize=10, color="black")
    axes[i].set_ylabel("mV", fontsize=15)
    axes[i].grid(True)
    axes[i].legend(loc="upper right")

# Set x-axis label for the bottom subplot
axes[-1].set_xlabel("Sample Number", fontsize=15)

axes[i].legend(loc="upper right", fontsize=15)  # Increased from default to 12

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save and show the plot
plt.savefig("ecg_comparison_plot_scaled.png")
plt.show()

# Print MSE values for reference
print("Mean Squared Error (MSE) for each channel:")
for channel, mse in mse_values.items():
    print(f"{channel}: {mse:.6f}")



    