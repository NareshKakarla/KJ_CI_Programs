import matplotlib.pyplot as plt
import numpy as np

# Data
methods = ['DQN', 'GP']
rewards = [2600, 2850]

# Set up a professional color scheme
colors = ['#3498db', '#2ecc71']  # Blue and Green

# Create the bar plot
plt.figure(figsize=(6, 5))  # Reduced figure size
bars = plt.bar(methods, rewards, width=0.4, color=colors, edgecolor='black', linewidth=1.5)

# Customize the plot
plt.title(' V = 4000 P = 0.8', fontsize=16, fontweight='bold')
plt.xlabel('Method', fontsize=14, fontweight='bold')
plt.ylabel('Expected Residual Energy', fontsize=14, fontweight='bold')
plt.ylim(0, max(rewards) * 1.1)  # Reduced headroom

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:}',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

# Increase tick label font size and make them bold
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')

# Add grid lines for better readability
plt.grid(axis='y', linestyle='--', alpha=0.3)

# Remove top and right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Make left and bottom spines thicker
plt.gca().spines['left'].set_linewidth(1.5)
plt.gca().spines['bottom'].set_linewidth(1.5)

# Adjust layout and display the plot
plt.tight_layout()

# Add a subtle background color
plt.gca().set_facecolor('#f8f9fa')

# Reduce the space between bars by adjusting the x-axis limits
plt.xlim(-0.5, len(methods) - 0.5)
plt.savefig("Bar_Plot.pdf")

plt.show()