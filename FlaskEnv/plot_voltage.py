# #### v1
# import pandas as pd
# import matplotlib.pyplot as plt

# # Read the CSV file
# df = pd.read_csv("telemetry_data.csv")

# # Constants for voltage conversion
# V_REF = 2.4  # Reference voltage for ADS1298 (in volts)
# MAX_24BIT = 2**23 - 1  # Maximum positive value for 24-bit (8,388,607)
# LSB_VOLTAGE = V_REF / MAX_24BIT  # Voltage per LSB (approx 0.2861 µV)

# # Function to convert 24-bit two's complement hex to signed integer
# def hex_to_signed_int(hex_str):
#     value = int(hex_str, 16)
#     if value & 0x800000:  # Check MSB for negative number
#         value -= 0x1000000  # Subtract 2^24
#     return value

# # Function to convert signed integer to voltage
# def int_to_voltage(signed_int):
#     return signed_int * LSB_VOLTAGE

# # Convert hex data to voltage for all channels
# channels = [f"channel{i}" for i in range(1, 9)]
# for channel in channels:
#     # First convert hex to signed integer
#     df[channel] = df[channel].apply(hex_to_signed_int)
#     # Then convert signed integer to voltage
#     df[channel] = df[channel].apply(int_to_voltage)

# # Create a figure with 8 subplots
# fig, axes = plt.subplots(8, 1, figsize=(10, 16), sharex=True)
# fig.suptitle("ECG Data - Voltage Values", fontsize=16)

# # Plot each channel
# for i, channel in enumerate(channels):
#     # Plot voltage (in volts) on the left y-axis
#     axes[i].plot(df.index, df[channel], label=channel, color="green")
#     axes[i].set_ylabel("Voltage (V)", fontsize=10, color="green")
#     axes[i].tick_params(axis="y", labelcolor="green")
#     axes[i].grid(True)
    
#     # Create a secondary y-axis for millivolts
#     axes_mv = axes[i].twinx()
#     axes_mv.plot(df.index, df[channel] * 1000, label=channel, color="green")  # Convert V to mV
#     axes_mv.set_ylabel("Voltage (mV)", fontsize=10, color="purple")
#     axes_mv.tick_params(axis="y", labelcolor="purple")
    
#     axes[i].legend(loc="upper right")

# # Set x-axis label for the bottom subplot
# axes[-1].set_xlabel("Sample Number", fontsize=12)

# # Adjust layout
# plt.tight_layout(rect=[0, 0, 1, 0.95])

# # Save and show the plot
# plt.savefig("ecg_voltage_plot.png")
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file directly from the local file system
df = pd.read_csv("telemetry_data.csv")

# Limit to the first 1000 data points
df = df.head(500)

# Constants for voltage conversion
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

# Convert hex data to millivolts for all channels
channels = [f"channel{i}" for i in range(1, 9)]
for channel in channels:
    # First convert hex to signed integer
    df[channel] = df[channel].apply(hex_to_signed_int)
    # Then convert signed integer to voltage (in volts)
    df[channel] = df[channel].apply(int_to_voltage)
    # Convert volts to millivolts
    df[channel] = df[channel] * 1000  # V to mV

# Create a figure with 8 subplots
fig, axes = plt.subplots(8, 1, figsize=(10, 16), sharex=True)
fig.suptitle("ECG Signal in Time Domain", fontsize=21)

# Plot each channel
for i, channel in enumerate(channels):
    axes[i].plot(df.index, df[channel], label=channel, color="red")
    axes[i].set_ylabel("mV", fontsize=15)
    axes[i].grid(True)
    axes[i].legend(loc="upper right")

# Set x-axis label for the bottom subplot
axes[-1].set_xlabel("Sample Number", fontsize=15)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save the plot
plt.savefig("ecg_voltage_plot.png")
plt.show()