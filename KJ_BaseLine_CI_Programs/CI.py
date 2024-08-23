
import numpy as np
import scipy.stats as st
import random as rdm
import matplotlib.pyplot as plt


MaxS_Power=MaxS_SIML_AVG_POWERS
MaxS_Backlog=MaxS_SIML_AVG_BACKLOGS

# MaxWeight_Mean_Power=MaxW_Mean_SIML_AVG_POWERS
# MaxWeight_Mean_Backlog=MaxW_Mean_SIML_AVG_BACKLOGS


# MaxWeight_Beta_Power=MaxW_Beta_SIML_AVG_POWERS
# MaxWeight_Beta_Backlog=MaxW_Beta_SIML_AVG_BACKLOGS



MaxQ_Power= MaxQ_SIML_AVG_POWERS
MaxQ_Backlog=MaxQ_SIML_AVG_BACKLOGS


MaxWeight_Power=MaxW_SIML_AVG_POWERS
MaxWeight_Backlog= MaxW_SIML_AVG_BACKLOGS

Random_Power=Random_AVG_POWERS
Random_Backlog=Random_AVG_BACKLOGS

Optimal_Power=[90.00000045680001]*11

st_Mw_Oracle_p = []
st_Mw_Beta_p = []
st_Mw_Mean_p = []
st_MQ_p = []
st_MS_p = []
st_Random_p = []


st_Mw_Oracle_p_mean = []
st_Mw_Beta_p_mean = []
st_Mw_Mean_p_mean = []
st_MQ_p_mean = []
st_MS_p_mean = []
st_Random_p_mean = []


st_Mw_Oracle_b= []
st_Mw_Beta_b = []
st_Mw_Mean_b = []
st_MQ_b = []
st_MS_b = []
st_Random_b = []


st_Mw_Oracle_b_mean = []
st_Mw_Beta_b_mean = []
st_Mw_Mean_b_mean = []
st_MQ_b_mean = []
st_MS_b_mean = []
st_Random_b_mean = []




def meanConfidenceInterval(fl, cf):
    m  = np.mean(np.array(fl))
    se = st.sem(np.array(fl))
    h  = se * st.t.ppf((1+cf) / 2, len(fl)-1)
    return m,h

# ********** Max S Power *************#
for i in MaxS_Power:
    mh=meanConfidenceInterval(list(i),0.95)
    st_MS_p.append(mh[1])
    st_MS_p_mean.append(mh[0])
# print("Hello")
SimulatedPower_MS=st_MS_p_mean

# ********** Max S Buffer *************#

for i in MaxS_Backlog:
    mh=meanConfidenceInterval(list(i),0.95)
    st_MS_b.append(mh[1])
    st_MS_b_mean.append(mh[0])
# print("Hello")
SimulatedBuffer_MS=st_MS_b_mean


# ********** Max Q Power *************#
for i in MaxQ_Power:
    mh=meanConfidenceInterval(list(i),0.95)
    st_MQ_p.append(mh[1])
    st_MQ_p_mean.append(mh[0])
# print("Hello")
SimulatedPower_MQ=st_MQ_p_mean

# ********** Max Q Buffer *************#

for i in MaxQ_Backlog:
    mh=meanConfidenceInterval(list(i),0.95)
    st_MQ_b.append(mh[1])
    st_MQ_b_mean.append(mh[0])
# print("Hello")
SimulatedBuffer_MQ=st_MQ_b_mean

# ********** Max W Power *************#

for i in MaxWeight_Power:
    mh=meanConfidenceInterval(list(i),0.95)
    st_Mw_Oracle_p.append(mh[1])
    st_Mw_Oracle_p_mean.append(mh[0])
# print("Hello")
SimulatedPower_Mw = st_Mw_Oracle_p_mean

# ********** Max W Buffer *************#

for i in MaxWeight_Backlog:
    mh=meanConfidenceInterval(list(i),0.95)
    st_Mw_Oracle_b.append(mh[1])
    st_Mw_Oracle_b_mean.append(mh[0])
# print("Hello")
SimulatedBuffer_Mw = st_Mw_Oracle_b_mean


# # ********** MaxW Power Beta *************#

# for i in MaxWeight_Beta_Power:
#     mh=meanConfidenceInterval(list(i),0.95)
#     st_Mw_Beta_p.append(mh[1])
#     st_Mw_Beta_p_mean.append(mh[0])
# # print("Hello")
# SimulatedPower_Mw_Beta=st_Mw_Beta_p_mean

# # ********** MaxW Buffer Beta *************#

# for i in MaxWeight_Beta_Backlog:
#     mh=meanConfidenceInterval(list(i),0.95)
#     st_Mw_Beta_b.append(mh[1])
#     st_Mw_Beta_b_mean.append(mh[0])
# # print("Hello")
# SimulatedBuffer_Mw_Beta=st_Mw_Beta_b_mean


# # ********** MaxW Power Mean *************#

# for i in MaxWeight_Mean_Power:
#     mh=meanConfidenceInterval(list(i),0.95)
#     st_Mw_Mean_p.append(mh[1])
#     st_Mw_Mean_p_mean.append(mh[0])
# # print("Hello")
# SimulatedPower_Mw_Mean=st_Mw_Mean_p_mean

# # ********** MaxW Buffer Mean *************#

# for i in MaxWeight_Mean_Backlog:
#     mh=meanConfidenceInterval(list(i),0.95)
#     st_Mw_Mean_b.append(mh[1])
#     st_Mw_Mean_b_mean.append(mh[0])
# # print("Hello")
# SimulatedBuffer_Mw_Mean=st_Mw_Mean_b_mean

# ********** Random Power *************#

for i in Random_Power:
    mh=meanConfidenceInterval(list(i),0.95)
    st_Random_p.append(mh[1])
    st_Random_p_mean.append(mh[0])
# print("Hello")
SimulatedPower_Random=st_Random_p_mean

# ********** Random Buffer *************#

for i in Random_Backlog:
    mh=meanConfidenceInterval(list(i),0.95)
    st_Random_b.append(mh[1])
    st_Random_b_mean.append(mh[0])
# print("Hello")
SimulatedBuffer_Random=st_Random_b_mean

V=[0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]

fig, ax = plt.subplots(2)
plt.rcParams["font.family"] = "Times New Roman"

ax[0].set_ylabel("Average Power ")
ax[1].set_xlabel(" V ")
ax[1].set_ylabel("Average Buffer")
ax[0].grid(True)
ax[1].grid(True)

ax[0].errorbar(V,SimulatedPower_MQ,yerr=st_MQ_p,capsize=5, label="MQ",marker="^",color='black',markerfacecolor='none', alpha=0.5)
ax[0].errorbar(V,SimulatedPower_Mw,yerr=st_Mw_Oracle_p,capsize=5, label="MW_Oracle ",marker="o",color='blue', markerfacecolor='none',alpha=0.5)
# ax[0].errorbar(V,SimulatedPower_Mw_Beta,yerr=st_Mw_Beta_p,capsize=5, label="Mw_Beta",marker="d",color='red', markerfacecolor='none',alpha=0.5)
# ax[0].errorbar(V,SimulatedPower_Mw_Mean,yerr=st_Mw_Mean_p,capsize=5, label="Mw_Mean",marker="s",color='green', markerfacecolor='none',alpha=0.5)
ax[0].errorbar(V,SimulatedPower_Random,yerr=st_Random_p,capsize=5, label="Random",marker="x",color='cyan',markerfacecolor='none',alpha=0.5)
# ax[0].errorbar(V,SimulatedPower_MS,yerr=st_MS_p,capsize=5, label="MS",marker="^",color='Green',markerfacecolor='none',alpha=0.5)
ax[0].plot(V,Optimal_Power,label="LPP",marker="|",color='black', linestyle="dashed",markerfacecolor='none')


ax[1].errorbar(V,SimulatedBuffer_MQ,yerr=st_MQ_b,capsize=5, label="MQ",marker="^",color='black',markerfacecolor='none', alpha=0.5)
# ax[1].errorbar(V,SimulatedBuffer_MS,yerr=st_MS_b,capsize=5, label="MS",marker="^",color='Green',markerfacecolor='none', alpha=0.5)
ax[1].errorbar(V,SimulatedBuffer_Mw,yerr=st_Mw_Oracle_b,capsize=5, label="Mw_Oracle",marker="o",color='blue', markerfacecolor='none',alpha=0.5)
# ax[1].errorbar(V,SimulatedBuffer_Mw_Beta,yerr=st_Mw_Beta_b,capsize=5, label="MW_Beta",marker="d",color='red', markerfacecolor='none',alpha=0.5)
# ax[1].errorbar(V,SimulatedBuffer_Mw_Mean,yerr=st_Mw_Mean_b,capsize=5, label=" MW_Mean ",marker="s",color='green', markerfacecolor='none',alpha=0.5)
ax[1].errorbar(V,SimulatedBuffer_Random,yerr=st_Random_b,capsize=5, label="Random",marker="x",color='cyan', markerfacecolor='none',alpha=0.5)

# ax[0].set_yticks(np.arange(80,120,step=10))
# ax[1].set_yticks(np.arange(10,120,step=40))

ax[0].legend()
ax[1].legend()
plt.savefig("Plot_over_V.eps")
plt.show()
