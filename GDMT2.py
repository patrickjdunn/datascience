# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 20:33:23 2024

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
    
    def initiate_or_optimize_medications(self, patient_id):
        patient = self._find_patient(patient_id)
        if patient:
            self._handle_ARNI_ACE_ARB(patient)
            self._handle_BetaBlocker(patient)
            self._handle_MRA(patient)
            self._handle_SGLT2(patient)
        else:
            print(f"Patient {patient_id} not found")
    
    def _handle_ARNI_ACE_ARB(self, patient):
        if patient['ejection_fraction'] < 40 and patient['renal_function'] > 30:
            if patient['medications']['ARNI_ACE_ARB'] is None:
                patient['medications']['ARNI_ACE_ARB'] = 'Initiated'
                print(f"Initiated ARNI/ACE/ARB for patient {patient['patient_id']}")
            elif patient['medications']['ARNI_ACE_ARB'] == 'Initiated':
                patient['medications']['ARNI_ACE_ARB'] = 'Optimized'
                print(f"Optimized ARNI/ACE/ARB for patient {patient['patient_id']}")
    
    def _handle_BetaBlocker(self, patient):
        if patient['ejection_fraction'] < 40 and patient['symptoms'] == 'Stable':
            if patient['medications']['BetaBlocker'] is None:
                patient['medications']['BetaBlocker'] = 'Initiated'
                print(f"Initiated Beta Blocker for patient {patient['patient_id']}")
            elif patient['medications']['BetaBlocker'] == 'Initiated':
                patient['medications']['BetaBlocker'] = 'Optimized'
                print(f"Optimized Beta Blocker for patient {patient['patient_id']}")
    
    def _handle_MRA(self, patient):
        if patient['ejection_fraction'] < 35 and patient['renal_function'] > 30:
            if patient['medications']['MRA'] is None:
                patient['medications']['MRA'] = 'Initiated'
                print(f"Initiated MRA for patient {patient['patient_id']}")
            elif patient['medications']['MRA'] == 'Initiated':
                patient['medications']['MRA'] = 'Optimized'
                print(f"Optimized MRA for patient {patient['patient_id']}")
    
    def _handle_SGLT2(self, patient):
        if patient['ejection_fraction'] < 40:
            if patient['medications']['SGLT2'] is None:
                patient['medications']['SGLT2'] = 'Initiated'
                print(f"Initiated SGLT2 Inhibitor for patient {patient['patient_id']}")
            elif patient['medications']['SGLT2'] == 'Initiated':
                patient['medications']['SGLT2'] = 'Optimized'
                print(f"Optimized SGLT2 Inhibitor for patient {patient['patient_id']}")
    
    def _find_patient(self, patient_id):
        for patient in self.patients:
            if patient['patient_id'] == patient_id:
                return patient
        return None

# Example usage
gdmt = HeartFailureGDMT()
gdmt.add_patient('001', 30, 'Stable', 35)
gdmt.initiate_or_optimize_medications('001')
