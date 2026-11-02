import psycopg
import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace

from patient_repository import (
    add_patient_to_db,
    get_all_patients_from_db,
    get_patient_by_id,
    update_patient_in_db,
    delete_patient_from_db,
)


class TestPatientRepository(unittest.TestCase):

    def setUp(self):
        # Create a fake PostgreSQL connection and cursor
        self.connection = MagicMock()
        self.cursor = MagicMock()

        self.connection.__enter__.return_value = self.connection
        self.connection.cursor.return_value.__enter__.return_value = self.cursor

        # Replace the real database connection
        self.patcher = patch(
            "patient_repository.get_connection",
            return_value=self.connection
        )
        self.mock_connection = self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.patient_row = (
            1, "John Doe", 30, "M", "Healthy"
        )

        self.patient_dict = {
            "patient_id": 1,
            "name": "John Doe",
            "age": 30,
            "gender": "M",
            "condition": "Healthy"
        }

    # TEST 1: INSERT PATIENT
    def test_add_patient(self):
        patient = SimpleNamespace(
            name="John Doe",
            age=30,
            gender="M",
            condition="Healthy"
        )

        self.cursor.fetchone.return_value = (1,)

        result = add_patient_to_db(patient)

        self.assertEqual(result, 1)
        self.cursor.execute.assert_called_once()

        params = self.cursor.execute.call_args.args[1]
        self.assertEqual(
            params,
            ("John Doe", 30, "M", "Healthy")
        )

    # TEST 2: GET ALL PATIENTS
    def test_get_all_patients(self):
        self.cursor.fetchall.return_value = [
            self.patient_row
        ]

        result = get_all_patients_from_db()

        self.assertEqual(result, [self.patient_dict])
        self.cursor.execute.assert_called_once()

    # TEST 3: GET PATIENT BY ID
    def test_get_patient_by_id(self):
        self.cursor.fetchone.return_value = self.patient_row

        result = get_patient_by_id(1)

        self.assertEqual(result, self.patient_dict)
        self.assertEqual(
            self.cursor.execute.call_args.args[1],
            (1,)
        )

    # TEST 4: PATIENT NOT FOUND
    def test_patient_not_found(self):
        self.cursor.fetchone.return_value = None

        result = get_patient_by_id(999)

        self.assertIsNone(result)

    # TEST 5: UPDATE PATIENT
    def test_update_patient(self):
        self.cursor.rowcount = 1

        result = update_patient_in_db(
            1, "Jane Doe", 28, "F", "Recovered"
        )

        self.assertTrue(result)
        self.assertEqual(
            self.cursor.execute.call_args.args[1],
            ( "Jane Doe", 28, "F", "Recovered", 1 )
        )

    # TEST 6: UPDATE NONEXISTENT PATIENT
    def test_update_patient_not_found(self):
        self.cursor.rowcount = 0

        result = update_patient_in_db(
            999, "Jane Doe", 28, "F", "Healthy"
        )

        self.assertFalse(result)

    # TEST 7: DELETE PATIENT
    def test_delete_patient(self):
        self.cursor.fetchone.return_value = (1,)

        result = delete_patient_from_db(1)

        self.assertTrue(result)
        self.assertEqual(
            self.cursor.execute.call_args.args[1],
            (1,)
        )

    # TEST 8: DELETE NONEXISTENT PATIENT
    def test_delete_patient_not_found(self):
        self.cursor.fetchone.return_value = None

        result = delete_patient_from_db(999)

        self.assertFalse(result)

    # TEST 9: INSERT - DATABASE ERROR
    def test_add_patient_db_error(self):
        self.cursor.execute.side_effect = psycopg.OperationalError ("Database error")

        patient = SimpleNamespace(
            name="John Doe",
            age=30,
            gender="M",
            condition="Healthy"
        )

        result = add_patient_to_db(patient)

        self.assertIsNone(result)

    #TEST 10: GET ALL PATIENTS - DATABASE ERROR
    def test_get_all_patients_db_error(self):
        self.cursor.execute.side_effect = psycopg.OperationalError("Database retrieval failed") 

        result = get_all_patients_from_db()

        self.assertIsNone(result)

    #TEST 11: SEARCH PATIENT BY ID - DATABASE ERROR
    def test_get_patient_by_id_db_error(self):
        self.cursor.execute.side_effect = psycopg.OperationalError("Database search failed") 

        result = get_patient_by_id(1) 

        self.assertIsNone(result)

    #TEST 12: UPDATE PATIENT - DATABASE ERROR
    def test_update_patient_db_error(self):
        self.cursor.execute.side_effect = psycopg.OperationalError("Database update failed") 

        result = update_patient_in_db(1, "Jane Doe", 28, "F", "Recovered") 

        self.assertFalse(result)

    #TEST 13: DELETE PATIENT - DATABASE ERROR
    def test_delete_patient_db_error(self):
        self.cursor.execute.side_effect = psycopg.OperationalError("Database deletion failed") 

        result = delete_patient_from_db(1) 

        self.assertFalse(result)    
        
if __name__ == "__main__":
    unittest.main()
