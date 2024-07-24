# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 06:36:55 2024

@author: PatrickDunn
"""

class Patient:
    def __init__(self, name, age, weight, medications=None):
        self.name = name
        self.age = age
        self.weight = weight
        self.medications = medications if medications else {
            'ARNI/ACE/ARB': {'name': None, 'dose': 0},
            'Beta Blocker': {'name': None, 'dose': 0},
            'MRA': {'name': None, 'dose': 0},
            'SGLT2': {'name': None, 'dose': 0},
        }
        self.follow_up_dates = []

    def initiate_medication(self, med_class, med_name, initial_dose):
        if med_class in self.medications:
            self.medications[med_class]['name'] = med_name
            self.medications[med_class]['dose'] = initial_dose
            print(f"{self.name} initiated on {med_name} with dose {initial_dose} mg.")

    def optimize_medication(self, med_class, increment):
        if med_class in self.medications:
            self.medications[med_class]['dose'] += increment
            print(f"{self.name}'s {self.medications[med_class]['name']} dose increased to {self.medications[med_class]['dose']} mg.")

    def schedule_follow_up(self, weeks):
        from datetime import datetime, timedelta
        next_follow_up = datetime.now() + timedelta(weeks=weeks)
        self.follow_up_dates.append(next_follow_up)
        print(f"Next follow-up scheduled for {next_follow_up.strftime('%Y-%m-%d %H:%M:%S')}.")

    def display_patient_info(self):
        print(f"Patient: {self.name}, Age: {self.age}, Weight: {self.weight} kg")
        for med_class, details in self.medications.items():
            print(f"{med_class}: {details['name']} at {details['dose']} mg")
        print("Follow-up dates:", [date.strftime('%Y-%m-%d %H:%M:%S') for date in self.follow_up_dates])

# Example usage:
participant = Patient(name="Ted Williams", age=65, weight=75)

# Initiate medications
participant.initiate_medication('ARNI/ACE/ARB', 'Entresto', 50)
participant.initiate_medication('Beta Blocker', 'Metoprolol', 25)
participant.initiate_medication('MRA', 'Spironolactone', 12.5)
participant.initiate_medication('SGLT2', 'Dapagliflozin', 10)

# Schedule first follow-up in 2 weeks
participant.schedule_follow_up(2)

# Optimization at follow-up (after 2 weeks)
participant.optimize_medication('ARNI/ACE/ARB', 50)
participant.optimize_medication('Beta Blocker', 25)
participant.optimize_medication('MRA', 12.5)
participant.schedule_follow_up(2)

# Display patient info
participant.display_patient_info()
