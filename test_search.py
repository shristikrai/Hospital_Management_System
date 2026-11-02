from patient_repository import get_patient_by_id
try:
    patient_id = int(input("Enter the patient ID you want to search for: "))
    patient = get_patient_by_id(patient_id)

    if patient is not None:
        print("\n--- Patient Found ---")
        print(f"Patient ID: {patient['patient_id']}")
        print(f"Name: {patient['name']}")
        print(f"Age: {patient['age']}")
        print(f"Gender: {patient['gender']}")
        print(f"Condition: {patient['condition']}") 
    else:
        print(f"No patient found with ID: {patient_id}")
except ValueError:
    print("Invalid input. Please enter a valid number for the patient ID.")

except Exception as e:
    print(f"An error occurred while searching for the patient: {e}")    