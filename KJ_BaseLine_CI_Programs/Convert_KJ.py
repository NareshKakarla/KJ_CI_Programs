import matplotlib.pyplot as plt
import numpy as np

def convert_to_kj(time_seconds, hover_energy=170):
    return (time_seconds * hover_energy) / 1000

def convert_data(data):
    return [[(x[0], convert_to_kj(x[1]), x[2]) for x in sublist] for sublist in data]

dat = [500,1000,1500,2000]
for i in dat:
    print(convert_to_kj(i,hover_energy= 170))