from patient import Patient
from patient_repository import add_patient_to_db

# Create a new patient
patient = Patient(patient_id=0, name="Aayush Rasali", age=30, gender="Male", condition="Fever")

# Add the patient to the PostgreSQL database
patient_id = add_patient_to_db(patient)

if patient_id is not None:
    print(f"Patient added successfully with ID: {patient_id}")
else:
    print("Failed to add patient to the database.")