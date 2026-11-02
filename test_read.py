
import sys
from patient_repository import get_all_patients_from_db

patients = get_all_patients_from_db()

if patients is None:
    print("Failed to retrieve patients from the database.")
    sys.exit(1)  # Exit the program if patients could not be retrieved

elif not patients:
    print("No patients found in the database.")

else:
    print("\n--- Patient Records ---")
    for patient in patients:
        print(f"Patient ID: {patient['patient_id']}")
        print(f"Name: {patient['name']}")
        print(f"Age: {patient['age']}")
        print(f"Gender: {patient['gender']}")
        print(f"Condition: {patient['condition']}")
        print("------------------------")

