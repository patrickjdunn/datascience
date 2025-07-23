import pandas as pd
import math
import numpy as np    

print("\n=== Input variables ===")
# Define age
age = 65  # you can also prompt this from user if needed
# Set default values instead of prompting user
time_horizon = "10yr"  # or "30yr"
condition = "cvd"      # "cvd", "ascvd", or "hf"
gender = "female"      # "male" or "female"

print(f"Age and Gender: {age} year old {gender}")

# Cholesterol inputs
high_cholesterol = "No"  # "Yes" or "No"
cholesterol_treatment = "Taking medications"  # "No", "Taking medications", "Making lifestyle changes"
total_cholesterol = 200
HDL_cholesterol = 45
LDL_cholesterol = 130
triglycerides = 150
non_hdl_cholesterol = total_cholesterol - HDL_cholesterol

print(f"Cholesterol: Total Cholesterol {total_cholesterol} and HDL {HDL_cholesterol}")

# Blood pressure
hypertension = "Yes"  # "Yes" or "No"
hypertension_treatment = "Taking medications"  # "No", "Taking medications", "Making lifestyle changes"
systolic_blood_pressure = 160
diastolic_blood_pressure = 80
id = 1
datetime = "2023-10-01"
symptoms = False

print(f"Blood pressure:  {systolic_blood_pressure} / {diastolic_blood_pressure}")

# Diabetes and glucose
diabetes = "No"  # "Yes" or "No"
diabetes_treatment = "No"  # "No", "Taking medications", "Making lifestyle changes"
fasting_blood_sugar = 90
A1c = 5.7

print(f"Glucose:  {fasting_blood_sugar} and A1c {A1c}")

# Tobacco use
tobacco_use = "Current user"  # "Current user", "Former user", "Never used"
quit_years = 0  # Only for "Former user"
second_hand_smoke = "No"  # "Yes" or "No"

print(f"Tobacco use: {tobacco_use}")

# Weight and BMI
height_in = 67  # in inches
weight_lbs = 223   # in pounds

height = height_in * 2.54  # in centimeters
weight = weight_lbs / 2.2   # in kilograms
BMI = weight / (height / 100) ** 2

print(f"BMI: {BMI:.1f}")

# Physical activity
moderate_intensity = 75  # in minutes per week
vigorous_intensity = 75   # in minutes per week

print(f"Physical activity: moderate {moderate_intensity} and vigorous {vigorous_intensity}")

# Sleep
sleep_hours = 8

print(f"Sleep: {sleep_hours} hours")

#eGFR
egfr = 90 #15-150
print(f"eGFR: {egfr}")

#uacr  
uacr = 40 #.1-25000
print(f"uacr: {uacr}")

# Load SDI data
sdi_df = pd.read_csv("zip-sdi.csv")

def lookup_sdi(zip_code, sdi_df):

    try:
        if zip_code is None or zip_code == "":
            return None  # Early exit if zip code is not provided

        zip_code = int(zip_code)
        sdi_row = sdi_df[sdi_df["ZCTA5_FIPS"] == zip_code]

        if not sdi_row.empty:
            raw_sdi = float(sdi_row.iloc[0]["SDI_score"])
            sdi_normalized = round(raw_sdi / 10)
            sdi_final = min(max(sdi_normalized, 1), 9)
            return sdi_final
        else:
            return None  # ZIP not found in dataset

    except Exception as e:
        return None  # Any other error results in None

def get_user_input():
    while True:
        zip_code = input("Enter your ZIP code (or press Enter to skip): ").strip()

        # Allow None or empty input
        if zip_code.lower() == "none" or zip_code == "":
            return None

        # Validate 5-digit ZIP
        elif zip_code.isdigit() and len(zip_code) == 5:
            return zip_code

        else:
            print("Invalid ZIP code. Please enter a 5-digit number or leave blank to skip.")

# Safe SDI lookup that handles missing zip code
def safe_lookup_sdi(zip_code, sdi_df):
    if zip_code is None:
        print("No ZIP code provided. SDI will not be calculated.")
        return None
    try:
        sdi = lookup_sdi(zip_code, sdi_df)
        return sdi
    except Exception as e:
        print(f"Error looking up SDI for ZIP code {zip_code}: {e}")
        return None

# Main workflow
zip_code = get_user_input()
sdi = safe_lookup_sdi(zip_code, sdi_df)

if sdi is not None:
    print(f"SDI for ZIP code {zip_code}: {sdi}")
else:
    print("No SDI value retrieved.")

#zip_code = 78641
#sdi = lookup_sdi(zip_code, sdi_df)
#print(f"SDI for ZIP code {zip_code}: {sdi}")

# Dictionary of coefficients
age_coefficients = {
    "10yr_cvd_female": 0.7716794,
    "10yr_cvd_male": 0.7847578,
    "10yr_ascvd_female": 0.7023067,
    "10yr_ascvd_male": 0.7128741,
    "10yr_hf_female": 0.884209,
    "10yr_hf_male": 0.9095703,
    "30yr_cvd_female": 0.5073749,
    "30yr_cvd_male": 0.4427595,
    "30yr_ascvd_female": 0.4386739,
    "30yr_ascvd_male": 0.3743566,
    "30yr_hf_female": 0.5927507,
    "30yr_hf_male": 0.5478829
}

# Function to calculate age-derived value
def calculate_age_derived_value(time_horizon, condition, gender, age):
    age_derived = (age - 55) / 10
    key = f"{time_horizon}_{condition}_{gender}"

    if key not in age_coefficients:
        raise ValueError(f"Invalid combination: {key}")

    coefficient = age_coefficients[key]
    age_value = age_derived * coefficient

    return age_value

# Calculate age value
age_value = calculate_age_derived_value(time_horizon, condition, gender, age)
age_derived = (age - 55) / 10

# Print result
#print(f"Age derived for {gender} with {condition} ({time_horizon}): {age_derived:.4f}")
#print(f"Age value for {gender} with {condition} ({time_horizon}): {age_value:.4f}")


# Dictionary of coefficients
age_squared_coefficients = {
    "10yr_cvd_female": 0,
    "10yr_cvd_male": 0,
    "10yr_ascvd_female": 0,
    "10yr_ascvd_male": 0,
    "10yr_hf_female": 0,
    "10yr_hf_male": 0,
    "30yr_cvd_female": -0.0981751,
    "30yr_cvd_male": -0.1064108,
    "30yr_ascvd_female": -0.0921956,
    "30yr_ascvd_male": -0.0995499,
    "30yr_hf_female": -0.1028754,
    "30yr_hf_male": -0.1111928
}
def calculate_age_squared_value(time_horizon, condition, gender, age):
    age_squared_derived = ((age - 55) / 10) ** 2
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    if key not in age_squared_coefficients:
        raise ValueError(f"Invalid combination: {key}")

    coefficient = age_squared_coefficients[key]
    age_squared_value = age_squared_derived * coefficient
    return age_squared_value

# Call the function
age_squared_value = calculate_age_squared_value(time_horizon, condition, gender, age)
age_squared_derived = ((age - 55) / 10) ** 2
# Print the result
#print(f"Age derived Value: {age_squared_derived:.6f}")
#print(f"Age Squared Value: {age_squared_value:.6f}")

# Print results
print("\n=== Life's Essential 8 Summary ===")

def evaluate_cholesterol(high_cholesterol, cholesterol_treatment, total_cholesterol, HDL_cholesterol):
    # Calculate non-HDL cholesterol
    non_hdl_cholesterol = total_cholesterol - HDL_cholesterol

    # Scoring logic
    if high_cholesterol == "No":
        cholesterol_score = 100
        message = "Goal met"
    elif non_hdl_cholesterol < 130 and cholesterol_treatment in ["No", "Making lifestyle changes"]:
        cholesterol_score = 100
        message = "Goal met"
    elif high_cholesterol == "Yes" and cholesterol_treatment == "No":
        cholesterol_score = 0
        message = "Your cholesterol is impacting your risk"
    elif non_hdl_cholesterol < 130 and cholesterol_treatment == "Taking medications":
        cholesterol_score = 80
        message = "Goal met"
    elif 130 <= non_hdl_cholesterol < 160:
        if cholesterol_treatment == "Taking medications":
            cholesterol_score = 40
            message = "Discuss your cholesterol with your healthcare professional"
        else:
            cholesterol_score = 60
            message = "Discuss your cholesterol with your healthcare professional"
    elif 160 <= non_hdl_cholesterol < 190:
        if cholesterol_treatment == "Taking medications":
            cholesterol_score = 20
            message = "Discuss your cholesterol with your healthcare professional"
        else:
            cholesterol_score = 40
            message = "Discuss your cholesterol with your healthcare professional"
    elif 190 <= non_hdl_cholesterol < 220:
        if cholesterol_treatment == "Taking medications":
            cholesterol_score = 0
            message = "Your cholesterol is impacting your health risk."
        else:
            cholesterol_score = 20
            message = "Discuss your cholesterol with your healthcare professional"
    elif non_hdl_cholesterol >= 220:
        cholesterol_score = 0
        message = "Your cholesterol is impacting your health risk."
    else:
        cholesterol_score = None
        message = "Invalid input or edge case not handled."

    return cholesterol_score, non_hdl_cholesterol, message

# Call the function
cholesterol_score, non_hdl, feedback = evaluate_cholesterol(high_cholesterol, cholesterol_treatment, total_cholesterol, HDL_cholesterol)

#display the result
#print(f"Non-HDL Cholesterol: {non_hdl}")
#print(f"Cholesterol Score: {cholesterol_score}")
print(f"Cholesterol assessment: {feedback}")

# Coefficients
non_hdl_coefficients = {
    "10yr_cvd_female": 0.0062109,
    "10yr_cvd_male": 0.0534485,
    "10yr_ascvd_female": 0.0898765,
    "10yr_ascvd_male": 0.1465201,
    "10yr_hf_female": 0,
    "10yr_hf_male": 0,
    "30yr_cvd_female": 0.0162303,
    "30yr_cvd_male": 0.0629381,
    "30yr_ascvd_female": 0.0977728,
    "30yr_ascvd_male": 0.1544808,
    "30yr_hf_female": 0,
    "30yr_hf_male": 0
}

# Function to derive non-HDL cholesterol
def calculate_non_hdl_derived(non_hdl_cholesterol):
    return (non_hdl_cholesterol * 0.02586) - 3.5

# Function to calculate non-HDL value using coefficient
def calculate_non_hdl_value(time_horizon, condition, gender, non_hdl_cholesterol):
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    if key not in non_hdl_coefficients:
        raise ValueError(f"Invalid combination: {key}")

    coef = non_hdl_coefficients[key]
    non_hdl_derived_value = calculate_non_hdl_derived(non_hdl_cholesterol)
    non_hdl_value = non_hdl_derived_value * coef
    return non_hdl_value

non_hdl_derived_value = calculate_non_hdl_derived(non_hdl_cholesterol)
non_hdl_value = calculate_non_hdl_value(time_horizon, condition, gender, non_hdl_cholesterol)
#print(f"Non-HDL derived value for {gender} with {condition} ({time_horizon}): {non_hdl_derived_value:.4f}")
#print(f"Non-HDL value for {gender} with {condition} ({time_horizon}): {non_hdl_value:.4f}")

hdl_coefficients = {
    "10yr_cvd_female":-0.1547756,
    "10yr_cvd_male": -0.0911282,
    "10yr_ascvd_female": -0.1407316,
    "10yr_ascvd_male": -0.1125794,
    "10yr_hf_female": 0,
    "10yr_hf_male": 0,
    "30yr_cvd_female": -0.1617147,
    "30yr_cvd_male": -0.1015427,
    "30yr_ascvd_female": -0.1453525,
    "30yr_ascvd_male": -0.1215297,
    "30yr_hf_female": 0,
    "30yr_hf_male": 0
}
# Function to calculate derived HDL value
def calculate_hdl_derived(HDL_cholesterol):
        return ((HDL_cholesterol * 0.02586) - 1.3) / 0.3

# Function to calculate HDL value using derived value and coefficients
def calculate_hdl_value(time_horizon, condition, gender, HDL_cholesterol):
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        if key not in hdl_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coef = hdl_coefficients[key]
        derived_value = calculate_hdl_derived(HDL_cholesterol)
        value = derived_value * coef
        return value

hdl_value = calculate_hdl_value(time_horizon, condition, gender, HDL_cholesterol)
#print(f"HDL value for {gender} with {condition} ({time_horizon}): {hdl_value:.4f}")

statin_coefficients = {
    "10yr_cvd_female": -0.1556524,
    "10yr_cvd_male": -0.1538484,
    "10yr_ascvd_female": -0.0678552,
    "10yr_ascvd_male": -0.1073619,
    "10yr_hf_female": 0,
    "10yr_hf_male": 0,
    "30yr_cvd_female": -0.0768135,
    "30yr_cvd_male": -0.0407714,
    "30yr_ascvd_female": 0.0117504,
    "30yr_ascvd_male":-0.0025063,
    "30yr_hf_female": 0,
    "30yr_hf_male": 0
}
    # Function to calculate statin value
def calculate_statin_value(time_horizon, condition, gender, cholesterol_treatment):
        statin_derived = 1 if cholesterol_treatment.lower() == "taking medications" else 0
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        if key not in statin_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = statin_coefficients[key]
        statin_value = statin_derived * coefficient
        return statin_value

# Call the function
statin_val = calculate_statin_value(time_horizon, condition, gender, cholesterol_treatment)
#print(f"Statin value for {gender}, {condition}, {time_horizon}: {statin_val:.4f}")

non_hdl_statin_coefficients = {
    "10yr_cvd_female": 0.1061825,
    "10yr_cvd_male": 0.1415382,
    "10yr_ascvd_female": 0.0788187,
    "10yr_ascvd_male": 0.1034169,
    "10yr_hf_female": 0,
    "10yr_hf_male": 0,
    "30yr_cvd_female": 0.0917585,
    "30yr_cvd_male": 0.1232822,
    "30yr_ascvd_female": 0.0664311,
    "30yr_ascvd_male": 0.0886745,
    "30yr_hf_female": 0,
    "30yr_hf_male": 0
}
# Function to calculate value of non-HDL × Statin interaction
def calculate_non_hdl_statin_value(time_horizon, condition, gender, non_hdl_cholesterol, cholesterol_treatment):
    # Derived values
    non_hdl_derived = non_hdl_cholesterol * 0.02586 - 3.5
    statin_derived = 1 if cholesterol_treatment.lower() == "taking medications" else 0
    non_hdl_statin_derived = non_hdl_derived * statin_derived

    # Lookup key
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    # Check key exists
    if key not in non_hdl_statin_coefficients:
        raise ValueError(f"Invalid combination: {key}")

    coefficient = non_hdl_statin_coefficients[key]
    non_hdl_statin_value = non_hdl_statin_derived * coefficient
    return non_hdl_statin_value

# Call function
non_hdl_statin_value = calculate_non_hdl_statin_value(time_horizon, condition, gender, non_hdl_cholesterol, cholesterol_treatment)
#print(f"Non-HDL × Statin value: {value:.4f}")

age_non_hdl_coefficients = {
    "10yr_cvd_female": -0.0742271,
    "10yr_cvd_male": -0.0436455,
    "10yr_ascvd_female": -0.0535985,
    "10yr_ascvd_male": -0.0228755,
    "10yr_hf_female": 0,
    "10yr_hf_male": 0,
    "30yr_cvd_female": -0.0679131,
    "30yr_cvd_male": -0.0441334,
    "30yr_ascvd_female": -0.0492826,
    "30yr_ascvd_male": -0.0254507,
    "30yr_hf_female": 0,
    "30yr_hf_male": 0
}

# Function to calculate Age × Non-HDL value
def calculate_age_non_hdl_value(time_horizon, condition, gender, age, non_hdl_cholesterol):
        # Derived variables
        age_derived = (age - 55) / 10
        non_hdl_derived = non_hdl_cholesterol * 0.02586 - 3.5
        age_non_hdl_derived = age_derived * non_hdl_derived

        # Construct key
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        # Validate key
        if key not in age_non_hdl_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        # Lookup coefficient and calculate value
        coefficient = age_non_hdl_coefficients[key]
        age_non_hdl_value = age_non_hdl_derived * coefficient
        return age_non_hdl_value

# Calculate value
age_non_hdl_derived = ((age - 55) / 10) * ((non_hdl_cholesterol * 0.02586) - 3.5)
age_non_hdl_value = calculate_age_non_hdl_value(time_horizon, condition, gender, age, non_hdl_cholesterol)
#print(f"Age × Non-HDL derived: {age_non_hdl_derived:.4f}")
#print(f"Age × Non-HDL value: {age_non_hdl_value:.4f}")

age_hdl_coefficients = {
    "10yr_cvd_female": 0.0288245,
    "10yr_cvd_male": 0.0199549,
    "10yr_ascvd_female": 0.0291762,
    "10yr_ascvd_male": 0.0267453,
    "10yr_hf_female": 0,
    "10yr_hf_male": 0,
    "30yr_cvd_female": 0.027634,
    "30yr_cvd_male": 0.0150236,
    "30yr_ascvd_female": 0.0274011,
    "30yr_ascvd_male": 0.0218126,
    "30yr_hf_female": 0,
    "30yr_hf_male": 0
}

# Function to calculate Age × HDL value
def calculate_age_hdl_value(time_horizon, condition, gender, age, HDL_cholesterol):
        # Derived values
        age_derived = (age - 55) / 10
        hdl_derived = ((HDL_cholesterol * 0.02586) - 1.3) / 0.3
        age_hdl_derived = age_derived * hdl_derived

        # Key for coefficient lookup
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        if key not in age_hdl_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = age_hdl_coefficients[key]
        age_hdl_value = age_hdl_derived * coefficient
        return age_hdl_value

# Calculate and print Age × HDL interaction value
age_hdl_derived = ((age - 55) / 10) * (((HDL_cholesterol * 0.02586) - 1.3) / 0.3)
age_hdl_value = calculate_age_hdl_value(time_horizon, condition, gender, age, HDL_cholesterol)
#print(f"Age × HDL derived: {age_hdl_derived:.4f}")
#print(f"Age × HDL value: {age_hdl_value:.4f}")

def assess_blood_pressure(hypertension, hypertension_treatment, systolic_blood_pressure, diastolic_blood_pressure, symptoms=False):
    # Normalize inputs
    hypertension = str(hypertension).strip().capitalize()
    hypertension_treatment = str(hypertension_treatment).strip().capitalize()

    # 1. Check for hypertensive crisis first
    if systolic_blood_pressure >= 180 or diastolic_blood_pressure >= 120:
        category = "Hypertensive Crisis"
        if symptoms:
            message = "Hypertensive Crisis with Symptoms. This is a medical emergency. Call 911."
        else:
            message = "Hypertensive Crisis without Symptoms. Contact your health care professional as soon as possible."
        return 0, message, category

    # 2. Categorize based on standard blood pressure ranges
    if systolic_blood_pressure < 90 or diastolic_blood_pressure < 60:
        category = "Low blood pressure"
    elif 90 <= systolic_blood_pressure < 120 and 60 <= diastolic_blood_pressure < 80:
        category = "Normal blood pressure"
    elif 120 <= systolic_blood_pressure < 130 and diastolic_blood_pressure < 80:
        category = "Elevated blood pressure"
    elif 130 <= systolic_blood_pressure < 140 or 80 <= diastolic_blood_pressure < 90:
        category = "Hypertension Stage 1"
    elif 140 <= systolic_blood_pressure < 180 or 90 <= diastolic_blood_pressure < 120:
        category = "Hypertension Stage 2"
    else:
        category = "Unclassified blood pressure"

    # 3. Scoring and message based on diagnosis and treatment
    if hypertension == "No":
        if systolic_blood_pressure < 120 and diastolic_blood_pressure < 80 and hypertension_treatment in ["No", "Making lifestyle changes"]:
            blood_pressure_score = 100
            message = "Blood pressure goal met"
        elif 120 <= systolic_blood_pressure < 130 and diastolic_blood_pressure < 80:
             blood_pressure_score = 75
             message = "Your blood pressure is elevated"
        elif 130 <= systolic_blood_pressure < 140 and 80 <= diastolic_blood_pressure < 90:
            if hypertension_treatment == "Taking medications":
                 blood_pressure_score = 30
            else:
                 blood_pressure_score = 50
            message = "You are in hypertension stage 1"
        elif 140 <= systolic_blood_pressure < 160 and 90 <= diastolic_blood_pressure < 100:
             blood_pressure_score = 25 if hypertension_treatment != "Taking medications" else 5
             message = "Your blood pressure is increasing your health risk"
        elif systolic_blood_pressure >= 160 and diastolic_blood_pressure >= 100:
             blood_pressure_score = 0
             message = "Your blood pressure is increasing your health risk"
        else:
             blood_pressure_score = 100
             message = "Blood pressure goal met"

    elif hypertension == "Yes":
        if hypertension_treatment in ["Taking medications", "Making lifestyle changes"]:
             blood_pressure_score = 50
             message = "You are on guideline directed medical therapy for hypertension"
        elif hypertension_treatment == "No":
             blood_pressure_score = 0
             message = "Your blood pressure is increasing your health risk"
        else:
             blood_pressure_score = 50
             message = "You are on guideline directed medical therapy for hypertension"

    else:
            blood_pressure_score = 0
            message = "Unknown hypertension status"

    return  blood_pressure_score, message, category

# Call function
blood_pressure_score, feedback, category = assess_blood_pressure(
        hypertension,
        hypertension_treatment,
        systolic_blood_pressure,
        diastolic_blood_pressure,
        symptoms
)

#print(f"Score: { blood_pressure_score}")
print(f"Blood pressure assessment: {category} and {feedback}")

min_sbp_coefficients = {
    "10yr_cvd_female": -0.1933123,
    "10yr_cvd_male": -0.4921973,
    "10yr_ascvd_female": -0.0256648,
    "10yr_ascvd_male": -0.3387216,
    "10yr_hf_female": -0.421474,
    "10yr_hf_male": -0.6765184,
    "30yr_cvd_female": -0.1111241,
    "30yr_cvd_male": -0.2542326,
    "30yr_ascvd_female": 0.0590925,
    "30yr_ascvd_male": -0.1083968,
    "30yr_hf_female": -0.3593781,
    "30yr_hf_male": -0.4547346
}

# Derived function for min SBP
def calculate_min_sbp_derived(systolic_blood_pressure):
    return (min(systolic_blood_pressure, 110) - 110) / 20
calculate_min_sbp_value = calculate_min_sbp_derived(systolic_blood_pressure)
#print(f"Min SBP derived value: {calculate_min_sbp_value:.4f}")

# Final function to calculate min_sbp_value
def calculate_min_sbp_value(time_horizon, condition, gender, systolic_blood_pressure):
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    if key not in min_sbp_coefficients:
        raise ValueError(f"Invalid combination: {key}")

    coef = min_sbp_coefficients[key]
    derived_value = calculate_min_sbp_derived(systolic_blood_pressure)
    min_sbp_value = derived_value * coef
    return min_sbp_value

# Calculate and print
min_sbp_val = calculate_min_sbp_value(time_horizon, condition, gender, systolic_blood_pressure)
#print(f"Min SBP value: {min_sbp_val:.4f}")

max_sbp_coefficients = {
    "10yr_cvd_female": 0.3071217,
    "10yr_cvd_male": 0.2972415,
    "10yr_ascvd_female": 0.314511,
    "10yr_ascvd_male": 0.2980252,
    "10yr_hf_female": 0.3002919,
    "10yr_hf_male": 0.3111651,
    "30yr_cvd_female": 0.282946,
    "30yr_cvd_male": 0.2549679,
    "30yr_ascvd_female": 0.2862862,
    "30yr_ascvd_male": 0.2555179,
    "30yr_hf_female": 0.2628556,
    "30yr_hf_male": 0.2527602
}

# Derived function for max SBP
def calculate_max_sbp_derived(systolic_blood_pressure):
    return (max(systolic_blood_pressure, 110) - 130) / 20

calculate_max_sbp_value = calculate_max_sbp_derived(systolic_blood_pressure)
#print(f"Max SBP derived value: {calculate_max_sbp_value:.4f}")

# Final function to calculate max_sbp_value
def calculate_max_sbp_value(time_horizon, condition, gender, systolic_blood_pressure):
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    if key not in max_sbp_coefficients:
        raise ValueError(f"Invalid combination: {key}")

    coef = max_sbp_coefficients[key]
    derived_value = calculate_max_sbp_derived(systolic_blood_pressure)
    value = derived_value * coef
    return value

max_sbp_val = calculate_max_sbp_value(time_horizon, condition, gender, systolic_blood_pressure)
#print(f"Max SBP value: {max_sbp_val:.4f}")

bptreat_coefficients = {
    "10yr_cvd_female": 0.3034892,
    "10yr_cvd_male": 0.2508052,
    "10yr_ascvd_female": 0.2133861,
    "10yr_ascvd_male": 0.1686621,
    "10yr_hf_female": 0.3313614,
    "10yr_hf_male": 0.2570964,
    "30yr_cvd_female": 0.2872416,
    "30yr_cvd_male": 0.1979729,
    "30yr_ascvd_female": 0.1840085,
    "30yr_ascvd_male": 0.1120322,
    "30yr_hf_female": 0.3219386,
    "30yr_hf_male": 0.220666
}

    # Function to calculate bptreat_value
def calculate_bptreat_value(time_horizon, condition, gender, hypertension_treatment):
        bptreat_derived = 1 if hypertension_treatment == "Taking medications" else 0
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        if key not in bptreat_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = bptreat_coefficients[key]
        bptreat_value = bptreat_derived * coefficient
        return bptreat_value

# Calculate and display result
bptreat_value = calculate_bptreat_value(time_horizon, condition, gender, hypertension_treatment)
#print(f"BPTreat Value: {bptreat_value:.4f}")

sbp_bptreat_coefficients = {
    "10yr_cvd_female": -0.0667026,
    "10yr_cvd_male": -0.0474695,
    "10yr_ascvd_female": -0.0451416,
    "10yr_ascvd_male": -0.0381038,
    "10yr_hf_female": -0.1002304,
    "10yr_hf_male": -0.0591177,
    "30yr_cvd_female": -0.0557282,
    "30yr_cvd_male": -0.0365522,
    "30yr_ascvd_female": -0.0331945,
    "30yr_ascvd_male": -0.0256116,
    "30yr_hf_female": -0.0880321,
    "30yr_hf_male": -0.0436769
}

# Function to calculate SBP × BPTreat interaction value
def calculate_sbp_bptreat_value(time_horizon, condition, gender, systolic_blood_pressure, hypertension_treatment):
        max_sbp_derived = (max(systolic_blood_pressure, 110) - 130) / 20
        bptreat_derived = 1 if hypertension_treatment == "Taking medications" else 0
        sbp_bptreat_derived = max_sbp_derived * bptreat_derived

        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        if key not in sbp_bptreat_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = sbp_bptreat_coefficients[key]
        sbp_bptreat_value = sbp_bptreat_derived * coefficient
        return sbp_bptreat_value

# Compute and display result
sbp_bptreat_val = calculate_sbp_bptreat_value(time_horizon, condition, gender, systolic_blood_pressure, hypertension_treatment)
#print(f"SBP × BPTreat Value: {sbp_bptreat_val:.4f}")

age_sbp_coefficients = {
    "10yr_cvd_female": -0.0875188,
    "10yr_cvd_male": -0.1022686,
    "10yr_ascvd_female": -0.0961839,
    "10yr_ascvd_male": -0.0897449,
    "10yr_hf_female": -0.0845363,
    "10yr_hf_male": -0.1219056,
    "30yr_cvd_female": -0.0907755,
    "30yr_cvd_male": -0.1046657,
    "30yr_ascvd_female": -0.0964709,
    "30yr_ascvd_male": -0.0869146,
    "30yr_hf_female": -0.0863132,
    "30yr_hf_male": -0.1168376
}

# Function to calculate Age × SBP interaction value
def calculate_age_sbp_value(time_horizon, condition, gender, age, systolic_blood_pressure):
        # Derived values
        age_derived = (age - 55) / 10
        max_sbp_derived = (max(systolic_blood_pressure, 110) - 130) / 20
        age_sbp_derived = age_derived * max_sbp_derived

        # Construct key
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        # Validate and calculate
        if key not in age_sbp_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = age_sbp_coefficients[key]
        age_sbp_value = age_sbp_derived * coefficient
        return age_sbp_value

# Calculate and print
age_sbp_value = calculate_age_sbp_value(time_horizon, condition, gender, age, systolic_blood_pressure)
#print(f"Age × SBP Value: {age_sbp_value:.6f}")

def evaluate_glucose(diabetes, diabetes_treatment, fasting_blood_sugar, A1c):
    # Normalize text input (optional for safety)
    diabetes = diabetes.strip().capitalize()
    diabetes_treatment = diabetes_treatment.strip().capitalize()

    glucose_score = None
    message = ""

    # Case 1: No diabetes and within normal glucose range
    if diabetes == "No" and (fasting_blood_sugar < 100 or A1c < 5.7):
        glucose_score = 100
        message = "Glucose goal met"

    # Case 2: Diabetes and on treatment
    elif diabetes == "Yes" and diabetes_treatment in ["Taking medications", "Making lifestyle changes"]:
        if A1c < 7:
            glucose_score = 40
            message = "Diabetes goal met"
        elif 7 <= A1c < 8:
            glucose_score = 30
            message = "Your A1c is high"
        elif 8 <= A1c < 9:
            glucose_score = 20
            message = "Your A1c is high"
        elif 9 <= A1c < 10:
            glucose_score = 10
            message = "Your A1c is high"
        elif A1c >= 10:
            glucose_score = 0
            message = "Your A1c is high"
        else:
            glucose_score = 50
            message = "Diabetes goal met"

    # Case 3: Diabetes but not on treatment
    elif diabetes == "Yes" and diabetes_treatment == "No":
        glucose_score = 0
        message = "Diabetes will increase your health risk"

    # Case 4: No diabetes but elevated fasting glucose or A1c in prediabetic range
    elif diabetes == "No" and ((100 <= fasting_blood_sugar <= 125) or (5.7 <= A1c < 6.4)):
        glucose_score = 60
        message = "Your glucose level is high"

    # Case 5: No diabetes but glucose clearly in diabetic range
    elif diabetes == "No" and (fasting_blood_sugar > 125 or A1c >= 6.4):
        glucose_score = 40
        message = "Your glucose level is high"

    # Fallback
    else:
        glucose_score = None
        message = "Unable to determine glucose score from inputs"

    return glucose_score, message

# Call the function
glucose_score, feedback = evaluate_glucose(diabetes, diabetes_treatment, fasting_blood_sugar, A1c)
# Display the result
#print(f"Glucose Score: {glucose_score}")
print(f"Glucose assessment: {feedback}")


diabetes_coefficients = {
    "10yr_cvd_female": 0.496753,
    "10yr_cvd_male": 0.4527054,
    "10yr_ascvd_female": 0.4799217,
    "10yr_ascvd_male": 0.399583,
    "10yr_hf_female": 0.6170359,
    "10yr_hf_male": 0.5535052,
    "30yr_cvd_female": 0.4004069,
    "30yr_cvd_male": 0.333835,
    "30yr_ascvd_female": 0.3669136,
    "30yr_ascvd_male": 0.2696998,
    "30yr_hf_female": 0.5113472,
    "30yr_hf_male": 0.4385384
}

# Helper function to derive binary diabetes status
def calculate_diabetes_derived(diabetes):
        return 1 if diabetes.strip().lower() == "yes" else 0

# Main function to calculate diabetes value
def calculate_diabetes_value(diabetes, time_horizon, condition, gender):
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        if key not in diabetes_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = diabetes_coefficients[key]
        derived = calculate_diabetes_derived(diabetes)
        diabetes_value = derived * coefficient
        return diabetes_value

diabetes_value = calculate_diabetes_value(diabetes, time_horizon, condition, gender)
#print(f"Diabetes Value: {diabetes_value:.6f}")

age_diabetes_coefficients = {
    "10yr_cvd_female": -0.2267102,
    "10yr_cvd_male": -0.1762507,
    "10yr_ascvd_female": -0.2001466,
    "10yr_ascvd_male": -0.1497464,
    "10yr_hf_female":-0.2989062,
    "10yr_hf_male": -0.2437577,
    "30yr_cvd_female": -0.2702118,
    "30yr_cvd_male": -0.2116113,
    "30yr_ascvd_female": -0.2279648,
    "30yr_ascvd_male": -0.165745,
    "30yr_hf_female": -0.3425359,
    "30yr_hf_male": -0.2730055
}

# Function to calculate age × diabetes derived value and its coefficient-weighted value
def calculate_age_diabetes_value(time_horizon, condition, gender, age, diabetes):
        # Derived values
        age_derived = (age - 55) / 10
        diabetes_derived = 1 if diabetes.strip().lower() == "yes" else 0
        age_diabetes_derived = age_derived * diabetes_derived

        # Build key for coefficient lookup
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        # Validate key
        if key not in age_diabetes_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        # Calculate value
        coefficient = age_diabetes_coefficients[key]
        age_diabetes_value = age_diabetes_derived * coefficient
        return age_diabetes_value

age_diabetes_value = calculate_age_diabetes_value(time_horizon, condition, gender, age, diabetes)
#print(f"Age × Diabetes Value: {age_diabetes_value:.6f}")

A1c_glucose_derived_coefficients = {
    "10yr_cvd_female": 0.1412555,
    "10yr_cvd_male": 0.1048297,
    "10yr_ascvd_female": 0.1410572,
    "10yr_ascvd_male": 0.1092726,
    "10yr_hf_female": 0.1614911,
    "10yr_hf_male": 0.1234088,
    "30yr_cvd_female": 0.0975598,
    "30yr_cvd_male": 0.063409,
    "30yr_ascvd_female": 0.1002615,
    "30yr_ascvd_male": 0.0722905,
    "30yr_hf_female": 0.1138832,
    "30yr_hf_male": 0.0804844
}
A1c_diabetes_derived_coefficients = {
    "10yr_cvd_female": 0.1298513,
    "10yr_cvd_male": 0.1165698,
    "10yr_ascvd_female": 0.123192,
    "10yr_ascvd_male": 0.101282,
    "10yr_hf_female": 0.176668,
    "10yr_hf_male": 0.148297,
    "30yr_cvd_female": 0.0925285,
    "30yr_cvd_male": 0.0676202,
    "30yr_ascvd_female": 0.0794709,
    "30yr_ascvd_male": 0.0501422,
    "30yr_hf_female": 0.1378342,
    "30yr_hf_male": 0.0985062
}

missing_A1c_derived_coefficients = {
    "10yr_cvd_female": -0.0031658,
    "10yr_cvd_male": -0.0230072,
    "10yr_ascvd_female": 0.005866,
    "10yr_ascvd_male": 0.0652944,
    "10yr_hf_female": -0.0010583,
    "10yr_hf_male": -0.0234637,
    "30yr_cvd_female":0.0101713,
    "30yr_cvd_male": 0.0038783,
    "30yr_ascvd_female": 0.017301,
    "30yr_ascvd_male": 0.0114945,
    "30yr_hf_female": 0.0138979,
    "30yr_hf_male": 0.0022806
}
def calculate_A1c_glucose_derived_value(time_horizon, condition, gender, A1c, diabetes):
    # Construct key
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    # Determine diabetes_derived from "Yes"/"No" (case-insensitive)
    diabetes_derived = 1 if str(diabetes).strip().lower() == "yes" else 0

    # Safely attempt to convert A1c to float
    try:
        A1c = float(A1c)
    except (TypeError, ValueError):
        A1c = None

    # If A1c is missing, use default coefficient
    if A1c is None or (isinstance(A1c, float) and math.isnan(A1c)):
        if key not in missing_A1c_derived_coefficients:
            raise ValueError(f"Missing A1c: invalid combination for {key}")
        coefficient = missing_A1c_derived_coefficients[key]
        return 1 * coefficient

    # Otherwise, compute derived value
    if key not in A1c_glucose_derived_coefficients:
        raise ValueError(f"Invalid combination: {key}")
    coefficient = A1c_glucose_derived_coefficients[key]
    A1c_glucose_derived = (A1c - 5.3) * (1 - diabetes_derived)
    A1c_glucose_value = A1c_glucose_derived * coefficient

    return A1c_glucose_value

import math

def calculate_A1c_diabetes_derived_value(time_horizon, condition, gender, A1c, diabetes):
    # Build dictionary key
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    # Safely determine if diabetes is "yes"
    diabetes_derived = 1 if str(diabetes).strip().lower() == "yes" else 0

    # Try converting A1c to a float
    try:
        A1c = float(A1c)
    except (TypeError, ValueError):
        A1c = None

    # Handle missing A1c
    if A1c is None or (isinstance(A1c, float) and math.isnan(A1c)):
        if key not in missing_A1c_derived_coefficients:
            raise ValueError(f"Missing A1c: invalid combination for {key}")
        coefficient = missing_A1c_derived_coefficients[key]
        return 1 * coefficient

    # Handle valid A1c
    if key not in A1c_diabetes_derived_coefficients:
        raise ValueError(f"Invalid combination: {key}")
    coefficient = A1c_diabetes_derived_coefficients[key]
    A1c_diabetes_derived = (A1c - 5.3) * diabetes_derived
    A1c_diabetes_value = A1c_diabetes_derived * coefficient

    return A1c_diabetes_value

#A1c = None  # or A1c = 7.2
#diabetes = "Yes"

A1c_glucose_value = calculate_A1c_glucose_derived_value(time_horizon, condition, gender, A1c, diabetes)
A1c_diabetes_value = calculate_A1c_diabetes_derived_value(time_horizon, condition, gender, A1c, diabetes)

#print("A1c_glucose_value:", A1c_glucose_value)
#print("A1c_diabetes_value:", A1c_diabetes_value)

def evaluate_tobacco_use(tobacco_use, quit_years, second_hand_smoke):
    if tobacco_use == "Never used":
        if second_hand_smoke == "No":
            tobacco_use_score = 100
            message = "Goal met"
        elif second_hand_smoke == "Yes":
            tobacco_use_score = 80
            message = "The second hand smoke is putting your health at risk"
    elif tobacco_use == "Former smoker":
        if quit_years >= 5:
            if second_hand_smoke == "No":
                tobacco_use_score = 75
                message = "Goal met"
            elif second_hand_smoke == "Yes":
                tobacco_use_score = 55
                message = "The second hand smoke is putting your health at risk"
        elif 1 <= quit_years < 5:
            if second_hand_smoke == "No":
                tobacco_use_score = 50
                message = "Goal met"
            elif second_hand_smoke == "Yes":
                tobacco_use_score = 30
                message = "The second hand smoke is putting your health at risk"
        elif quit_years < 1:
            if second_hand_smoke == "No":
                tobacco_use_score = 25
                message = "Goal met"
            elif second_hand_smoke == "Yes":
                tobacco_use_score = 5
                message = "The second hand smoke is putting your health at risk"
    elif tobacco_use == "Current user":
        tobacco_use_score = 0
        message = "Your current smoking is a health risk."
    else:
        tobacco_use_score = None
        message = "Invalid input"

    return tobacco_use_score, message

# Call the function

tobacco_use_score, feedback = evaluate_tobacco_use(tobacco_use, quit_years, second_hand_smoke)

# Display result
#print(f"Tobacco Use: {tobacco_use}")
#print(f"Tobacco Use Score: {tobacco_use_score}")
print(f"Tobacco assessment: {feedback}")

smoking_coefficients = {
    "10yr_cvd_female": 0.466605,
    "10yr_cvd_male": 0.3726641,
    "10yr_ascvd_female": 0.4062049,
    "10yr_ascvd_male": 0.3379111,
    "10yr_hf_female": 0.5380269,
    "10yr_hf_male": 0.4326811,
    "30yr_cvd_female":0.2918701,
    "30yr_cvd_male": 0.1873833,
    "30yr_ascvd_female": 0.2354695,
    "30yr_ascvd_male": 0.1628432,
    "30yr_hf_female": 0.347344,
    "30yr_hf_male": 0.2397952
}

def calculate_smoking_value(time_horizon, condition, gender, tobacco_use):
    # Derived value: 1 if current smoker, else 0
    smoking_derived = 1 if tobacco_use.strip().lower() == "current user" else 0

    # Build key for coefficient lookup
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    # Validate key
    if key not in smoking_coefficients:
        raise ValueError(f"Invalid combination: {key}")

    # Lookup coefficient and compute final value
    coefficient = smoking_coefficients[key]
    smoking_value = smoking_derived * coefficient
    return smoking_value

smoking_value = calculate_smoking_value(time_horizon, condition, gender, tobacco_use)
#print(f"Smoking Value: {smoking_value:.6f}")

age_smoking_coefficients = {
    "10yr_cvd_female": -0.0676125,
    "10yr_cvd_male": -0.0715873,
    "10yr_ascvd_female": -0.0586472,
    "10yr_ascvd_male": -0.077206,
    "10yr_hf_female": -0.1111354,
    "10yr_hf_male": -0.105363,
    "30yr_cvd_female": -0.1373216,
    "30yr_cvd_male": -0.1277905,
    "30yr_ascvd_female": -0.120405,
    "30yr_ascvd_male": -0.1244714,
    "30yr_hf_female": -0.181405,
    "30yr_hf_male": -0.1573691
}

def calculate_age_smoking_value(time_horizon, condition, gender, age, tobacco_use):
        # Derived values
        age_derived = (age - 55) / 10
        smoking_derived = 1 if tobacco_use.lower() == "current user" else 0
        age_smoking_derived = age_derived * smoking_derived

        # Construct key
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        # Validate and get coefficient
        if key not in age_smoking_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = age_smoking_coefficients[key]
        age_smoking_value = age_smoking_derived * coefficient
        return age_smoking_value

# Calculate and print
age_smoking_value = calculate_age_smoking_value(time_horizon, condition, gender, age, tobacco_use)
#print(f"Age-Smoking Value: {age_smoking_value:.6f}")

def evaluate_weight(weight, height):
    # Calculate BMI
    #BMI = weight / (height / 100) ** 2

    # Evaluate weight score based on BMI
    if BMI < 25:
        weight_score = 100
        message = "Weight goal met"
    elif 25 <= BMI < 30:
        weight_score = 70
        message = "Your should consider your weight as an area to focus on"
    elif 30 <= BMI < 35:
        weight_score = 30
        message = "Your weight is impacting your health"
    elif 35 <= BMI < 40:
        weight_score = 15
        message = "Your weight is impacting your health"
    elif BMI >= 40:
        weight_score = 0
        message = "Your weight is impacting your health."
    else:
        weight_score = None
        message = "Invalid input"

    return weight_score, BMI, message

# call the function
weight_score, bmi, feedback = evaluate_weight(weight, height)

# Display the result
#print(f"BMI: {bmi:.1f}")
#print(f"Weight Score: {weight_score}")
print(f"Weight assessment: {feedback}")

min_bmi_coefficients = {
    "10yr_cvd_female": 0,
    "10yr_cvd_male": 0,
    "10yr_ascvd_female": 0,
    "10yr_ascvd_male": 0,
    "10yr_hf_female": -0.0191335,
    "10yr_hf_male": -0.0854286,
    "30yr_cvd_female": 0,
    "30yr_cvd_male": 0,
    "30yr_ascvd_female": 0,
    "30yr_ascvd_male": 0,
    "30yr_hf_female": 0.0564656,
    "30yr_hf_male": 0.0640931
}

def calculate_min_bmi_value(time_horizon, condition, gender, BMI):
        # Derived value
        min_bmi_derived = (min(BMI, 30) - 25) / 5

        # Key for coefficient lookup
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        # Validate and retrieve coefficient
        if key not in min_bmi_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = min_bmi_coefficients[key]
        min_bmi_value = min_bmi_derived * coefficient
        return min_bmi_value

# Calculate value
min_bmi_value = calculate_min_bmi_value(time_horizon, condition, gender, BMI)
#print(f"Min BMI Value: {min_bmi_value:.6f}")

max_bmi_coefficients = {
    "10yr_cvd_female": 0,
    "10yr_cvd_male": 0,
    "10yr_ascvd_female": 0,
    "10yr_ascvd_male": 0,
    "10yr_hf_female": 0.2764302,
    "10yr_hf_male": 0.3551736,
    "30yr_cvd_female": 0,
    "30yr_cvd_male": 0,
    "30yr_ascvd_female": 0,
    "30yr_ascvd_male": 0,
    "30yr_hf_female": 0.2363857,
    "30yr_hf_male": 0.2643081
}
def calculate_max_bmi_value(time_horizon, condition, gender, BMI):
        # Derived value
        max_bmi_derived = (max(BMI, 30) - 30) / 5

        # Create the coefficient key
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        # Validate and apply coefficient
        if key not in max_bmi_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = max_bmi_coefficients[key]
        max_bmi_value = max_bmi_derived * coefficient
        return max_bmi_value

max_bmi_value = calculate_max_bmi_value(time_horizon, condition, gender, BMI)
#print(f"Max BMI Value: {max_bmi_value:.6f}")

age_bmi_coefficients = {
    "10yr_cvd_female": 0,
    "10yr_cvd_male": 0,
    "10yr_ascvd_female": 0,
    "10yr_ascvd_male": 0,
    "10yr_hf_female": 0.0008104,
    "10yr_hf_male": 0.0037907,
    "30yr_cvd_female": 0,
    "30yr_cvd_male": 0,
    "30yr_ascvd_female": 0,
    "30yr_ascvd_male": 0,
    "30yr_hf_female": 0.0031285,
    "30yr_hf_male": -0.0174998
}
def calculate_age_bmi_value(time_horizon, condition, gender, age, BMI):
        # Derived values
        age_derived = (age - 55) / 10
        max_bmi_derived = (max(BMI, 30) - 30) / 5
        age_bmi_derived = age_derived * max_bmi_derived

        # Construct key
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        # Validate and get coefficient
        if key not in age_bmi_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = age_bmi_coefficients[key]
        age_bmi_value = age_bmi_derived * coefficient
        return age_bmi_value

age_bmi_value = calculate_age_bmi_value(time_horizon, condition, gender, age, BMI)
#print("age_bmi_value:", round(age_bmi_value, 5))

#PREVENT values not already defined
#egfr = 90 #15-150
min_egfr_coefficients = {
    "10yr_cvd_female": 0.4780697,
    "10yr_cvd_male": 0.3886854,
    "10yr_ascvd_female": 0.3847744,
    "10yr_ascvd_male": 0.2582604,
    "10yr_hf_female": 0.5975847,
    "10yr_hf_male": 0.5102245,
    "30yr_cvd_female": 0.1017102,
    "30yr_cvd_male": 0.0246102,
    "30yr_ascvd_female": 0.0354338,
    "30yr_ascvd_male": -0.077507,
    "30yr_hf_female": 0.1971295,
    "30yr_hf_male": 0.1354588
}

def calculate_min_egfr_value(time_horizon, condition, gender, egfr):
        min_egfr_derived = (min(egfr, 60) - 60) / -15
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        if key not in min_egfr_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = min_egfr_coefficients[key]
        min_egfr_value = min_egfr_derived * coefficient
        return min_egfr_value

min_egfr_value = calculate_min_egfr_value(time_horizon, condition, gender, egfr)
#print("min_egfr_value:", round(min_egfr_value, 5))

max_egfr_coefficients = {
    "10yr_cvd_female": 0.0529077,
    "10yr_cvd_male": 0.0081661,
    "10yr_ascvd_female": 0.0495174,
    "10yr_ascvd_male": 0.0147769,
    "10yr_hf_female": 0.0654197,
    "10yr_hf_male": 0.015472,
    "30yr_cvd_female": 0.0622643,
    "30yr_cvd_male": 0.0552014,
    "30yr_ascvd_female": 0.0573093,
    "30yr_ascvd_male":0.0583407,
    "30yr_hf_female": 0.0735227,
    "30yr_hf_male": 0.0570689
}

def calculate_max_egfr_value(time_horizon, condition, gender, egfr):
        max_egfr_derived = (max(egfr, 60) - 90) / -15
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        if key not in max_egfr_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coefficient = max_egfr_coefficients[key]
        max_egfr_value = max_egfr_derived * coefficient
        return max_egfr_value

max_egfr_value = calculate_max_egfr_value(time_horizon, condition, gender, egfr)
#print("max_egfr_value:", round(max_egfr_value, 5))

age_egfr_coefficients = {
    "10yr_cvd_female": -0.1493231,
    "10yr_cvd_male": -0.1428668,
    "10yr_ascvd_female": -0.1537791,
    "10yr_ascvd_male": -0.1198368,
    "10yr_hf_female": -0.1666635,
    "10yr_hf_male": -0.1660207,
    "30yr_cvd_female": -0.1255864,
    "30yr_cvd_male": -0.0955922,
    "30yr_ascvd_female": -0.1157635,
    "30yr_ascvd_male": -0.0624552,
    "30yr_hf_female": -0.1356989,
    "30yr_hf_male": -0.1128676
}

def calculate_age_egfr_value(time_horizon, condition, gender, age, egfr):
        # Derived components
        age_derived = (age - 55) / 10
        max_egfr_derived = (max(egfr, 60) - 90) / -15
        age_egfr_derived = age_derived * max_egfr_derived

        # Select coefficient
        key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

        if key not in age_egfr_coefficients:
            raise ValueError(f"Invalid combination: {key}")

        coef = age_egfr_coefficients[key]
        age_egfr_value = age_egfr_derived * coef

        return age_egfr_value

age_egfr_value = calculate_age_egfr_value(time_horizon, condition, gender, age, egfr)
#print("age_egfr_value:", round(age_egfr_value, 5))

#uacr = 40 #.1-25000
uacr_derived_coefficients = {
    "10yr_cvd_female": 0.1645922,
    "10yr_cvd_male": 0.1772853,
    "10yr_ascvd_female": 0.1371824,
    "10yr_ascvd_male": 0.1375837,
    "10yr_hf_female": 0.1948135,
    "10yr_hf_male": 0.2164607,
    "30yr_cvd_female": 0.1028065,
    "30yr_cvd_male": 0.0894596,
    "30yr_ascvd_female": 0.0810739,
    "30yr_ascvd_male": 0.0560171,
    "30yr_hf_female": 0.1273306,
    "30yr_hf_male": 0.1233486
}

missing_uacr_derived_coefficients = {
    "10yr_cvd_female": -0.0006181,
    "10yr_cvd_male": 0.1095674,
    "10yr_ascvd_female": 0.0061613,
    "10yr_ascvd_male": 0.0652944,
    "10yr_hf_female": 0.0395368,
    "10yr_hf_male": 0.1702805,
    "30yr_cvd_female": -0.0006181,
    "30yr_cvd_male": 0.0710124,
    "30yr_ascvd_female": -0.0147785,
    "30yr_ascvd_male": 0.0252244,
    "30yr_hf_female": 0.0167008,
    "30yr_hf_male": 0.1274796
}

def calculate_uacr_value(time_horizon, condition, gender, uacr):
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    # Handle blank or non-numeric UACR input
    try:
        uacr = float(uacr)
    except (ValueError, TypeError):
        uacr = None

    # Check for missing or invalid UACR
    if uacr is None or uacr <= 0 or (isinstance(uacr, float) and math.isnan(uacr)):
        if key not in missing_uacr_derived_coefficients:
            raise ValueError(f"Invalid combination for missing UACR: {key}")
        coefficient = missing_uacr_derived_coefficients[key]
        uacr_derived = 1
    else:
        if key not in uacr_derived_coefficients:
            raise ValueError(f"Invalid combination: {key}")
        coefficient = uacr_derived_coefficients[key]
        uacr_derived = math.log(uacr)

    uacr_value = uacr_derived * coefficient
    return uacr_value

try:
    uacr_value = calculate_uacr_value(time_horizon, condition, gender, uacr)
    #print(f"uacr_value: {uacr_value:.6f}")
except ValueError as e:
    print(str(e))

#sdi = 5 #1-10
min_sdi_derived_coefficients = {
    "10yr_cvd_female": 0.1361989,
    "10yr_cvd_male": 0.0802431,
    "10yr_ascvd_female": 0.1413965,
    "10yr_ascvd_male": 0.0651121,
    "10yr_hf_female": 0.1213034,
    "10yr_hf_male": 0.1106372,
    "30yr_cvd_female": 0.1067741,
    "30yr_cvd_male": 0.0256704,
    "30yr_ascvd_female": 0.1107632,
    "30yr_ascvd_male": 0.015675,
    "30yr_hf_female": 0.0847634,
    "30yr_hf_male": 0.057746
}

max_sdi_derived_coefficients = {
    "10yr_cvd_female": 0.2261596,
    "10yr_cvd_male": 0.275073,
    "10yr_ascvd_female": 0.228136,
    "10yr_ascvd_male": 0.2676683,
    "10yr_hf_female": 0.2314147,
    "10yr_hf_male": 0.3371204,
    "30yr_cvd_female": 0.1853138,
    "30yr_cvd_male": 0.1887637,
    "30yr_ascvd_female": 0.1840367,
    "30yr_ascvd_male": 0.1864231,
    "30yr_hf_female": 0.18397,
    "30yr_hf_male": 0.2446441
}

missing_sdi_derived_coefficients = {
    "10yr_cvd_female": 0.1804508,
    "10yr_cvd_male": 0.144759,
    "10yr_ascvd_female": 0.1588908,
    "10yr_ascvd_male": 0.1388492,
    "10yr_hf_female": 0.1819138,
    "10yr_hf_male": 0.1694628,
    "30yr_cvd_female": 0.1567115,
    "30yr_cvd_male": 0.089241,
    "30yr_ascvd_female": 0.1308962,
    "30yr_ascvd_male": 0.0845697,
    "30yr_hf_female": 0.1485802,
    "30yr_hf_male": 0.1076782
}

def calculate_min_sdi_derived_value(time_horizon, condition, gender, sdi):
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    if sdi is None or sdi == '' or (isinstance(sdi, float) and math.isnan(sdi)):
        if key not in missing_sdi_derived_coefficients:
            raise ValueError(f"Invalid combination for missing SDI: {key}")
        coefficient = missing_sdi_derived_coefficients[key]
        min_sdi_derived = 1  # Fixed value when missing
    else:
        if key not in min_sdi_derived_coefficients:
            raise ValueError(f"Invalid combination: {key}")
        min_sdi_derived = 1 if 4 <= sdi < 7 else 0
        coefficient = min_sdi_derived_coefficients[key]

    min_sdi_value = min_sdi_derived * coefficient
    return min_sdi_value

def calculate_max_sdi_derived_value(time_horizon, condition, gender, sdi):
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"

    if sdi is None or sdi == '' or (isinstance(sdi, float) and math.isnan(sdi)):
        if key not in missing_sdi_derived_coefficients:
            raise ValueError(f"Invalid combination for missing SDI: {key}")
        coefficient = missing_sdi_derived_coefficients[key]
        max_sdi_derived = 1  # Fixed value when missing
    else:
        if key not in max_sdi_derived_coefficients:
            raise ValueError(f"Invalid combination: {key}")
        max_sdi_derived = 1 if sdi >= 7 else 0
        coefficient = max_sdi_derived_coefficients[key]

    max_sdi_value = max_sdi_derived * coefficient
    return max_sdi_value

min_sdi_value = calculate_min_sdi_derived_value(time_horizon, condition, gender, sdi)
max_sdi_value = calculate_max_sdi_derived_value(time_horizon, condition, gender, sdi)

#print(f"min_sdi_value: {min_sdi_value:.6f}")
#print(f"max_sdi_value: {max_sdi_value:.6f}")

#MCL section
def calculate_physical_activity_score(moderate_intensity, vigorous_intensity):
    # Calculate total activity: vigorous counts double
    total_physical_activity = moderate_intensity + (vigorous_intensity * 2)

# Determine score
    if total_physical_activity >= 150:
        total_physical_activity_score = 100
        print("Activity goal met")
    elif 120 <= total_physical_activity < 150:
        total_physical_activity_score = 90
        print("Physical activity is an area to focus on")
    elif 90 <= total_physical_activity < 120:
        total_physical_activity_score = 80
        print("Physical activity is an area to focus on")
    elif 60 <= total_physical_activity < 90:
        total_physical_activity_score = 60
        print("Physical activity is an area to focus on")
    elif 30 <= total_physical_activity < 60:
        total_physical_activity_score = 40
        print("Your sedentary lifestyle is a concern")
    elif 1 <= total_physical_activity < 30:
        total_physical_activity_score = 20
        print("Your sedentary lifestyle is a concern")
    else:
        total_physical_activity_score = 0
        print("Your sedentary lifestyle is a concern")

    return total_physical_activity, total_physical_activity_score

# Call the function
total_minutes, total_physical_activity_score = calculate_physical_activity_score(moderate_intensity, vigorous_intensity)

# Display result
#print(f"Total Physical Activity (minutes): {total_minutes}")
#print(f"Be More Active Score: {total_physical_activity_score}")

# Sleep
def evaluate_sleep(sleep_hours):
    if 7 <= sleep_hours < 9:
        sleep_score = 100
        message = "Goal met"
    elif 9 <= sleep_hours < 10:
        sleep_score = 90
        message = "This is an area to work on"
    elif 6 <= sleep_hours < 7:
        sleep_score = 70
        message = "This is an area to work on"
    elif 5 <= sleep_hours < 6:
        sleep_score = 40
        message = "Your sleep is a concern"
    elif sleep_hours >= 10:
        sleep_score = 40
        message = "Your sleep is a concern"
    elif 4 <= sleep_hours < 5:
        sleep_score = 20
        message = "Your sleep is a concern"
    elif sleep_hours < 4:
        sleep_score = 0
        message = "Your sleep is a concern"
    else:
        sleep_score = None
        message = "Invalid input"

    return sleep_score, message

# Call the function
sleep_score, note = evaluate_sleep(sleep_hours)

# Display result
#print(f"Sleep Hours: {sleep_hours}")
#print(f"Sleep Score: {sleep_score}")
print(f"Sleep assessment: {note}")

# Nutrition intake (days per week or servings per day)
green_leafy_vegetables = 7
berries = 2
red_meat = 3
fish_seafood = 1
poultry = 4
beans_peas = 5
nuts = 4
full_fat_dairy = 2
butter_cream = 3
sugary_drinks = 1
vegetables = 3
fruits = 2
whole_grains = 3
olive_oil = 2
alcohol = 1
#gender = "female"
restaurant_meals = 1

def calculate_eat_better_function_score(green_leafy_vegetables, berries, red_meat, fish_seafood, poultry,beans_peas, nuts,full_fat_dairy, butter_cream, sugary_drinks, vegetables, fruits, whole_grains, olive_oil, alcohol, gender, restaurant_meals
):
    # Individual scores based on criteria
    # Green leafy vegetables
    if green_leafy_vegetables < 7:
        green_leafy_vegetables_score = 0
        message = "You are not eating enough green leafy vegetables"
    else:
        green_leafy_vegetables_score = 1
        message = "Goal met"
    #berries
    if berries < 2:
        berries_score = 0
        message = "You are not eating enough berries"
    else:    
        berries_score = 1
        message = "Goal met"
    # Red meat
    if red_meat < 3:
        red_meat_score = 0
        message = "You are eating too much red meat"
    else:
        red_meat_score = 1
        message = "Goal met"
    # Fish and seafood
    if fish_seafood < 1:
        fish_seafood_score = 0
        message = "You are not eating enough fish and seafood"
    else:
        fish_seafood_score = 1
        message = "Goal met"
    # Poultry
    if poultry < 5:
        poultry_score = 0
        message = "You are not eating enough poultry"
    else:
        poultry_score = 1
        message = "Goal met"
    # Beans and peas
    if beans_peas < 4:
        beans_peas_score = 0
        message = "You are not eating enough beans and peas"
    else:
        beans_peas_score = 1
        message = "Goal met"
    # Nuts
    if nuts < 4:
        nuts_score = 0
        message = "You are not eating enough nuts"
    else:
        nuts_score = 1
        message = "Goal met"
    # Full fat dairy
    if full_fat_dairy > 4:
        full_fat_dairy_score = 0
        message = "You are eating too much full fat dairy"
    else:
        full_fat_dairy_score = 1
        message = "Goal met"
    # Butter and cream
    if butter_cream > 5:
        butter_cream_score = 0
        message = "You are eating too much butter and cream"
    else:
        butter_cream_score = 1
        message = "Goal met"
    # Sugary drinks
    if sugary_drinks > 4:
        sugary_drinks_score = 0
        message = "You are eating too many sugary drinks"
    else:
        sugary_drinks_score = 1
        message = "Goal met"
    # Vegetables
    if vegetables < 2:
        vegetables_score = 0
        message = "You are not eating enough vegetables"
    else:
        vegetables_score = 1
        message = "Goal met"
    # Fruits
    if fruits < 1:
        fruits_score = 0
        message = "You are not eating enough fruits"
    else:
        fruits_score = 1
        message = "Goal met"
    # Whole grains
    if whole_grains < 3:
        whole_grains_score = 0
        message = "You are not eating enough whole grains"
    else:
        whole_grains_score = 1
        message = "Goal met"
    # Olive oil
    if olive_oil < 3:
        olive_oil_score = 0
        message = "You are not eating enough olive oil"
    else:
        olive_oil_score = 1
        message = "Goal met"
    # Alcohol    
    if alcohol > 2 and gender == 'Male':
        alcohol_score = 0
        message = "You are drinking too much alcohol"
    elif alcohol > 1 and gender == 'Female':
        alcohol_score = 0
    else:
        alcohol_score = 1
        message = "Goal met"
    # Restaurant meals
    if restaurant_meals > 2:
        restaurant_meals_score = 0
        message = "You are eating too many restaurant meals"
    else:    
        restaurant_meals_score = 1
        message = "Goal met"

# Total score
    eat_better_score = sum([
        green_leafy_vegetables_score, berries_score, red_meat_score, fish_seafood_score, poultry_score,
        beans_peas_score, nuts_score, full_fat_dairy_score, butter_cream_score, sugary_drinks_score,
        vegetables_score, fruits_score, whole_grains_score, olive_oil_score, alcohol_score, restaurant_meals_score
    ])

    # Scoring criteria
    if eat_better_score >= 15:
        score = 100
        message = "Eat better goal met"
    elif 12 <= eat_better_score <= 14:
        score = 80
        message = "Nutrition is something you could focus on"
    elif 8 <= eat_better_score <= 11:
        score = 50
        message = "Nutrition is something you could focus on"
    elif 4 <= eat_better_score <= 7:
        score = 25
        message = "Nutrition could be impacting your health"
    else:
        score = 0
        message = "Nutrition could be impacting your health"

    return eat_better_score, score, message

# Call the function
eat_better_score, nutrition_score, message = calculate_eat_better_function_score(
    green_leafy_vegetables, berries, red_meat, fish_seafood, poultry,
    beans_peas, nuts, full_fat_dairy, butter_cream, sugary_drinks,
    vegetables, fruits, whole_grains, olive_oil, alcohol, gender, restaurant_meals
)

#print("Eat Better Subscore:", eat_better_score)
#print("Overall Nutrition Score:", nutrition_score)
print("Nutrition assessment:", message)

# Calculate MLC score
MLC_score = (
    total_physical_activity_score/8
    + sleep_score/8
    + tobacco_use_score/8
    + weight_score/8
    + cholesterol_score/8
    + glucose_score/8
    + blood_pressure_score/8
    + nutrition_score/8
)

# Categorize MLC score
if MLC_score >= 80:
    cvh_category = "High CVH"
elif 50 <= MLC_score < 80:
    cvh_category = "Moderate CVH"
else:
    cvh_category = "Low CVH"

# Print results
print("\n=== My Life Check Summary ===")
print(f"MLC Score (out of 100): {MLC_score}")
print(f"Cardiovascular Health Status: {cvh_category}")

# Intercept dictionary
intercept_constants = {
    "10yr_cvd_female": -3.860385, "10yr_cvd_male": -3.631387,
    "10yr_ascvd_female": -4.291503, "10yr_ascvd_male": -3.969788,
    "10yr_hf_female": -4.896524, "10yr_hf_male": -4.663513,
    "30yr_cvd_female": -1.748475, "30yr_cvd_male": -1.504558,
    "30yr_ascvd_female": -2.314066, "30yr_ascvd_male": -1.985368,
    "30yr_hf_female": -2.642208, "30yr_hf_male": -2.425439
}
# Function to calculate final risk score sum
def calculate_risk_score_sum(time_horizon, condition, gender, *values):
    key = f"{time_horizon.lower()}_{condition.lower()}_{gender.lower()}"
    if key not in intercept_constants:
        raise ValueError(f"Invalid combination: {key}")
    intercept = intercept_constants[key]
    return intercept + sum(values)

# List of time horizons and conditions
time_horizons = ["10yr", "30yr"]
conditions = ["cvd", "ascvd", "hf"]

# Risk factor values to be passed as *args
component_values = (
    age_value,
    age_squared_value,
    non_hdl_value,
    hdl_value,
    statin_val,
    non_hdl_statin_value,
    age_non_hdl_value,
    age_hdl_value,
    min_sbp_val,
    max_sbp_val,
    bptreat_value,
    sbp_bptreat_val,
    age_sbp_value,
    diabetes_value,
    age_diabetes_value,
    A1c_glucose_value,
    A1c_diabetes_value,
    smoking_value,
    age_smoking_value,
    min_bmi_value,
    max_bmi_value,
    age_bmi_value,
    min_egfr_value,
    max_egfr_value,
    age_egfr_value,
    uacr_value,
    min_sdi_value,
    max_sdi_value,
)

# Loop through each combination and print the risk
print("\n=== PREVENT Summary ===")
for time_horizon in time_horizons:
    for condition in conditions:
        try:
            risk_score_sum = calculate_risk_score_sum(
                time_horizon, condition, gender, *component_values
            )
            risk_score = math.exp(risk_score_sum) / (1 + math.exp(risk_score_sum))
            print(f"PREVENT Risk for {gender}, {condition}, {time_horizon}: {risk_score * 100:.1f}%")
        except ValueError as e:
            print(str(e))
#print(f"PREVENT Risk Score Sum: {risk_score_sum}")