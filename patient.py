class Patient: #class
    def __init__(self,patient_id,name,age,gender,condition): #constructor
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.condition = condition

    def display_info(self):
        print("Patient ID: ", self.patient_id) #display_info() is designed to display information,so print() is used
        print("Name: ", self.name)
        print("Age: ", self.age)
        print("Gender: ", self.gender)
        print("Condition: ",self.condition)

    def update_age(self,new_age):
        if new_age > 0:
            self.age = new_age
            return True
        else:
            print("Age must be greater than 0.")
            return False
    
    def update_condition(self,new_condition):
        if new_condition.strip():
            self.condition = new_condition
            return True
        else:
            print("Medical condition cannot be empty.")
            return False

    def update_name(self,new_name):
        if new_name.strip():
            self.name = new_name
            return True
        else:
            print("Name cannot be empty.")
            return False

    def update_gender(self,new_gender):
        if new_gender.strip():
            self.gender = new_gender
            return True
        else:
            print("Gender cannot be empty.")
            return False 

    def to_dict(self):
        return{ #whereas, to_dict() is designed to produce data, so it uses return
            "patient_id" : self.patient_id,
            "name" : self.name,
            "age" : self.age,
            "gender" : self.gender,
            "condition" : self.condition
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["patient_id"],
            data["name"],
            data["age"],
            data["gender"],
            data["condition"]
        )

if __name__ == "__main__": #if patient.py is run directly, run the testing code
    #if its run from main.py(from patient import Patient), dont run all the test patients | becoz its being imported not run directly

    patient_data = {
    "patient_id": 3,
    "name": "Sarah Mill",
    "age": 30,
    "gender": "Female",
    "condition": "Diabetic"
}

    patient1 = Patient(1,"Shristi Rai", 25, "Female", "Normal")
    patient2 = Patient(2, "John Smith", 50, "Male", "Diabetic")
    patient3 = Patient.from_dict(patient_data)

    #Test update_age()
    print("Before updating age: ")
    patient1.display_info()
    print()
    patient1.update_age(30)
    print()
    print("\nAfter updating age: ")
    patient1.display_info()

    #Test update_condition()
    print("\nBefore updating condition: ")
    patient1.display_info()
    print()
    patient1.update_condition("High Blood Pressure")

    print("\nAfter updating condition: ")
    patient1.display_info()
    print()

    #Test update_name()
    print("\nBefore updating name: ")
    patient1.display_info()
    print()
    patient1.update_name("Shristi Kumari Rai")

    print("\nAfter updating name: ")
    patient1.display_info()
    print()

    #Test update_gender()
    print("\nBefore updating gender: ")
    patient1.display_info()
    print()
    patient1.update_gender("Other")
  
    print("\nAfter updating gender: ")
    patient1.display_info()
    print()

    patient2.display_info()
    print()
    patient3.display_info()
    print()


    print(patient1.to_dict())