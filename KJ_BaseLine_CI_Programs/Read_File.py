def read_arrays_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    
    # Create a new dictionary to store our variables
    local_vars = {}
    
    try:
        # Execute the content of the file in the context of our local_vars dictionary
        exec(content, {}, local_vars)
    except Exception as e:
        print(f"Warning: An error occurred while executing the file content: {e}")
        print("Some arrays might be incomplete or malformed.")
    
    return local_vars

# Read the arrays from the file
filename = 'simulation_resultcopy.txt'
try:
    arrays = read_arrays_from_file(filename)

    # Print the names of the arrays found and the first few elements of each
    for array_name, array_value in arrays.items():
        if array_name.startswith('V_'):  # Only process arrays starting with 'V_'
            print(f"Array name: {array_name}")
            try:
                print(f"First few elements: {array_value[0][0][:5]}")
            except Exception as e:
                print(f"Could not print first few elements: {e}")
            print()

    # Example of how to access the arrays
    array_names = ['V_Opt_ser', 'V_Opt_dcr', 'V_fixed_ser', 'V_rand_ser']
    for name in array_names:
        if name in arrays:
            print(f"Accessing {name}:")
            try:
                print(arrays[name][0][0][:5])
            except Exception as e:
                print(f"Could not access array: {e}")
        else:
            print(f"{name} not found in the file.")
        print()

except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")