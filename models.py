import uuid
from datetime import datetime

# Represents a patient in the hospital
class Patient:
    def __init__(self, name, age, reason, emergency=False):
        self.id = str(uuid.uuid4())  # Unique identifier for each patient
        self.name = name
        self.age = age
        self.reason = reason # Reason for visit
        self.emergency = emergency # Boolean: is it an emergency case?
        self.admission_time = datetime.now() # Timestamp of admission
        self.history = [("Admitted", self.admission_time)]  # Event log
        self.assigned_doctor = None 
        self.room = None  # Room assigned upon admission

    def add_history(self, action):
         # Room assigned upon admission
        self.history.append((action, datetime.now()))

# Represents a doctor in the hospital
class Doctor:
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty
        self.patients_queue = []  # # List of patient IDs (FIFO queue)

