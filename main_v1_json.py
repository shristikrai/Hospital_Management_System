import json
from patient import Patient

DATA_FILE = "data/patients.json"

#store all patients in a list and keep track of the next patient ID
patients = []
next_patient_id = 1


#save all patients in JSON file
def save_patients():
    with open(DATA_FILE,"w") as file:
        json.dump(
            [patient.to_dict() for patient in patients],
            file,
            indent=4
        )


#load patients from JSON file
def load_patients():
    global patients
    global next_patient_id
    try:
        with open(DATA_FILE,"r") as file:
            data = json.load(file)
            patients = [Patient.from_dict(patient) for patient in data]

        if patients:
            next_patient_id = max(
                patient.patient_id for patient in patients
            ) +1
        else:
            next_patient_id = 1
    except FileNotFoundError:
        print("Data file not found. Starting with an empty patient list.")
        patients = []
        next_patient_id = 1

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data. Starting with an empty patient list.")
        patients = []
        next_patient_id = 1


#Add a new patient
def add_patient():
    global next_patient_id

    # Validate name
    while True:
        name = input ("Enter patient full name: ").strip()

        if name:
            break
        print("Patient name cannot be empty.")

    # Validate age
    while True:
        try:
            age = int(input("Enter patient age: "))
            if age < 0 or age > 120:
                print("Please enter an age between 0 and 120.")
                continue
            break
        except ValueError:
            print("Invalid input. Age must be a number.")

    # Validate gender
    while True:
         gender = input ("Enter gender: ").strip()

         if gender:
            break
            print("Gender cannot be empty.")

    # Validate medical condition
    while True:
        condition = input("Enter medical condition: ").strip()
        if condition:
            break
        print("Medical condition cannot be empty.")

    patient = Patient(
        next_patient_id,
        name,
        age,
        gender,
        condition
    )

    patients.append(patient)
    next_patient_id += 1
    save_patients()

    print("\nPatient added successfully.")


#  View patients
def view_patients():
    if not patients:
        print("\nNo patients found.")
        return
    print("\n--- Patient List ---")

    for patient in patients:
        print()
        patient.display_info()

        
# Search patient
def search_patient():
    print("\n--- Search Patient ---")
    print("1. Search by Patient Id")
    print("2. Search by Patient Name ")
    choice = input(" Enter your choice : ").strip()

    # Search by Id
    if choice == "1":
        try:
            patient_id = int(input("Enter Patient ID: "))
        except ValueError:
            print("Invalid Patient ID. Please enter a number.")
            return

        for patient in patients:
            if patient.patient_id == patient_id:
                print("\n--- Patient Found ---")
                patient.display_info()
                return

        print("Patient not found.")

    # Search by name
    elif choice == "2":
        name = input(" Enter Patient name: ").strip()
        if not name:
            print(" Patient name cannot be Empty. ")
            return

        found = False
        for patient in patients:
            if name.lower() in patient.name.lower():
                print("\n--- Patient Found ---")
                patient.display_info()
                found = True

        if not found:
            print("Patient not found.")
    else:
        print("Invalid choice. Please select 1 0r 2.")


# Update patient
def update_patient():
    try:
        patient_id = int(input("Enter Patient ID to Update: "))
    except ValueError:
        print("Invalid Patient ID. Please enter a number.")
        return

    for patient in patients:
        if patient.patient_id == patient_id:
            print("\nPatient Found:", patient.name)
            
            # Get and validate name
            name = input("Enter new name: ").strip()
            if not name:
                print("Name cannot be Empty. ")
                return

            # Get and validate age
            try:
                age = int(input("Enter new age: "))
            except ValueError:
                print("Age must be a number.")
                return

            if age <= 0:
                print("Age must be greater than 0. ")
                return
            
            # Get and validate gender
            gender = input("Enter new gender: ").strip()
            if not gender:
                print("Gender cannot be Empty. ")
                return

            # Get and validate condition    
            condition = input("Enter new condition: ").strip()
            if not condition:
                print("Medical condition cannot be Empty.")
                return

            # Update only after all validations pass
            patient.update_name(name)
            patient.update_age(age)
            patient.update_gender(gender)
            patient.update_condition(condition)

            # Save changes to JSON
            save_patients()

            print("\nPatient updated successfully.")
            return
    print("\nPatient not found.")


# Delete patient
def delete_patient():
    try:
        patient_id = int(input("Enter Patient ID to delete: "))
    except ValueError:
        print("Invalid Patient ID. Please enter a number.")
        return

    for patient in patients:
        if patient.patient_id == patient_id:
            print("\n--- Patient Found --- ")
            patient.display_info()

            confirmation = input("\nAre you sure, you want to delete this patient ? (y/n): ").strip().lower()
            if confirmation == "y":
                patients.remove(patient)
                save_patients()
                print("Patient deleted successfully.")
            elif confirmation == "n":
                print("Deletion cancelled.")
            else:
                print("Invalid input. Deletion cancelled.")
            return
    print("\nPatient not found.")

# Load patients from JSON
load_patients()

# Main menu
while True:
    print("\n--- Hospital Patient Management System ---")
    print("1. Add Patient")
    print("2. View Patients")
    print("3. Search Patients")
    print("4. Update Patient")
    print("5. Delete Patient")
    print("6. Exit")

    choice= input("\nEnter your choice: ").strip()

    if choice == "1":
        add_patient()

    elif choice == "2":
       view_patients()
    elif choice == "3":
        search_patient()

    elif choice == "4":
        update_patient()

    elif choice == "5":
        delete_patient()

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
