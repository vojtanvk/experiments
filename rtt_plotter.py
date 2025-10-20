import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set Matplotlib style for a slightly cleaner look
plt.style.use('seaborn-v0_8-darkgrid')

def plot_sensor_data(df: pd.DataFrame, title: str = "Time Series Data Analysis"):
# --- Plotting Setup ---
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Define a list of markers to use for different data types
    markers = ['o', 's', '^', 'D', 'v', '<', '>']
    
    # Iterate over unique types and plot each group separately
    unique_types = df['Type'].unique()
    
    for i, data_type in enumerate(unique_types):
        # Filter the data for the current type
        subset = df[df['Type'] == data_type]
        
        # Determine the marker style for this type
        marker_style = markers[i % len(markers)]

        # Plot X, Y, Z values against Timestamp
        ax.plot(subset['Timestamp'], subset['X'], 
                label=f'{data_type} - X', 
                marker=marker_style, 
                linestyle='-', 
                alpha=0.8)
        
        ax.plot(subset['Timestamp'], subset['Y'], 
                label=f'{data_type} - Y', 
                marker=marker_style, 
                linestyle='--', 
                alpha=0.8)
        
        ax.plot(subset['Timestamp'], subset['Z'], 
                label=f'{data_type} - Z', 
                marker=marker_style, 
                linestyle=':', 
                alpha=0.8)

    # --- Customization and Labels ---
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel("Timestamp (Arbitrary Units)", fontsize=12)
    ax.set_ylabel("Measured Value (X, Y, Z)", fontsize=12)
    
    # Place the legend outside the plot area for clarity
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    
    # Add a grid for easier reading
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Optimize layout to prevent labels from overlapping
    plt.tight_layout()
    
    # Display the plot
    plt.show()