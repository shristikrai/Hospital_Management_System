
from patient import Patient
from patient_repository import (
    add_patient_to_db,
    get_patient_by_id,
    get_all_patients_from_db,
    update_patient_in_db,
    delete_patient_from_db                      
)

def display_patient(patient):
    print("\n--- Patient Details ---")
    print(f"Patient ID: {patient['patient_id']}")
    print(f"Name: {patient['name']}")
    print(f"Age: {patient['age']}")
    print(f"Gender: {patient['gender']}")
    print(f"Condition: {patient['condition']}")
    print("------------------------")

#validate patient name,age,gender and medical condition.
def get_patient_details():
    name = input("Enter patient name: ").strip()
    while not name:
        print("Name cannot be empty. Please enter a valid name.")
        name = input("Enter patient name: ").strip()

    age_input = input("Enter patient age: ").strip()
    while not age_input.isdigit() or not (0 < int(age_input) <= 120):
        print("Invalid age. Please enter a number between 1 and 120.")
        age_input = input("Enter patient age: ").strip()
    age = int(age_input)

    gender = input("Enter patient gender (M/F): ").strip().upper()
    while gender not in ['M', 'F']:
        print("Invalid gender. Please enter 'M' for Male or 'F' for Female.")
        gender = input("Enter patient gender (M/F): ").strip().upper()

    condition = input("Enter medical condition: ").strip()
    while not condition:
        print("Medical condition cannot be empty. Please enter a valid condition.")
        condition = input("Enter medical condition: ").strip()

    return Patient(None, name, age, gender, condition)

#Add a new patient to the PostgreSQL database using the add_patient_to_db function from patient_repository.py
def add_patient():
    patient = get_patient_details()     #collect patient details from user input and return a Patient object
    patient_id = add_patient_to_db(patient)   #insert the patient into the database and return the added patient object with the assigned patient_id         
    if patient_id is not None:
        print("\nPatient added successfully.")
        display_patient(get_patient_by_id(patient_id))  #retrieve the added patient from the database and display its details   
    else:
        print("\nFailed to add patient.")

#Retrive and display all patients from PostgreSQL
def view_patients():
    patients = get_all_patients_from_db()  #retrieve all patients from the database
    if patients is None:
        print("\nFailed to retrieve patients from PostgreSQL.")
        return
    if not patients:
        print("\nNo patients found.")
        return
    
    print(f"\nTotal patients found: {len(patients)}")
    print("\n--- Patient List ---")

    for patient in patients:
        display_patient(patient)  #display each patient's details

#search for a patient by ID and display its details
def search_patient():
    try:
        patient_id = int(input("Enter the patient ID you want to search for: "))

        if patient_id <= 0:
            print("Invalid input. Please enter a positive number for the patient ID.")
            return

        patient = get_patient_by_id(patient_id)

        if patient is not None:
            print("\n--- Patient Found ---")
            display_patient(patient)
        else:

            print(f"No patient found with ID: {patient_id}")
    except ValueError:
        print("Invalid input. Please enter a valid number for the patient ID.")
    except Exception as e:
        print(f"An error occurred while searching for the patient: {e}")
    

#update an existing patient's information in PostgreSQL
def update_patient():
    try:
        patient_id = int(input("Enter the patient ID you want to update: "))
        if patient_id <= 0:
            print("Invalid input. Please enter a positive number for the patient ID.")
            return

        patient = get_patient_by_id(patient_id)

        if patient is not None:
            print("\n--- Current Patient Details ---")
            display_patient(patient)

            # Prompt for new details
            name = input("Enter new name (leave blank to keep current): ").strip() or patient['name']
            age_input = input("Enter new age (leave blank to keep current): ").strip()
            age = int(age_input) if age_input else patient['age']
            if age <= 0 or age > 120:
                print("Invalid age. Please enter a number between 1 and 120.")
                return
            gender = input("Enter new gender (leave blank to keep current): ").strip() or patient['gender']
            if gender.upper() not in ['M', 'F', 'MALE', 'FEMALE']:
                print("Invalid gender. Please enter 'M' for Male or 'F' for Female.")
                return
            
            condition = input("Enter new condition (leave blank to keep current): ").strip() or patient['condition']

            # Update the patient in the database
            updated = update_patient_in_db(patient_id, name, age, gender, condition)
            if updated:
                print("\nPatient details updated successfully.")
                updated_patient = get_patient_by_id(patient_id)

                if updated_patient is not None:
                    print("\n--- Updated Patient Details ---")
                    display_patient(updated_patient)
            else:
                print("\nFailed to update patient details.")

        else:
            print(f"No patient found with ID: {patient_id}")

    except ValueError:
        print("Invalid input. Please enter a valid number for the patient ID or age.")
    except Exception as e:
        print(f"An error occurred while updating the patient: {e}")

#Delete an existing patient from PostgreSQL
def delete_patient():
    try:
        patient_id = int(input("Enter the patient ID you want to delete: "))
        if patient_id <= 0:
            print("Invalid input. Please enter a positive number for the patient ID.")
            return

        patient = get_patient_by_id(patient_id)

        if patient is None:
            print(f"No patient found with ID: {patient_id}")
        else:
            print("\n--- Patient Details ---")
            display_patient(patient)

            confirmation = input("Are you sure you want to delete this patient? (yes/no): ").strip().lower()
            if confirmation == 'yes':
                deleted = delete_patient_from_db(patient_id)
                if deleted:
                    print("\nPatient deleted successfully.")
                    remaining_patients = get_patient_by_id(patient_id)
                    if remaining_patients is None:
                        print(f"Patient with ID {patient_id} has been removed from the database.")
                    else:
                        print(f"Patient with ID {patient_id} still exists in the database.")
                else:
                    print("\nFailed to delete patient.")
            elif confirmation == 'no':
                print("\nDeletion cancelled.")
            else:
                print("\nDeletion cancelled.")

    except ValueError:
        print("Invalid input. Please enter a valid number for the patient ID.")
    except Exception as e:
        print(f"An error occurred while deleting the patient: {e}")

#Main menu for Hospital Management System
def main_menu():
    while True:
        print("\n--- Hospital Patient Management System ---")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Search Patient by ID")
        print("4. Update Patient by ID")
        print("5. Delete Patient by ID")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            add_patient()
        elif choice == '2':
            view_patients()
        elif choice == '3':
            search_patient()
        elif choice == '4':
            update_patient()
        elif choice == '5':
            delete_patient()
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
if __name__ == "__main__":
    main_menu()

