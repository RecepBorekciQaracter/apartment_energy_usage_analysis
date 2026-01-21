import numpy as np

# Context
# A property management company is responsible for several apartment buildings and wants to reduce energy costs while promoting sustainable consumption. Each apartment is equipped with smart meters that record electricity usage at fixed intervals throughout the day.
# The company has collected numerical data representing electricity consumption (in kWh) for multiple apartments over several days. Each apartment belongs to a specific building, and all apartments follow the same measurement schedule.
# The data is provided as raw numerical arrays, without labels or preprocessing.

# Objective
# Design an analysis system that uses numerical computation to understand and optimize energy consumption patterns across apartments and buildings.

# ========================
# 1. DATA & CONFIGURATION SECTION
# ========================

SEPARATOR_LINE = "=" * 40

columns = [
            "Hour_00","Hour_01","Hour_02", "Hour_03","Hour_04","Hour_05","Hour_06","Hour_07",
            "Hour_08","Hour_09","Hour_10","Hour_11","Hour_12","Hour_13","Hour_14","Hour_15",
            "Hour_16","Hour_17","Hour_18","Hour_19","Hour_20","Hour_21","Hour_21","Hour_23"
        ]

rows = [
        "Apartment_1","Apartment_2","Apartment_3","Apartment_4","Apartment_5",
        "Apartment_6","Apartment_7","Apartment_8","Apartment_9","Apartment_10",
        "Apartment_11","Apartment_12","Apartment_13","Apartment_14","Apartment_15",
        "Apartment_16","Apartment_17","Apartment_18","Apartment_19","Apartment_20"
        ]

# ========================
# 2. COMPUTATION SECTION
# ========================

# A. Load apartment data from file
def load_data(file_path):
    """
    Load apartment energy usage data from a TXT file.
    
    Args:
        file_path (str): Path to the TXT file containing apartment data.
    
    Returns:
        np.ndarray: 2D array of daily apartment energy usages (apartments x hours).
    """
    apartment_data = np.genfromtxt(file_path, delimiter=",")
    return apartment_data

# B. Apartment usage functions
# GOAL 1: Determine the average daily energy consumption per apartment and identify which apartments consume significantly more than the rest.

# Compute and return daily total energy consumption per apartment
def compute_apartment_energy_total(apartment_data):
    apartment_total = np.sum(apartment_data, axis=1) # Total usage by apartment
    return apartment_total

# Compute and return average daily energy consumption per apartment
def compute_apartment_energy_averages(apartment_data):
    apartment_avg = np.average(apartment_data, axis=1) # Average by apartment
    return apartment_avg

def compute_population_usage_statistics(apartment_avg):
    population_mean = np.mean(apartment_avg)
    population_median = np.median(apartment_avg)
    population_std = np.std(apartment_avg)

    return population_mean, population_median, population_std

def compute_high_consumption_flags(apartment_avg, mean, std):
    K = 0.7
    THRESHOLD = mean + K * std

    high_consumption_flags = (apartment_avg > THRESHOLD)

    return THRESHOLD, high_consumption_flags

# ========================
# 3. REPORTING / PRESENTATION SECTION
# ========================

def print_separator():
    """Print a separator line for visual organization of output."""
    print(SEPARATOR_LINE)

def print_newline():
    """Print a blank line for spacing in output."""
    print("\n")

def print_apartment_data(rows, columns, apartment_data):
    print("APARTMENT DATA: ")
    print(f"Rows: {rows}")
    print(f"Columns: {columns}")
    print(f"Data: \n")
    print(apartment_data)
    print(apartment_data.shape)

def print_apartment_total(rows, apartment_total):
    print("TOTAL ENERGY USAGE BY APARTMENT: ")
    for i in range(len(rows)):
        print(f"{rows[i]}: {round(apartment_total[i], 4)}")

def print_apartment_averages(rows, apartment_avg):
    print("AVERAGE ENERGY USAGE BY APARTMENT: ")
    for i in range(len(rows)):
        print(f"{rows[i]}: {round(apartment_avg[i], 4)}")

def print_population_usage_statistics(population_mean, population_median, population_std):
    print("POPULATION STATISTICS: ")
    print(f"Mean: {round(population_mean, 4)}")
    print(f"Median: {round(population_median, 4)}")
    print(f"Standard Deviation: {round(population_std, 4)}")

def print_high_consumption_flags(rows, threshold, apartment_high_flags):
    print(f"Threshold is: {threshold}")
    print("APARTMENTS WITH HIGH ENERGY USAGE: ")
    for i in range(len(rows)):
        print(f"{rows[i]}: {apartment_high_flags[i]}")

# ========================
# 4. MAIN FUNCTION
# ========================

def main():
    apartment_data = load_data("apartment_data.txt")
    apartment_avg = compute_apartment_energy_averages(apartment_data)
    apartment_total = compute_apartment_energy_total(apartment_data)
    population_mean, population_median, population_std = compute_population_usage_statistics(apartment_avg)
    threshold, high_consumption_flags = compute_high_consumption_flags(apartment_avg, population_mean, population_std)

    print_separator()
    print_apartment_data(rows, columns, apartment_data)
    print_separator()

    print_newline()

    print_separator()
    print_apartment_total(rows, apartment_total)
    print_separator()

    print_newline()

    print_separator()
    print_apartment_averages(rows, apartment_avg)
    print_separator()

    print_newline()

    print_separator()
    print_population_usage_statistics(population_mean, population_median, population_std)
    print_separator()

    print_newline()

    print_separator()
    print_high_consumption_flags(rows, threshold, high_consumption_flags)
    print_separator()

main()