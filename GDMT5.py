# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 07:42:27 2024

@author: PatrickDunn
"""

import sqlite3
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

    def add_patient(self, patient_id, name, age):
        with self.conn:
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

# Example usage
monitoring = HeartFailureMonitoring()
monitoring.add_patient('001', 'John Doe', 70)
monitoring.log_weight('001', 75.5)
monitoring.log_medication_adherence('001', 'ARNI', True)
monitoring.log_symptoms('001', 'Shortness of breath')

report = monitoring.get_patient_report('001')
if report:
    print("\nPatient Report:")
    for log_type, logs in report.items():
        print(f"\n{log_type}:")
        for log in logs:
            print(log)
