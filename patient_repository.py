
import psycopg
from database import get_connection

def add_patient_to_db(patient):
    """Add a new patient to the database."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute( #execute the SQL query to insert a new patient into the database
                    """ 
                    INSERT INTO patients (name, age, gender, condition)
                    VALUES (%s, %s, %s, %s)
                    RETURNING patient_id;
                    """,
                    (patient.name, patient.age, patient.gender, patient.condition)
                )
                patient_id = cursor.fetchone()[0] #retrieve the generated patient_id from the database after insertion
                
            return patient_id
    except psycopg.Error as e:
        print(f"Error adding patient to database: {e}")
        return None

def get_all_patients_from_db():
    """Retrieve all patients from the PostgreSQL database."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT patient_id, name, age, gender, condition 
                    FROM patients
                    ORDER BY patient_id;
                    """
                )

                rows = cursor.fetchall()
                patients = []
                for row in rows:
                    patient = {
                        "patient_id": row[0],
                        "name": row[1],
                        "age": row[2],
                        "gender": row[3],
                        "condition": row[4]
                    }
                    patients.append(patient)
        return patients


    except psycopg.Error as e:
        print(f"Error retrieving patient from database: {e}")
        return None

def get_patient_by_id(patient_id):
    """Retrieve a patient by ID from the PostgreSQL database."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT patient_id, name, age, gender, condition 
                    FROM patients
                    WHERE patient_id = %s;
                    """,
                    (patient_id,)
                )

                row = cursor.fetchone() #retrieve the first row of the result set, which corresponds to the patient with the specified ID
                if row:
                    patient = {
                        "patient_id": row[0],
                        "name": row[1],
                        "age": row[2],
                        "gender": row[3],
                        "condition": row[4]
                    }
                    return patient
                else:
                    return None

    except psycopg.Error as e:
        print(f"Error retrieving patient from database: {e}")
        return None


def update_patient_in_db(patient_id, name, age, gender, condition):
    """Update an existing patient's information in the PostgreSQL database."""
    try:
        with get_connection() as connection:  #establish a connection to the PostgreSQL database using the get_connection() function from the database module
            with connection.cursor() as cursor:
                cursor.execute( #%s placeholders safely pass Python values to SQL and WHERE ensures only the patient with the specified patient_id is updated
                    """UPDATE patients
                    SET name = %s, age = %s, gender = %s, condition = %s 
                    WHERE patient_id = %s;
                    """,
                    (name, age, gender, condition, patient_id)
                )
                result = cursor.rowcount  #retrieve the number of rows affected by the update operation
                if result is None or result == 0:
                    print(f"No patient found with ID: {patient_id}")
                    return False

                connection.commit()
                return True

    except psycopg.Error as e:
        print(f"Error updating patient in database: {e}")
        return False

def delete_patient_from_db(patient_id):
    """Delete a patient from the PostgreSQL database."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """ DELETE FROM patients 
                    WHERE patient_id = %s
                    RETURNING patient_id;
                    """,
                    (patient_id,)
                )

                result = cursor.fetchone()
                if result is None:
                    print(f"No patient found with ID: {patient_id}")
                    return False    

                connection.commit()
                return True
    except psycopg.Error as e:
        print(f"Error deleting patient from database: {e}")
        return False
