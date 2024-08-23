import numpy as np
# from I_P_Success import Success_Prob
from New_P_Success import Success_Prob
from matplotlib import pyplot as plt
import random
import scipy.stats as st

def number_of_attempts(i,V,P1,C1,P_values,V_values,count,Left_reward,Right_reward):
        P = P1
        C = C1
        R_V = V 
        reward = 0
        beta = Success_Prob(i)  
        # if(i == 14000):
        #     print("beta - ",beta)
        P_values.append(P)
        V_values.append(R_V)
        if( P > (C / (beta * R_V)) and R_V >= C):
        # if(count < 1):
            count = count + 1
            P_new = (P * (1-beta)) / (P * (1-beta) + (1 - P))
            Left_reward =  P*beta*(R_V-C)
            returned_value,count_val = number_of_attempts(i,R_V-C,P_new,C,P_values,V_values,count,Left_reward,Right_reward)
            Right_reward = (1-P*beta)*(-C)
            if(returned_value > 0):
                Right_reward = (1-P*beta)*(-C + returned_value)
            reward = Left_reward + Right_reward
            return reward,count_val
        else:
            return 0,count
# control loop
def find_reward(new_distance,V,P,C):
    # print(" P Value = ",P)
    P_values = []
    V_values = []
    Success_Prob(new_distance)
    # print(" beta  = ",Success_Prob(new_distance))
    return (number_of_attempts(new_distance,V,P,C,P_values,V_values,count = 0,Left_reward=0,Right_reward=0))
