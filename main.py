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
            "Hour_16","Hour_17","Hour_18","Hour_19","Hour_20","Hour_21","Hour_22","Hour_23"
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

# C. Identify peak consumption periods
# GOAL 2: Identify peak consumption periods across all apartments and determine whether these peaks are caused by many apartments consuming moderately more, or a few apartments consuming extremely high values.

def compute_time_interval_averages(apartment_data):
    time_interval_avg = np.average(apartment_data, axis=0) # Average by hours
    return time_interval_avg

def compute_time_interval_maxima(apartment_data):
    time_interval_max = np.max(apartment_data, axis=0)
    return time_interval_max

def compute_peak_time_intervals(time_avg, k):
    mean_of_time_avgs = np.mean(time_avg)
    std_of_time_avgs = np.std(time_avg)

    threshold = mean_of_time_avgs + k * std_of_time_avgs

    peak_time_flags = time_avg > threshold

    return threshold, peak_time_flags
    
def compute_peak_contribution_distribution(columns, apartment_data, peak_flags):
    peak_analysis = []

    for hour_index in range(len(columns)):
        if not peak_flags[hour_index]:
            continue  # Skip non-peak hours

        # Extract all apartment usage for this hour
        hour_data = apartment_data[:, hour_index]
        hour_mean = np.mean(hour_data)
        hour_std = np.std(hour_data)

        # Define significant contributors
        significant_mask = hour_data > (hour_mean + hour_std)

        significant_count = np.sum(significant_mask)

        total_energy = np.sum(hour_data)
        significant_energy = np.sum(hour_data[significant_mask])

        contribution_ratio = (
            significant_energy / total_energy
            if total_energy > 0 else 0
        )

        peak_analysis.append({
            "hour_index": hour_index,
            "total_energy": total_energy,
            "significant_apartments": significant_count,
            "contribution_ratio": contribution_ratio
        })

    return peak_analysis

# D. Compute consumption stability metrics 
# GOAL 3: Compare apartments in terms of consumption stability, identifying which ones show regular usage patterns and which ones are highly irregular.

def compute_apartment_variance(apartment_data):
    apartment_variance = np.var(apartment_data, axis=1)

    return apartment_variance

def compute_apartment_std(apartment_data):
    apartment_std = np.std(apartment_data, axis=1)

    return apartment_std

def compute_apartment_coefficient_of_variation(apartment_avg, apartment_std):
    if np.any(apartment_avg==0):
        raise ValueError("Can not divide by zero.") 

    apartment_cv = apartment_std / apartment_avg

    return apartment_cv

def compute_stability_scores(apartment_cv):
    stability_scores = 1 / (1 + apartment_cv)

    return stability_scores

# E. Create Normalized Profiles
# Goal 4: Create a normalized consumption profile so apartments with different absolute usage levels can be compared fairly.
def compute_min_max_normalized_profiles(apartment_data):
    min_per_hour = np.min(apartment_data, axis=0)
    max_per_hour = np.max(apartment_data, axis=0)

    # Avoid division by zero
    range_per_hour = max_per_hour - min_per_hour
    if np.any(range_per_hour == 0):
        raise ValueError("Cannot normalize: at least one hour has zero variance")

    normalized = (apartment_data - min_per_hour) / range_per_hour
    return normalized

def compute_z_score_normalized_profiles(apartment_data):
    mean_per_hour = np.mean(apartment_data, axis=0)
    std_per_hour = np.std(apartment_data, axis=0)

    if np.any(std_per_hour == 0):
        raise ValueError("Cannot z-normalize: at least one hour has zero std")

    z_scores = (apartment_data - mean_per_hour) / std_per_hour
    return z_scores

# ========================
# 3. REPORTING / PRESENTATION SECTION
# ========================

# B. Apartment usage functions
def print_separator():
    """Print a separator line for visual organization of output."""
    print(SEPARATOR_LINE)

def print_newline():
    """Print a blank line for spacing in output."""
    print("\n")

# A. Print apartment data
def print_apartment_data(rows, columns, apartment_data):
    print("APARTMENT DATA: ")
    print(f"Rows: {rows}")
    print(f"Columns: {columns}")
    print(f"Data: \n")
    print(apartment_data)
    print(f"Data shape: {apartment_data.shape}")

# B. Print apartment usage information
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

def print_high_consumption_flags_by_apartment(rows, threshold, apartment_high_flags):
    print(f"Threshold is: {threshold}")
    print("APARTMENTS WITH HIGH ENERGY USAGE: ")
    for i in range(len(rows)):
        print(f"{rows[i]}: {apartment_high_flags[i]}")

# C. Print peak consumption periods
def print_time_interval_averages(columns, time_interval_avg):
    print("AVERAGE ENERGY USAGE BY TIME INTERVAL: ")
    for i in range(len(columns)):
        print(f"{columns[i]}: {round(time_interval_avg[i], 4)}")

def print_time_interval_max_values(columns, time_interval_max):
    print("MAXIMUM ENERGY USAGE BY TIME INTERVAL: ")
    for i in range(len(columns)):
        print(f"{columns[i]}: {round(time_interval_max[i], 4)}")

def print_high_consumption_flags_by_time_averages(columns, time_avg_flags, threshold):
    print(f"Threshold is: {threshold}")
    print("TIME PERIODS WITH HIGH ENERGY USAGE: ")
    for i in range(len(columns)):
        print(f"{columns[i]}: {time_avg_flags[i]}")

def print_peak_contribution_distribution(peak_analysis, columns=None):
    print("PEAK CONSUMPTION CONTRIBUTION ANALYSIS: ")

    if not peak_analysis:
        print("No peak hours detected.")
        return

    for peak in peak_analysis:
        hour_index = peak["hour_index"]
        total_energy = peak["total_energy"]
        significant_count = peak["significant_apartments"]
        contribution_ratio = peak["contribution_ratio"]

        hour_label = columns[hour_index] if columns else f"Hour_{hour_index:02d}"

        print("-" * 40)
        print(f"Peak Hour             : {hour_label}")
        print(f"Total Energy (kWh)    : {round(total_energy, 4)}")
        print(f"High-Usage Apartments : {significant_count}")
        print(f"Contribution Ratio    : {round(contribution_ratio * 100, 2)}%")

        # Interpretation
        if significant_count <= 2 and contribution_ratio > 0.5:
            interpretation = "Peak driven by a few extreme consumers."
        elif significant_count > 2 and contribution_ratio > 0.5:
            interpretation = "Peak driven by several high-usage apartments."
        else:
            interpretation = "Peak caused by moderate increases across apartments."

        print(f"Interpretation        : {interpretation}")

    print("-" * 40)

# D. Print consumption stability metrics 
def print_apartment_variance(rows, apartment_var):
    print("VARIANCE BY APARTMENT: ")
    for i in range(len(rows)):
        print(f"{rows[i]}: {round(apartment_var[i], 4)}")

def print_apartment_std(rows, apartment_std):
    print("STANDARD DEVIATION BY APARTMENT: ")
    for i in range(len(rows)):
        print(f"{rows[i]}: {round(apartment_std[i], 4)}")

def print_apartment_coefficient_of_variation(rows, apartment_cv):
    print("COEFFICIENT OF VARIATION BY APARTMENT: ")
    for i in range(len(rows)):
        print(f"{rows[i]}: {round(apartment_cv[i], 4)}")

def print_stability_scores(rows, apartment_stability_scores):
    print("STABILITY SCORES BY APARTMENT: ")
    for i in range(len(rows)):
        print(f"{rows[i]}: {round(apartment_stability_scores[i], 4)}")

def print_most_stable_and_irregular_apartments(rows, stability_scores, top_n=3):
    print("MOST STABLE AND UNSTABLE APARTMENTS: ")
    
    sorted_indices = np.argsort(stability_scores)

    stable_indices = sorted_indices[-top_n:][::-1] # Maximum, in reverse
    unstable_indices = sorted_indices[:top_n] # Minimum

    print("-" * 40)

    print(f"Most stable {top_n} apartments and their stability scores: ")
    for i in stable_indices:
        print(f"{rows[i]}: {round(stability_scores[i], 4)}")

    print("-" * 40)

    print(f"Most unstable {top_n} apartments and their stability scores: ")
    
    for i in unstable_indices:
        print(f"{rows[i]}: {round(stability_scores[i], 4)}")

    print("-" * 40)

# E. Print Normalized Profiles
def print_normalization_explanation():
    print("NORMALIZED CONSUMPTION PROFILES")
    print("Each hour was normalized independently across apartments.")
    print("This preserves hourly consumption patterns while removing")
    print("absolute usage scale differences between apartments.")

def print_normalized_profiles(rows, normalization_type, normalized_data, sample_count=5):
    print(f"APARTMENT NORMALIZED PROFILES BY {normalization_type}: (first {sample_count} apartments)")
    for i in range(sample_count):
        print(f"{rows[i]}: {np.round(normalized_data[i], 4)}")

# ========================
# 4. MAIN FUNCTION
# ========================

def main():
    apartment_data = load_data("apartment_data.txt")
    apartment_avg = compute_apartment_energy_averages(apartment_data)
    apartment_total = compute_apartment_energy_total(apartment_data)
    population_mean, population_median, population_std = compute_population_usage_statistics(apartment_avg)
    apartment_threshold, high_consumption_flags = compute_high_consumption_flags(apartment_avg, population_mean, population_std)

    time_interval_avg = compute_time_interval_averages(apartment_data)
    time_interval_max = compute_time_interval_maxima(apartment_data)
    time_threshold, peak_time_intervals = compute_peak_time_intervals(time_interval_avg, 0.8)
    peak_contribution_distribution = compute_peak_contribution_distribution(columns, apartment_data, peak_time_intervals)

    apartment_var = compute_apartment_variance(apartment_data)
    apartment_std = compute_apartment_std(apartment_data)
    try:
        apartment_cv = compute_apartment_coefficient_of_variation(apartment_avg, apartment_std)
    except ValueError as e:
        print(e)
    apartment_stability_score = compute_stability_scores(apartment_cv)

    try:
        min_max_normalized_data = compute_min_max_normalized_profiles(apartment_data)
        z_score_normalized_data = compute_z_score_normalized_profiles(apartment_data)
    except ValueError as e:
        print(e)

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
    print_high_consumption_flags_by_apartment(rows, apartment_threshold, high_consumption_flags)
    print_separator()

    print_newline()

    print_separator()
    print_time_interval_averages(columns, time_interval_avg)
    print_separator()

    print_newline()

    print_separator()
    print_time_interval_max_values(columns, time_interval_max)
    print_separator()

    print_newline()
        
    print_separator()
    print_high_consumption_flags_by_time_averages(columns, peak_time_intervals, threshold=time_threshold)
    print_separator()

    print_newline()

    print_separator()
    print_peak_contribution_distribution(peak_contribution_distribution, columns)
    print_separator()

    print_newline()

    print_separator()
    print_apartment_variance(rows, apartment_var)
    print_separator()

    print_newline()

    print_separator()
    print_apartment_std(rows, apartment_std)
    print_separator()

    print_newline()

    print_separator()
    print_apartment_coefficient_of_variation(rows, apartment_cv)
    print_separator()

    print_newline()

    print_separator()
    print_stability_scores(rows, apartment_stability_score)
    print_separator()

    print_newline()

    print_separator()
    print_most_stable_and_irregular_apartments(rows, apartment_stability_score, top_n = 4)
    print_separator()

    print_newline()

    print_separator()
    print_normalization_explanation()
    print_separator()
    
    print_newline()

    print_separator()
    print_normalized_profiles(rows, "MIN-MAX NORMALIZATION", min_max_normalized_data, sample_count=3)
    print_separator()
    
    print_newline()

    print_separator()
    print_normalized_profiles(rows, "Z-SCORE NORMALIZATION", z_score_normalized_data, sample_count=3)
    print_separator()
    
main()