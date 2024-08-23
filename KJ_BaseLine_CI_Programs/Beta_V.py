import numpy as np
import matplotlib.pyplot as plt
from New_P_Success import Success_Prob

def time_to_energy(time_seconds, hover_energy_rate=170):
    return time_seconds * hover_energy_rate / 1000 # Convert to kJ

V1_time = 800 # Initial time in seconds
V1_energy = time_to_energy(V1_time) # Convert to energy in kJ
P = 0.8
Plot_V = []
dist = []
Beta = []
Prod_Beta_V = []
init = 12000

for i in range(1800, 0, -100):
    if 0 <= i < 2000:
        C = 3 # dBm
    elif 2000 <= i < 4000:
        C = 6 # dBm
    elif 4000 <= i < 6000:
        C = 11 # dBm
    elif 6000 <= i < 8000:
        C = 20 # dBm
    elif 8000 <= i < 10000:
        C = 37 # dBm
    elif 10000 <= i <= 12000:
        C = 68 # dBm
    dist_travelled = 12000 - i
    time_to_fly = 2 * dist_travelled / 50
    energy_to_fly = time_to_energy(time_to_fly)
    V = max(V1_energy - energy_to_fly, 0)
    Plot_V.append(V)
    beta = Success_Prob(i)
    Beta.append(beta)
    Prod_Beta_V.append(beta * V)
    dist.append(i)

# Set up the plot
plt.rcParams.update({
    'font.family': 'Times New Roman',
    'font.weight': 'bold',
})

fig, ax1 = plt.subplots(figsize=(16, 10)) # Increased figure size

# Plot Beta on the first y-axis
color = 'tab:red'
ax1.set_xlabel('Distance'r'$(d_n)$', fontsize=50, fontweight='bold')
ax1.set_ylabel('Success Probability ('r'$\beta_{d_n}$)', color=color, fontsize=50, fontweight='bold')
ax1.plot(dist, Beta, color=color, label='Beta', linewidth=8)
ax1.tick_params(axis='y', labelcolor=color)

# Create a second y-axis and plot V
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Energy(E) KJ', color=color, fontsize=50, fontweight='bold')
ax2.plot(dist, Plot_V, color=color, label='Energy', linewidth=8)
ax2.tick_params(axis='y', labelcolor=color)

# Plot V*Beta on the second y-axis
color = 'tab:green'
ax2.plot(dist, Prod_Beta_V, color=color, label='Energy * Beta', linewidth=8)

# Customize ticks - Increase tick label font size
ax1.tick_params(axis='both', which='major', labelsize=50)  # Increased from 30 to 40
ax2.tick_params(axis='both', which='major', labelsize=50)  # Increased from 30 to 40

# Set custom x-ticks
x_ticks = np.arange(0, 2000, 250)
ax1.set_xticks(x_ticks)
ax1.set_xticklabels(x_ticks, rotation=45, ha='right') # Rotated labels

# Set custom y-ticks for both axes
ax1.set_yticks(np.arange(0.5, 1.01, 0.1)) # Reduced frequency
ax2.set_yticks(np.arange(50, 67, 4)) # Reduced frequency

# Add a legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, [r'$\beta_{d_n}$', r'$\hat{E_n}$', r'$\hat{E_n} \times \beta_{d_n}$'], loc='lower right', fontsize=50)

# Set title and adjust layout
fig.tight_layout()

# Add grid
ax1.grid(True, linestyle='--', linewidth=1.5, alpha=0.7)

# Make tick labels bold
for ax in [ax1, ax2]:
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight('bold')

plt.savefig('Beta_V.pdf', format='pdf', dpi=300, bbox_inches='tight')
plt.show()

print(f"Initial energy: {V1_energy:.2f} kJ")