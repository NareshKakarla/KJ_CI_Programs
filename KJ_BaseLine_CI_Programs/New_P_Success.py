import math
import numpy as np
def Success_Prob(d):
     # d = int(input("Enter number of Nodes"))
    BW  = 125000
    N_0 = -174 #dBm
    NF = 36 # 6dB
    dN = N_0 + NF + 10*math.log10(BW) #dBm
    N =  ((10**(dN/10))/1000)    
    # print(" N = ",N)
    D_T_p = 19 # dBm
    T_p = ((10**(D_T_p/10))/1000)
    if( 0 <= d < 2000):
        dtheta_sf = - 6 # dBm
    if( 2000 <= d < 4000):
        dtheta_sf = - 9 # dBm
    if( 4000 <= d < 6000):
        dtheta_sf = - 12 # dBm
    if( 6000 <= d < 8000):
        dtheta_sf = - 15 # dBm
    if( 8000 <= d < 10000):
        dtheta_sf = - 17.5 # dBm
    if(d >= 10000):
        dtheta_sf = -20
    # print("SF = ",dtheta_sf)
        
    # dtheta_sf = - 20 # dBm
    theta_sf = ((10**(dtheta_sf/10))/1000)
    eta = 2.96
    lamda = (300/868.1)
    # print("Lamba = ",lamda)
    ld1 = lamda/((4*3.14*d+1)**eta)  # attenuation function
    dldi = 10*math.log10(ld1/10**-3)
    ldi = ((10**(dldi/10))/1000)
    # print("ldi = ",ldi)
    prob = math.exp(-((N*theta_sf)/(T_p*ldi)))
    if(d>=12000):
        prob = 0.0001
    return prob