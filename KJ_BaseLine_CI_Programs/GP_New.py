import numpy as np
import matplotlib.pyplot as plt
from skopt import gp_minimize
from skopt.space import Real
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, Matern, ConstantKernel as C
from Final_Finding_Expected_Reward_Gp import find_reward
import warnings

# Conversion function
def time_to_kj(time_seconds, hover_energy=170):
    return (time_seconds * hover_energy) / 1000

# Matplotlib settings
plt.rcParams.update({'font.family': 'Times New Roman'})

# Define the objective function
init = 14000
V = 3529  # Initial energy in seconds
P = 0.8
hover_energy_per_sec = 170  # J/s

warnings.filterwarnings("ignore")

def objective_function(x):
    if 0 <= x[0] < 2000:
        C1 = 3 # dBm
    elif 2000 <= x[0] < 4000:
        C1 = 6 # dBm
    elif 4000 <= x[0] < 6000:
        C1 = 11 # dBm
    elif 6000 <= x[0] < 8000:
        C1 = 20 # dBm
    elif 8000 <= x[0] < 10000:
        C1 = 37 # dBm
    elif 10000 <= x[0] <= 12000:
        C1 = 68 # dBm
    elif x[0] > 12000:
        C1 = 68
    
    dist_travelled = init - x[0]
    time_to_fly = (dist_travelled / 50) * 2
    V_after_flight = max(V - time_to_fly, 0)
    
    reward, count = find_reward(x[0], V_after_flight, P, C1)
    return -time_to_kj(reward)  # Return negative energy as we're minimizing

# Define the bounds for the optimization
bounds = [(0, init)]

# Define kernels for Gaussian Process Regression
kernels = {
    "Matern": C(1.0) * Matern(length_scale=1.0, nu=2.5)
}

# Perform Bayesian optimization with each kernel and plot the results
for kernel_name, kernel in kernels.items():
    print(f"Using kernel: {kernel_name}")
    result = gp_minimize(objective_function, bounds, acq_func="EI", n_calls=20, random_state=42, verbose=True)

    # Extract the results
    x_results = np.array(result.x_iters).reshape(-1, 1)
    y_results = -np.array(result.func_vals)

    # Plot function variance after each iteration
    for i in range(1, len(x_results) + 1):
        gp = GaussianProcessRegressor(kernel=kernel, alpha=1e-10, n_restarts_optimizer=10, random_state=42)
        gp.fit(x_results[:i], y_results[:i])
        
        x_plot = np.linspace(bounds[0][0], bounds[0][1], 1000).reshape(-1, 1)
        mu, sigma = gp.predict(x_plot, return_std=True)

        plt.figure(figsize=(12, 12))
        plt.plot(x_plot, mu, label='Mean Prediction', linewidth=3)
        plt.fill_between(x_plot.ravel(), mu - sigma, mu + sigma, alpha=0.1, color='blue', label='± 1 Sigma')
        plt.fill_between(x_plot.ravel(), mu - 2*sigma, mu + 2*sigma, alpha=0.1, color='green', label='± 2 Sigma')
        plt.fill_between(x_plot.ravel(), mu - 3*sigma, mu + 3*sigma, alpha=0.1, color='red', label='± 3 Sigma')
        
        plt.scatter(x_results[:i], y_results[:i], color='red', s=100, label='Sampled Points')
        
        max_idx = np.argmax(y_results[:i])
        plt.scatter(x_results[max_idx], y_results[max_idx], color='green', s=200, label='Current Maximum')

        plt.title(f'Iteration {i}', fontsize=60, fontweight='bold')
        plt.xlabel('Distance in Km', fontsize=60, fontweight='bold')
        plt.ylabel('Expected Residual Energy (KJ)', fontsize=60, fontweight='bold')
        # plt.legend(loc='best', prop={'size': 40, 'weight': 'bold'})
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.xticks(fontsize=60, fontweight='bold')
        plt.yticks(fontsize=60, fontweight='bold')
        plt.gca().set_xticks(np.arange(0, 15000, 2000))
        plt.gca().set_xticklabels([f'{int(x/1000)}' for x in np.arange(0, 15000, 2000)])
        plt.gca().set_xlabel('Distance (Km)', fontsize=60, fontweight='bold')
        plt.xlim(0, 14000)
        if i == 8:
            legend = plt.legend(loc='best', prop={'size': 40, 'weight': 'bold'})
            plt.setp(legend.get_texts(), fontsize=40, fontweight='bold')

        plt.savefig(f'iteration_{i}.pdf', format='pdf', dpi=300, bbox_inches='tight')
        plt.close()

    # Find the maximum value and corresponding point
    x_max = result.x
    y_max = -result.fun
    print(f"Maximum value found with {kernel_name} kernel:")
    print(f"  Energy: {y_max:.2f} kJ")
    print(f"  at distance = {x_max[0]:.2f} m\n")