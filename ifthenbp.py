# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 20:22:04 2024

@author: PatrickDunn
"""

def categorize_blood_pressure(systolic, diastolic):
    if systolic < 120 and diastolic < 80:
        category = "Normal"
    elif 120 <= systolic < 130 and diastolic < 80:
        category = "Elevated"
    elif (130 <= systolic < 140) or (80 <= diastolic < 90):
        category = "Hypertension Stage 1"
    elif (140 <= systolic) or (90 <= diastolic):
        category = "Hypertension Stage 2"
    else:
        category = "Hypertensive Crisis (consult your doctor immediately)"
    return category

# Example usage:
systolic_bp = 135
diastolic_bp = 85
bp_category = categorize_blood_pressure(systolic_bp, diastolic_bp)
print(f"Blood Pressure Category: {bp_category}")

# List of heart failure symptoms and corresponding management tips
symptoms_management = {
    "Shortness of breath": "Sit up and lean forward. Use prescribed medications. Contact your healthcare provider if it persists.",
    "Swelling in legs, ankles, and feet": "Elevate your legs. Reduce salt intake. Wear compression stockings. Inform your doctor if swelling increases.",
    "Fatigue and weakness": "Rest when needed. Maintain a balanced diet. Engage in light physical activities as advised by your doctor.",
    "Rapid or irregular heartbeat": "Monitor your heart rate. Avoid stimulants like caffeine. Take medications as prescribed. Seek medical advice if symptoms worsen.",
    "Persistent cough or wheezing": "Stay hydrated. Avoid smoking and pollutants. Use cough medications as directed by your healthcare provider.",
    "Increased need to urinate at night": "Limit fluid intake in the evening. Discuss diuretics timing with your doctor. Monitor for signs of fluid retention.",
    "Difficulty concentrating or decreased alertness": "Get adequate rest. Engage in mental exercises. Discuss any concerns with your healthcare provider."
}

# Iterate through the symptoms and provide management tips
for symptom, tip in symptoms_management.items():
    print(f"Symptom: {symptom}")
    print(f"Management Tip: {tip}")
    print("-" * 50)

# Example output:
# Symptom: Shortness of breath
# Management Tip: Sit up and lean forward. Use prescribed medications. Contact your healthcare provider if it persists.
# --------------------------------------------------
# Symptom: Swelling in legs, ankles, and feet
# Management Tip: Elevate your legs. Reduce salt intake. Wear compression stockings. Inform your doctor if swelling increases.
# --------------------------------------------------
# ... (continues for all symptoms)

# Define target heart rate range for moderate intensity exercise
min_target_hr = 100
max_target_hr = 140

# Sample heart rate data (this could come from a heart rate monitor in real applications)
heart_rate_data = [95, 102, 110, 125, 138, 145, 135, 130, 120, 105, 100]

# Index to keep track of heart rate data points
index = 0

# Monitor exercise intensity
while index < len(heart_rate_data):
    current_hr = heart_rate_data[index]
    
    if current_hr < min_target_hr:
        print(f"Heart Rate: {current_hr} bpm - Increase intensity.")
    elif min_target_hr <= current_hr <= max_target_hr:
        print(f"Heart Rate: {current_hr} bpm - Maintain current intensity.")
    else:
        print(f"Heart Rate: {current_hr} bpm - Decrease intensity.")
    
    index += 1

# Example output:
# Heart Rate: 95 bpm - Increase intensity.
# Heart Rate: 102 bpm - Maintain current intensity.
# Heart Rate: 110 bpm - Maintain current intensity.
# Heart Rate: 125 bpm - Maintain current intensity.
# Heart Rate: 138 bpm - Maintain current intensity.
# Heart Rate: 145 bpm - Decrease intensity.
# Heart Rate: 135 bpm - Maintain current intensity.
# Heart Rate: 130 bpm - Maintain current intensity.
# Heart Rate: 120 bpm - Maintain current intensity.
# Heart Rate: 105 bpm - Maintain current intensity.
# Heart Rate: 100 bpm - Maintain current intensity.
