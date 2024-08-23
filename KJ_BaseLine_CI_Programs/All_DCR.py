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

runs = 60
Var_V_Opt = []
Var_V_Rand = []
Var_V_Fixed = []
Var_V_TSP = []

########################################


optimal_service_rate  = []
optimal_energy = []
optimal_dcr = []

fixed_service_rate  = []
fixed_energy = []
fixed_dcr = []

random_service_rate  = []
random_energy = []
random_dcr = []

TSP_service_rate  = []
TSP_energy = []
TSP_dcr = []

############################################


for init_V in range(500, 2100, 500):
    print(f" ------------------For V = {init_V}------------------")
    Opt_Over_P = []
    R_Over_P = []
    F_Over_P = []
    Var_V_TSP_P = []
    
    for P_init in np.arange(0.2, 0.8, 0.2):
        print(f" For P = {P_init}")
        
        # Run simulations and calculate confidence intervals
        opt_results = Optimal_attempts_fun(runs, init_V, P_init)
        rand_results = random_attempts_fun(runs, init_V, P_init)
        fixed_results = fixed_attempts_fun(runs, init_V, P_init)
        tsp_results = TSP_attempts(runs, init_V, P_init)

    Var_V_Opt.append(opt_results)
    Var_V_Rand.append(rand_results)
    Var_V_Fixed.append(fixed_results)
    Var_V_TSP.append(tsp_results)

    # Var_V_Opt.append(Opt_Over_P)
    # Var_V_Rand.append(R_Over_P)
    # Var_V_Fixed.append(F_Over_P)
    # Var_V_TSP.append(Var_V_TSP_P)


print("Optimal =", Var_V_Opt)
print("Rand  =", Var_V_Rand)
print("Fixed =", Var_V_Fixed)
print("TSP =", Var_V_TSP)