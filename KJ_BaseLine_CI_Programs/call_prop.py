import numpy as np
from New_P_Success import Success_Prob
from Final_Finding_Expected_Reward_Gp import find_reward
def call_prop_fun(V,initial_location,P):

    Attempt_array =  []
    Expected_Reward = []
    # print(V,initial_location,P)
    # input("print hi")
    dist_values = np.arange(0,initial_location,1)
    Expected_Reward = []
    
    for i in dist_values:
        if( 0 <= i < 2000):
            C = 3  # dBm
        if( 2000 <= i < 4000):
            C = 6 # dBm
        if( 4000 <= i < 6000):
            C = 11 # dBm
        if( 6000 <= i < 8000):
            C = 20 # dBm
        if( 8000 <= i < 10000):
            C = 37 # dBm
        if(i >= 10000):
            C = 68 # dBm
       
        dist_travelled = initial_location-i
        time_to_fly = dist_travelled/50
        time_to_fly = 2*time_to_fly
        V_after_flight = max(V - time_to_fly,0)
        if(V_after_flight > C):
            R_Val,count_val = find_reward(i,V_after_flight,P,C)
            # print(" Reward obatined = ",R_Val,count_val)
            Attempt_array.append(count_val)
            Expected_Reward.append(R_Val)
        else:
            Expected_Reward.append(0)
            Attempt_array.append(0)
    # print("\nExpected Reward = ",np.argmax(Expected_Reward),max(Expected_Reward))
    return(np.argmax(Expected_Reward),max(Expected_Reward))