
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
#CORSMiddleware allows our future Streamlit frontend to communicate with the FastAPI backend without running into cross-origin issues.

from fastapi import HTTPException,status
from schemas import PatientCreate, PatientUpdate, PatientResponse

from patient_repository import (
    add_patient_to_db,
    get_all_patients_from_db,
    get_patient_by_id,
    update_patient_in_db,
    delete_patient_from_db
)


#initialize FastAPI app
app = FastAPI(
    title="Hospital Management System API",
    description="REST API for managing patient records using PostgreSQL.",
    version="3.0.0"
)

#Configure CORS middleware to allow cross-origin requests from any origin, with any method and headers. This is useful for development and testing purposes, but in production, you may want to restrict the allowed origins for security reasons.
app.add_middleware(
    CORSMiddleware,  
    allow_origins=["http://localhost:8501"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Endpoint 1:Home
@app.get("/") #returns basic application information 
async def home():
    return {
        "message": "Welcome to the Hospital Management System API!",
        "version": "3.0.0",
        "status": "API is running successfully."
        }

#Endpoint 2:Health Check
@app.get("/health") #checks the health of the API
async def health_check():
    return {
        "status": "Healthy",
        "message": "The Hospital Management API is running successfully."
    }


@app.post(
    "/patients",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED
)
def create_patient(patient: PatientCreate):
    """Create a new patient record in PostgreSQL."""

    # Step 1: Insert patient into the database
    patient_id = add_patient_to_db(patient)

    # Step 2: Check whether insertion succeeded
    if patient_id is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to create patient"
        )

    # Step 3: Retrieve the newly created patient
    new_patient = get_patient_by_id(patient_id)

    if new_patient is None:
        raise HTTPException(
            status_code=500,
            detail="Patient created but could not be retrieved"
        )

    # Step 4: Return the patient information
    return new_patient

#Endpoint 3: Retrieve All Patients
@app.get("/patients", response_model=list[PatientResponse])
def get_all_patients():
    """Retrieve all patient records from PostgreSQL."""
    patients = get_all_patients_from_db()

    if patients is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve patients"
        )
    return patients

#Endpoint 4: Retrieve a Patient by ID
@app.get(
    "/patients/{patient_id}", 
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK
)
def get_patient(patient_id: int):
    """Retrieve a patient record by ID from PostgreSQL."""
    patient = get_patient_by_id(patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    return patient

#Endpoint 5: Update a Patient
@app.patch(
    "/patients/{patient_id}",
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK
)
def update_patient(patient_id: int, updates: PatientUpdate):    
    """Update selected patient record in PostgreSQL."""

    #step 1 : Get only the field provided by the user for update, excluding unset fields.
    update_data=updates.model_dump(exclude_unset=True) #exclude_unset=True ensures that only the fields provided by the user are included in the updates dictionary, preventing accidental overwriting of existing data with None values.

    #step 2: Update the patient in postgreSQL 
    result = update_patient_in_db(patient_id, update_data)

    #step 3: handle errors
    if result is None:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update patient with ID {patient_id}"
        )
    
    if result is False:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )

    #step 4: Retrieve the updated patient record
    updated_patient = get_patient_by_id(patient_id)
    
    if updated_patient is None:
        raise HTTPException(
            status_code=500,
            detail=f"Patient with ID {patient_id} updated but could not be retrieved"
        )
    return updated_patient

@app.delete(
    "/patients/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_patient(patient_id: int):
    """Delete a patient record by ID from PostgreSQL."""

    #step 1: Delete the patient from PostgreSQL
    result = delete_patient_from_db(patient_id)

    #step 2: Check if deletion was successful and handle errors
    if result is False:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found or deletion failed"
        )

    #step 3: Return a success message
    return None


    