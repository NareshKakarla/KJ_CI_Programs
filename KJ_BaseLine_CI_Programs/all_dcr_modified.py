from DC_Prob import Optimal_attempts_fun
from random_attempt_DCR import random_attempts_fun
from fixed_attempt_DCR import fixed_attempts_fun
from TSP_DCR_Final import TSP_attempts
import numpy as np
import scipy.stats as stats

def calculate_confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    se = stats.sem(data)
    ci = se * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean, ci

runs = 5000

V_Opt_ser = []
V_Opt_energy = []
V_Opt_dcr = []

V_rand_ser = []
V_rand_energy = []
V_rand_dcr = []

V_fixed_ser = []
V_fixed_energy = []
V_fixed_dcr = []

V_TSP_ser = []
V_TSP_energy = []
V_TSP_dcr = []

# Open a file to write the output
with open('simulation_results.txt', 'w') as f:
    for init_V in range(500, 2100, 500):
        f.write(f" ------------------For V = {init_V}------------------\n")
        print(f" ------------------For V = {init_V}------------------")
        
        optimal_service_rate = []
        optimal_energy = []
        optimal_dcr = []

        fixed_service_rate = []
        fixed_energy = []
        fixed_dcr = []

        random_service_rate = []
        random_energy = []
        random_dcr = []

        TSP_service_rate = []
        TSP_energy = []
        TSP_dcr = []
        
        for P_init in np.arange(0.2, 0.8, 0.2):
            f.write(f" For P = {P_init}\n")
            print(f" For P = {P_init}")
            
            # Run simulations and calculate confidence intervals
            opt_results = Optimal_attempts_fun(runs, init_V, P_init)
            rand_results = random_attempts_fun(runs, init_V, P_init)
            fixed_results = fixed_attempts_fun(runs, init_V, P_init)
            tsp_results = TSP_attempts(runs, init_V, P_init)

            optimal_service_rate.append(opt_results[0])
            optimal_energy.append(opt_results[1])
            optimal_dcr.append(opt_results[2])

            random_service_rate.append(rand_results[0])
            random_energy.append(rand_results[1])
            random_dcr.append(rand_results[2])

            fixed_service_rate.append(fixed_results[0])
            fixed_energy.append(fixed_results[1])
            fixed_dcr.append(fixed_results[2])

            TSP_service_rate.append(tsp_results[0])
            TSP_energy.append(tsp_results[1])
            TSP_dcr.append(tsp_results[2])

        V_Opt_ser.append(list(optimal_service_rate))
        V_Opt_energy.append(list(optimal_energy))
        V_Opt_dcr.append(list(optimal_dcr))

        V_fixed_ser.append(list(fixed_service_rate))
        V_fixed_energy.append(list(fixed_energy))
        V_fixed_dcr.append(list(fixed_dcr))

        V_rand_ser.append(list(random_service_rate))
        V_rand_energy.append(list(random_energy))
        V_rand_dcr.append(list(random_dcr))

        V_TSP_ser.append(list(TSP_service_rate))
        V_TSP_energy.append(list(TSP_energy))
        V_TSP_dcr.append(list(TSP_dcr))

    # Write results to file
    f.write("\nV_Opt_ser = \n")
    f.write(str(V_Opt_ser) + "\n")
    f.write("V_Opt_energy = \n")
    f.write(str(V_Opt_energy) + "\n")
    f.write("V_Opt_dcr = \n")
    f.write(str(V_Opt_dcr) + "\n")
    f.write("V_fixed_ser = \n")
    f.write(str(V_fixed_ser) + "\n")
    f.write("V_fixed_energy = \n")
    f.write(str(V_fixed_energy) + "\n")
    f.write("V_fixed_dcr = \n")
    f.write(str(V_fixed_dcr) + "\n")
    f.write("V_rand_ser = \n")
    f.write(str(V_rand_ser) + "\n")
    f.write("V_rand_energy = \n")
    f.write(str(V_rand_energy) + "\n")
    f.write("V_rand_dcr = \n")
    f.write(str(V_rand_dcr) + "\n")
    f.write("V_TSP_ser = \n")
    f.write(str(V_TSP_ser) + "\n")
    f.write("V_TSP_energy = \n")
    f.write(str(V_TSP_energy) + "\n")
    f.write("V_TSP_dcr = \n")
    f.write(str(V_TSP_dcr) + "\n")
    f.write("*****************\n")

# Print to console as well
print("Results have been written to simulation_results.txt")