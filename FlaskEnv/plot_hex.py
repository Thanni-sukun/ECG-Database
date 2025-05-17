# ### v1

# import pandas as pd
# import matplotlib.pyplot as plt

# # Read the CSV file
# df = pd.read_csv("telemetry_data.csv")

# # Function to convert 24-bit two's complement hex to signed integer
# def hex_to_signed_int(hex_str):
#     # Convert hex string to integer
#     value = int(hex_str, 16)
#     # Check if the MSB is 1 (indicating a negative number in two's complement)
#     if value & 0x800000:  # 0x800000 is 2^23 (MSB for 24-bit)
#         value -= 0x1000000  # Subtract 2^24 to get the negative value
#     return value

# # Convert hex data to signed integers for all channels
# channels = [f"channel{i}" for i in range(1, 9)]
# for channel in channels:
#     df[channel] = df[channel].apply(hex_to_signed_int)

# # Create a figure with 8 subplots (one for each channel)
# fig, axes = plt.subplots(8, 1, figsize=(10, 16), sharex=True)
# fig.suptitle("ECG Data - Raw Hex Values (Signed 24-bit Integers)", fontsize=16)

# # Plot each channel
# for i, channel in enumerate(channels):
#     axes[i].plot(df.index, df[channel], label=channel, color="blue")
#     axes[i].set_ylabel(channel, fontsize=10)
#     axes[i].grid(True)
#     axes[i].legend(loc="upper right")

# # Set x-axis label for the bottom subplot
# axes[-1].set_xlabel("Sample Number", fontsize=12)

# # Adjust layout to prevent overlap
# plt.tight_layout(rect=[0, 0, 1, 0.95])

# # Save and show the plot
# plt.savefig("ecg_hex_plot.png")
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file directly from the local file system
df = pd.read_csv("telemetry_data.csv")

# Limit to the first 1000 data points
df = df.head(1000)

# Function to convert 24-bit two's complement hex to signed integer
def hex_to_signed_int(hex_str):
    try:
        # Convert hex string to integer
        value = int(hex_str, 16)
        # Check if the MSB is 1 (indicating a negative number in two's complement)
        if value & 0x800000:  # 0x800000 is 2^23 (MSB for 24-bit)
            value -= 0x1000000  # Subtract 2^24 to get the negative value
        return value
    except (ValueError, TypeError):
        return 0  # Return 0 for invalid hex values

# Convert hex data to signed integers for all channels
channels = [f"channel{i}" for i in range(1, 9)]
for channel in channels:
    df[channel] = df[channel].apply(hex_to_signed_int)

# Create a figure with 8 subplots (one for each channel)
fig, axes = plt.subplots(8, 1, figsize=(10, 16), sharex=True)
fig.suptitle("ECG Data - Raw Hex Values (Signed 24-bit Integers, First 1000 Points)", fontsize=16)

# Plot each channel
for i, channel in enumerate(channels):
    axes[i].plot(df.index, df[channel], label=channel, color="blue")
    axes[i].set_ylabel(channel, fontsize=10)
    axes[i].grid(True)
    axes[i].legend(loc="upper right")

# Set x-axis label for the bottom subplot
axes[-1].set_xlabel("Sample Number", fontsize=12)

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save the plot
plt.savefig("ecg_hex_plot.png")
plt.show()