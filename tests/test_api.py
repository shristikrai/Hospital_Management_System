from fastapi.testclient import TestClient
from api import app 

client = TestClient(app)

#Test 1: Verify the health endpoint
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "Healthy",
        "message": "The Hospital Management API is running successfully."
    }


# Test 2: Verify patient creation without modifying PostgreSQL
def test_create_patient(monkeypatch):

    # Step 1: Prepare sample patient data
    patient_data = {
        "name": "John Doe",
        "age": 30,
        "gender": "Male",
        "condition": "Common Cold"
    }

    # Step 2: Mock database insertion
    def mock_add_patient_to_db(patient):
        return 1

    # Step 3: Mock retrieving the created patient
    def mock_get_patient_by_id(patient_id):
        return {
            **patient_data,
            "patient_id": patient_id
        }

    # Step 4: Replace real database functions with mocks
    monkeypatch.setattr(
        "api.add_patient_to_db",
        mock_add_patient_to_db
    )

    monkeypatch.setattr(
        "api.get_patient_by_id",
        mock_get_patient_by_id
    )

    # Step 5: Send POST request
    response = client.post("/patients", json=patient_data)

    # Step 6: Verify response
    assert response.status_code == 201

    assert response.json() == {
        **patient_data,
        "patient_id": 1
    }


#Test 3:Retrieve all patients without accessing PostgreSQL
def test_get_all_patients(monkeypatch):
    # Step 1: Prepare sample patient records
    patients_data = [
        {
            "patient_id": 1,
            "name": "John Doe",
            "age": 30,
            "gender": "Male",
            "condition": "Common Cold"
        },
        {
            "patient_id": 2,
            "name": "Jane Smith",
            "age": 25,
            "gender": "Female",
            "condition": "Flu"
        }
    ]

    # Step 2: Mock retrieving all patients
    def mock_get_all_patients_from_db():
        return patients_data

    # Step 3: Replace real database function with mock
    monkeypatch.setattr(
        "api.get_all_patients_from_db",
        mock_get_all_patients_from_db
    )

    # Step 4: Send GET request
    response = client.get("/patients")

    # Step 5: Verify response
    assert response.status_code == 200
    assert response.json() == patients_data
    assert len(response.json()) == 2

#Test 4: Retrieve a patient by ID without accessing PostgreSQL
def test_get_patient_by_id(monkeypatch):
    # Step 1: Prepare sample patient data
    patient_data = {
        "patient_id": 1,
        "name": "John Doe",
        "age": 30,
        "gender": "Male",
        "condition": "Common Cold"
    }

    # Step 2: Mock retrieving a patient by ID
    def mock_get_patient_by_id(patient_id):
        if patient_id == 1:
            return patient_data
        else:
            return None

    # Step 3: Replace real database function with mock
    monkeypatch.setattr(
        "api.get_patient_by_id",
        mock_get_patient_by_id
    )

    # Step 4: Send GET request for existing patient
    response_existing = client.get("/patients/1")
    assert response_existing.status_code == 200
    assert response_existing.json() == patient_data

    # Step 5: Send GET request for non-existing patient
    response_non_existing = client.get("/patients/999")
    assert response_non_existing.status_code == 404
    assert response_non_existing.json() == {
        "detail": "Patient with ID 999 not found"
    }

#Test 5: Update a patient without accessing PostgreSQL
def test_update_patient(monkeypatch):
    # Step 1: Prepare sample patient data and updates
    original_patient_data = {
        "patient_id": 1,
        "name": "John Doe",
        "age": 30,
        "gender": "Male",
        "condition": "Common Cold"
    }

    updates = {
        "age": 31,
        "condition": "Recovered"
    }

    updated_patient_data = {
        **original_patient_data,
        **updates
    }

    # Step 2: Mock updating a patient in the database
    def mock_update_patient_in_db(patient_id, updates):
        if patient_id == 1:
            assert updates =={
                "age": 31,
                "condition": "Recovered"
            }
            return True
        else:
            return False

    # Step 3: Mock retrieving the updated patient by ID
    def mock_get_patient_by_id(patient_id):
        if patient_id == 1:
            return updated_patient_data
        else:
            return None

    # Step 4: Replace real database functions with mocks
    monkeypatch.setattr(
        "api.update_patient_in_db",
        mock_update_patient_in_db
    )

    monkeypatch.setattr(
        "api.get_patient_by_id",
        mock_get_patient_by_id
    )

    # Step 5: Send PATCH request to update the patient
    response = client.patch("/patients/1", json=updates)

    # Step 6: Verify response for successful update
    assert response.status_code == 200
    assert response.json() == updated_patient_data

    # Step 7: Send PATCH request for non-existing patient
    response_non_existing = client.patch("/patients/999", json=updates)
    assert response_non_existing.status_code == 404
    assert response_non_existing.json() == {
        "detail": "Patient with ID 999 not found"
    }


# Test 6: Delete a patient without accessing PostgreSQL
def test_delete_patient(monkeypatch):

    # Step 1: Mock deleting a patient from PostgreSQL
    def mock_delete_patient_from_db(patient_id):
        if patient_id == 1:
            return True
        else:
            return False

    # Step 2: Replace actual database function with mock
    monkeypatch.setattr(
        "api.delete_patient_from_db",
        mock_delete_patient_from_db
    )

    # Step 3: Send DELETE request for existing patient
    response = client.delete("/patients/1")

    # Step 4: Verify successful deletion
    assert response.status_code == 204
    assert response.content == b""

    # Step 5: Send DELETE request for non-existing patient
    response_non_existing = client.delete("/patients/999")

    # Step 6: Verify patient not found
    assert response_non_existing.status_code == 404
    assert response_non_existing.json() == {
        "detail": "Patient with ID 999 not found or deletion failed"
    }
