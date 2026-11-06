import streamlit as st
import requests

#Step 1: Configure the Streamlit page
st.set_page_config(
    page_title="Hospital Management System",
    page_icon=":hospital:",
    layout="wide"
)

#step 2: Define FastAPI backend URL
API_URL = "http://localhost:8000"

#step 3: Dashboard title
st.title("Hospital Management System")
st.write("Patient Management Dashboard - Version 3")

#Step 4:Check FastAPT connection
st.subheader("Backend Connection Status")

try:
    response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )
    if response.status_code == 200:
        st.success("Backend connection successful")
    else:
        st.error(f"Backend connection failed with status code {response.status_code}")
except requests.exceptions.RequestException as e:
    st.error(f"Backend connection failed: {e}")

#step 5: Display all patients
st.subheader("Patient Records")

try:
    #Request patient data from FastAPI
    response = requests.get(
        f"{API_URL}/patients",
        timeout=5
    )

    if response.status_code == 200:
        patients = response.json()

        if patients:
            st.dataframe(
                patients,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No patient records found.")
    
    else:
        st.error(
            f"Failed to retrieve patients."
            f"Status code: {response.status_code}"
        )
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching patient records: {e}")

#step 6:Add a new patient
st.subheader("Add New Patient")

with st.form("add_patient_form"):   #creates a form for entering patient information
    name = st.text_input("Patient Name") #collects the patients name and condition
    age = st.number_input(  #collects their age
        "Age",
        min_value=0,
        max_value=120,
        value=0
    )

    gender = st.selectbox(      
        "Gender",
        ["M", "F", "Other"]
    )

    condition = st.text_input("Medical Condition")
    submitted = st.form_submit_button("Add Patient")

    if submitted:
        patient_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "condition": condition
        }

        try:
            response = requests.post(
                f"{API_URL}/patients",
                json=patient_data,
                timeout=5
            )
            if response.status_code == 201:
                st.success("Patient added successfully!")
                st.rerun()

            else:
                st.error(
                    f"Failed to add patient: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")


# Step 6: Search Patient by ID
st.subheader("Search Patient by ID")

# Step 1: Enter patient ID
search_id = st.number_input(
    "Enter Patient ID",
    min_value=1,
    step=1,
    key="search_patient_id"
)

# Step 2: Search button
if st.button("Search Patient"):

    # Step 3: Send GET request to FastAPI
    try:
        response = requests.get(
            f"{API_URL}/patients/{search_id}",
            timeout=5
        )

        # Step 4: Check response
        if response.status_code == 200:
            patient = response.json()

            st.success("Patient found successfully!")
            st.write("Patient Details")
            st.json(patient)

        elif response.status_code == 404:
            st.warning("Patient not found!")

        else:
            st.error(
                f"Error fetching patient: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Backend connection failed: {e}")


# Step 7: Update Patient Details
st.subheader("Update Patient Details")

# Step 1: Enter the patient ID
update_id = st.number_input(
    "Enter Patient ID to Update",
    min_value=1,
    step=1,
    key="update_patient_id"
)

# Step 2: Enter optional updates
new_name = st.text_input("New Patient Name (Optional)")
new_age = st.number_input(
    "New Age (0 means no change)",
    min_value=0,
    step=1
)
new_condition = st.text_input("New Medical Condition (Optional)")

# Step 3: Update button
if st.button("Update Patient"):

    # Prepare only the fields that need updating
    updates = {}

    if new_name.strip():
        updates["name"] = new_name.strip()

    if new_age > 0:
        updates["age"] = new_age

    if new_condition.strip():
        updates["condition"] = new_condition.strip()

    if not updates:
        st.warning("Please enter at least one field to update.")

    else:
        try:
            response = requests.patch(
                f"{API_URL}/patients/{update_id}",
                json=updates,
                timeout=5
            )

            if response.status_code == 200:
                st.success("Patient updated successfully!")
                st.json(response.json())

            elif response.status_code == 404:
                st.warning("Patient not found!")

            else:
                st.error(
                    f"Update failed: {response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Backend connection failed: {e}")



# Step 8: Delete Patient
st.subheader("Delete Patient")

# Step 1: Enter patient ID
delete_id = st.number_input(
    "Enter Patient ID to Delete",
    min_value=1,
    step=1,
    key="delete_patient_id"
)

# Step 2: Confirm deletion
confirm_delete = st.checkbox(
    "I confirm that I want to delete this patient."
)

# Step 3: Delete button
if st.button("Delete Patient"):

    if not confirm_delete:
        st.warning("Please confirm before deleting.")

    else:
        try:
            response = requests.delete(
                f"{API_URL}/patients/{delete_id}",
                timeout=5
            )

            if response.status_code == 204:
                st.success("Patient deleted successfully!")

            elif response.status_code == 404:
                st.warning("Patient not found!")

            else:
                st.error(
                    f"Deletion failed: {response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Backend connection failed: {e}")
