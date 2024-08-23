def calculate_total_energy(operating_time, hover_energy):
    total_energy_joules = operating_time * hover_energy
    total_energy_kj = total_energy_joules / 1000
    return total_energy_kj

# Get input from user
operating_time = float(input("Enter operating time in seconds: "))
hover_energy = float(input("Enter hover energy consumption in joules per second: "))

# Calculate and display result
total_energy = calculate_total_energy(operating_time, hover_energy)
print(f"Total energy consumption: {total_energy:.2f} kJ")



