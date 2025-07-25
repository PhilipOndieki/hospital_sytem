from queue import PriorityQueue

from queue import PriorityQueue

# Queue of patients prioritized by emergency status and admission time
patients_queue = PriorityQueue()  # (priority, admission_time, patient_id)

# Dictionary to store patient records using patient ID as key
patient_records = {}  # { patient_id: Patient }

# List of Doctor objects
doctors = []  # list of Doctor objects

# Set of available hospital room numbers (100 to 199)
available_rooms = set(range(100, 200))  # room numbers from 100 to 199

# Admin credentials (username: admin, password: admin123)
ADMIN_CREDENTIALS = {
    "admin": "admin123"
}


# Search for a doctor by name
def find_doctor_by_name(name):
    for doctor in doctors:
        if doctor.name.lower() == name.lower():
            return doctor
    return None

