from patient_repository import update_patient_in_db, get_patient_by_id

try:
    patient_id = int(input("Enter the patient ID you want to update: "))
    patient = get_patient_by_id(patient_id)

    if patient is not None:
        print("\n--- Current Patient Details ---")
        print(f"Patient ID: {patient['patient_id']}")
        print(f"Name: {patient['name']}")
        print(f"Age: {patient['age']}")
        print(f"Gender: {patient['gender']}")
        print(f"Condition: {patient['condition']}")

        # Prompt for new details
        name = input("Enter new name (leave blank to keep current): ").strip() or patient['name']
        age_input = input("Enter new age (leave blank to keep current): ").strip()
        age = int(age_input) if age_input else patient['age']
        gender = input("Enter new gender (leave blank to keep current): ").strip() or patient['gender']
        condition = input("Enter new condition (leave blank to keep current): ").strip() or patient['condition']

        # Update the patient in the database
        updated = update_patient_in_db(patient_id, name, age, gender, condition)
        if updated:
            print("\nPatient details updated successfully.")

            updated_patient = get_patient_by_id(patient_id)
            print("\n--- Updated Patient Details ---")
            print(updated_patient)
        else:
            print("\nFailed to update patient details.")

    else:
        print(f"No patient found with ID: {patient_id}")
    
except ValueError:
    print("Invalid input. Please enter a valid number for the patient ID or age.")

