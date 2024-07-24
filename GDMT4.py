# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 06:38:49 2024

@author: PatrickDunn
"""

from datetime import datetime

class HeartFailureMonitoring:
    def __init__(self):
        self.patients = []

    def add_patient(self, patient_id, name, age):
        patient = {
            'patient_id': patient_id,
            'name': name,
            'age': age,
            'weight_log': [],
            'medication_adherence_log': [],
            'symptoms_log': []
        }
        self.patients.append(patient)
        print(f"Added patient {name} with ID {patient_id}")

    def log_weight(self, patient_id, weight):
        patient = self._find_patient(patient_id)
        if patient:
            log_entry = {'date': datetime.now(), 'weight': weight}
            patient['weight_log'].append(log_entry)
            print(f"Logged weight for patient {patient_id}: {weight} kg")

    def log_medication_adherence(self, patient_id, medication, adherence):
        patient = self._find_patient(patient_id)
        if patient:
            log_entry = {'date': datetime.now(), 'medication': medication, 'adherence': adherence}
            patient['medication_adherence_log'].append(log_entry)
            print(f"Logged medication adherence for patient {patient_id}: {medication} - {'Adherent' if adherence else 'Non-adherent'}")

    def log_symptoms(self, patient_id, symptoms):
        patient = self._find_patient(patient_id)
        if patient:
            log_entry = {'date': datetime.now(), 'symptoms': symptoms}
            patient['symptoms_log'].append(log_entry)
            print(f"Logged symptoms for patient {patient_id}: {symptoms}")

    def get_patient_report(self, patient_id):
        patient = self._find_patient(patient_id)
        if patient:
            report = {
                'Weight Log': patient['weight_log'],
                'Medication Adherence Log': patient['medication_adherence_log'],
                'Symptoms Log': patient['symptoms_log']
            }
            return report
        else:
            print(f"Patient {patient_id} not found")
            return None

    def _find_patient(self, patient_id):
        for patient in self.patients:
            if patient['patient_id'] == patient_id:
                return patient
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
