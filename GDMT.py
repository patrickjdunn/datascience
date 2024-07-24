# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 17:14:48 2024

@author: PatrickDunn
"""

class HeartFailureGDMT:
    def __init__(self):
        self.patients = []
    
    def add_patient(self, patient_id, ejection_fraction, symptoms, renal_function):
        patient = {
            'patient_id': patient_id,
            'ejection_fraction': ejection_fraction,
            'symptoms': symptoms,
            'renal_function': renal_function,
            'medications': {
                'ARNI_ACE_ARB': None,
                'BetaBlocker': None,
                'MRA': None,
                'SGLT2': None
            }
        }
        self.patients.append(patient)
    
    def initiate_ARNI_ACE_ARB(self, patient_id):
        patient = self._find_patient(patient_id)
        if patient:
            if patient['ejection_fraction'] < 40:
                if patient['renal_function'] > 30:
                    patient['medications']['ARNI_ACE_ARB'] = 'Initiated'
                    print(f"Initiated ARNI/ACE/ARB for patient {patient_id}")
                else:
                    print(f"Patient {patient_id} has poor renal function, cannot initiate ARNI/ACE/ARB")
            else:
                print(f"Patient {patient_id} does not meet ejection fraction criteria for ARNI/ACE/ARB")
    
    def optimize_ARNI_ACE_ARB(self, patient_id):
        patient = self._find_patient(patient_id)
        if patient and patient['medications']['ARNI_ACE_ARB'] == 'Initiated':
            patient['medications']['ARNI_ACE_ARB'] = 'Optimized'
            print(f"Optimized ARNI/ACE/ARB for patient {patient_id}")
        else:
            print(f"Cannot optimize ARNI/ACE/ARB for patient {patient_id}, not initiated yet")
    
    def initiate_BetaBlocker(self, patient_id):
        patient = self._find_patient(patient_id)
        if patient:
            if patient['ejection_fraction'] < 40 and patient['symptoms'] == 'Stable':
                patient['medications']['BetaBlocker'] = 'Initiated'
                print(f"Initiated Beta Blocker for patient {patient_id}")
            else:
                print(f"Patient {patient_id} does not meet criteria for Beta Blocker initiation")
    
    def optimize_BetaBlocker(self, patient_id):
        patient = self._find_patient(patient_id)
        if patient and patient['medications']['BetaBlocker'] == 'Initiated':
            patient['medications']['BetaBlocker'] = 'Optimized'
            print(f"Optimized Beta Blocker for patient {patient_id}")
        else:
            print(f"Cannot optimize Beta Blocker for patient {patient_id}, not initiated yet")
    
    def initiate_MRA(self, patient_id):
        patient = self._find_patient(patient_id)
        if patient:
            if patient['ejection_fraction'] < 35 and patient['renal_function'] > 30:
                patient['medications']['MRA'] = 'Initiated'
                print(f"Initiated MRA for patient {patient_id}")
            else:
                print(f"Patient {patient_id} does not meet criteria for MRA initiation")
    
    def optimize_MRA(self, patient_id):
        patient = self._find_patient(patient_id)
        if patient and patient['medications']['MRA'] == 'Initiated':
            patient['medications']['MRA'] = 'Optimized'
            print(f"Optimized MRA for patient {patient_id}")
        else:
            print(f"Cannot optimize MRA for patient {patient_id}, not initiated yet")
    
    def initiate_SGLT2(self, patient_id):
        patient = self._find_patient(patient_id)
        if patient:
            if patient['ejection_fraction'] < 40:
                patient['medications']['SGLT2'] = 'Initiated'
                print(f"Initiated SGLT2 Inhibitor for patient {patient_id}")
            else:
                print(f"Patient {patient_id} does not meet criteria for SGLT2 Inhibitor initiation")
    
    def optimize_SGLT2(self, patient_id):
        patient = self._find_patient(patient_id)
        if patient and patient['medications']['SGLT2'] == 'Initiated':
            patient['medications']['SGLT2'] = 'Optimized'
            print(f"Optimized SGLT2 Inhibitor for patient {patient_id}")
        else:
            print(f"Cannot optimize SGLT2 Inhibitor for patient {patient_id}, not initiated yet")
    
    def _find_patient(self, patient_id):
        for patient in self.patients:
            if patient['patient_id'] == patient_id:
                return patient
        print(f"Patient {patient_id} not found")
        return None

# Example usage
gdmt = HeartFailureGDMT()
gdmt.add_patient('001', 30, 'Stable', 35)
gdmt.initiate_ARNI_ACE_ARB('001')
gdmt.optimize_ARNI_ACE_ARB('001')
gdmt.initiate_BetaBlocker('001')
gdmt.optimize_BetaBlocker('001')
gdmt.initiate_MRA('001')
gdmt.optimize_MRA('001')
gdmt.initiate_SGLT2('001')
gdmt.optimize_SGLT2('001')
