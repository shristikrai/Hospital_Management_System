from patient_repository import delete_patient_from_db, get_patient_by_id

try:
    patient_id = int(input("Enter the patient ID you want to delete: "))
    patient = get_patient_by_id(patient_id)

    if patient is None:
        print(f"No patient found with ID: {patient_id}")
    else:
        print("\n--- Patient Details ---")
        print(f"Patient ID: {patient['patient_id']}")
        print(f"Name: {patient['name']}")
        print(f"Age: {patient['age']}")
        print(f"Gender: {patient['gender']}")
        print(f"Condition: {patient['condition']}")

        confirmation = input("Are you sure you want to delete this patient? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            deleted = delete_patient_from_db(patient_id)
            if deleted:
                print("\nPatient deleted successfully.")
            else:
                print("\nFailed to delete patient.")
        else:
            print("\nDeletion cancelled.")

except ValueError:
    print("Invalid input. Please enter a valid number for the patient ID.")
except Exception as e:
    print(f"An error occurred while deleting the patient: {e}")