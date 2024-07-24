# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 20:54:02 2024

@author: PatrickDunn
"""

@app.route('/log_data', methods=['POST'])
def log_data():
    patient_id = request.form['patient_id']
    weight = request.form['weight']
    medication = request.form['medication']
    adherence = int(request.form['adherence'])
    symptoms = request.form['symptoms']

    monitoring.log_weight(patient_id, float(weight))
    monitoring.log_medication_adherence(patient_id, medication, adherence)
    monitoring.log_symptoms(patient_id, symptoms)
    
    categorical_mappings = {
        'SMARTGoals': {'Set': 0, 'Not Set': 1},
        'HFSymptoms': {'Stable': 0, 'New or Worsening': 1},
        'MedicationAdherence': {'All the time': 0, 'Inconsistently': 1, 'I am not taking my medication as prescribed': 2},
        'ActionPlan': {'Following plan': 0, 'Inconsistent': 1, 'Not following plan': 2},
        'TreatmentGoal': {'At goal': 0, 'Improving, but not at goal': 1, 'Not making progress': 2},
        'GDMTStatus': {'Optimal': 0, 'Suboptimal': 1, 'Not on GDMT': 2}
    }

    SMARTGoals = categorical_mappings['SMARTGoals'][request.form['SMARTGoals']]
    HFSymptoms = categorical_mappings['HFSymptoms'][request.form['HFSymptoms']]
    MedicationAdherence = categorical_mappings['MedicationAdherence'][request.form['MedicationAdherence']]
    ActionPlan = categorical_mappings['ActionPlan'][request.form['ActionPlan']]
    TreatmentGoal = categorical_mappings['TreatmentGoal'][request.form['TreatmentGoal']]
    GDMTStatus = categorical_mappings['GDMTStatus'][request.form['GDMTStatus']]

    score = SMARTGoals + HFSymptoms + MedicationAdherence + ActionPlan + TreatmentGoal + GDMTStatus

    if score == 0:
        recheck_interval = 'Recheck in 4 weeks'
    elif score <= 2:
        recheck_interval = 'Recheck in 2 weeks'
    else:
        recheck_interval = 'Recheck in 1 week'

    monitoring.save_score(patient_id, score, recheck_interval)

    return redirect(url_for('index'))

