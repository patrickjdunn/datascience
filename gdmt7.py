# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 19:47:22 2024

@author: PatrickDunn
"""

import sqlite3
import pandas as pd
from datetime import datetime

class HeartFailureMonitoring:
    def __init__(self, db_name='heart_failure_monitoring.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS patients (
                                    patient_id TEXT PRIMARY KEY,
                                    name TEXT,
                                    age INTEGER
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS weight_log (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    patient_id TEXT,
                                    date TEXT,
                                    weight REAL,
                                    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS medication_adherence_log (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    patient_id TEXT,
                                    date TEXT,
                                    medication TEXT,
                                    adherence INTEGER,
                                    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS symptoms_log (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    patient_id TEXT,
                                    date TEXT,
                                    symptoms TEXT,
                                    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS scores (
                                    patient_id TEXT,
                                    score INTEGER,
                                    recheck_interval TEXT,
                                    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
                                )''')

    def add_patient(self, patient_id, name, age):
        with self.conn:
            existing_patient = self.conn.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,)).fetchone()
            if existing_patient:
                print(f"Patient with ID {patient_id} already exists.")
            else:
                self.conn.execute('INSERT INTO patients (patient_id, name, age) VALUES (?, ?, ?)', 
                                  (patient_id, name, age))
                print(f"Added patient {name} with ID {patient_id}")

    def log_weight(self, patient_id, weight):
        with self.conn:
            self.conn.execute('INSERT INTO weight_log (patient_id, date, weight) VALUES (?, ?, ?)', 
                              (patient_id, datetime.now().isoformat(), weight))
        print(f"Logged weight for patient {patient_id}: {weight} kg")

    def log_medication_adherence(self, patient_id, medication, adherence):
        with self.conn:
            self.conn.execute('INSERT INTO medication_adherence_log (patient_id, date, medication, adherence) VALUES (?, ?, ?, ?)', 
                              (patient_id, datetime.now().isoformat(), medication, adherence))
        print(f"Logged medication adherence for patient {patient_id}: {medication} - {'Adherent' if adherence else 'Non-adherent'}")

    def log_symptoms(self, patient_id, symptoms):
        with self.conn:
            self.conn.execute('INSERT INTO symptoms_log (patient_id, date, symptoms) VALUES (?, ?, ?)', 
                              (patient_id, datetime.now().isoformat(), symptoms))
        print(f"Logged symptoms for patient {patient_id}: {symptoms}")

    def get_patient_report(self, patient_id):
        patient = self.conn.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,)).fetchone()
        if patient:
            weight_log = self.conn.execute('SELECT * FROM weight_log WHERE patient_id = ?', (patient_id,)).fetchall()
            medication_adherence_log = self.conn.execute('SELECT * FROM medication_adherence_log WHERE patient_id = ?', (patient_id,)).fetchall()
            symptoms_log = self.conn.execute('SELECT * FROM symptoms_log WHERE patient_id = ?', (patient_id,)).fetchall()

            report = {
                'Weight Log': weight_log,
                'Medication Adherence Log': medication_adherence_log,
                'Symptoms Log': symptoms_log
            }
            return report
        else:
            print(f"Patient {patient_id} not found")
            return None

    def save_score(self, patient_id, score, recheck_interval):
        with self.conn:
            self.conn.execute('INSERT INTO scores (patient_id, score, recheck_interval) VALUES (?, ?, ?)', 
                              (patient_id, score, recheck_interval))
        print(f"Saved score for patient {patient_id}: {score} ({recheck_interval})")

# Initialize monitoring instance and populate with some example data
monitoring = HeartFailureMonitoring()
monitoring.add_patient('001', 'John Doe', 70)
monitoring.log_weight('001', 75.5)
monitoring.log_medication_adherence('001', 'ARNI', 1)
monitoring.log_symptoms('001', 'Shortness of breath')

# Define mappings for categorical variables
categorical_mappings = {
    'SMARTGoals': {'Set': 0, 'Not Set': 1},
    'HFSymptoms': {'Stable': 0, 'New or Worsening': 1},
    'MedicationAdherence': {'All the time': 0, 'Inconsistently': 1, 'I am not taking my medication as prescribed': 2},
    'ActionPlan': {'Following plan': 0, 'Inconsistent': 1, 'Not following plan': 2},
    'TreatmentGoal': {'At goal': 0, 'Improving, but not at goal': 1, 'Not making progress': 2},
    'GDMTStatus': {'Optimal': 0, 'Suboptimal': 1, 'Not on GDMT': 2}
}

# Create a sample DataFrame with categorical and quantitative variables
data = {
    'PatientID': ['001', '002', '003', '004'],
    'SMARTGoals': ['Set', 'Not Set', 'Set', 'Not Set'],
    'HFSymptoms': ['Stable', 'New or Worsening', 'Stable', 'New or Worsening'],
    'MedicationAdherence': ['All the time', 'Inconsistently', 'I am not taking my medication as prescribed', 'All the time'],
    'ActionPlan': ['Following plan', 'Inconsistent', 'Not following plan', 'Following plan'],
    'TreatmentGoal': ['At goal', 'Improving, but not at goal', 'Not making progress', 'At goal'],
    'GDMTStatus': ['Optimal', 'Suboptimal', 'Not on GDMT', 'Optimal'],
    'HeartRate': [72, 101, 88, 76],
    'BloodPressure': ['120/80', '140/90', '130/85', '125/82'],
    'Weight': [70.5, 85.0, 78.2, 68.3]
}

df = pd.DataFrame(data)

# Apply the mappings to convert categorical responses to numerical values
for column, mapping in categorical_mappings.items():
    df[column] = df[column].map(mapping)

# Calculate the score by summing the specified columns
df['score'] = df[['SMARTGoals', 'HFSymptoms', 'MedicationAdherence', 'ActionPlan', 'TreatmentGoal', 'GDMTStatus']].sum(axis=1)

# Create a new column for the recheck interval based on the score
def determine_recheck_interval(score):
    if score == 0:
        return 'Recheck in 4 weeks'
    elif score <= 2:
        return 'Recheck in 2 weeks'
    else:
        return 'Recheck in 1 week'

df['RecheckInterval'] = df['score'].apply(determine_recheck_interval)

# Save the scores and recheck intervals to the database
for index, row in df.iterrows():
    monitoring.save_score(row['PatientID'], row['score'], row['RecheckInterval'])

print(df)

