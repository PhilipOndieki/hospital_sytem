import json
from models import Patient, Doctor
from utils import patients_queue, patient_records, doctors, find_doctor_by_name, available_rooms, ADMIN_CREDENTIALS

# Admit a new patient and assign a room
def admit_patient():
    name = input("Enter patient name: ")
    age = int(input("Enter age: "))
    reason = input("Reason for visit: ")
    emergency = input("Is it an emergency? (y/n): ").lower() == 'y'

    if not available_rooms:
        print("❌ No rooms available right now.")
        return

    patient = Patient(name, age, reason, emergency)
    room_assigned = available_rooms.pop()
    patient.room = room_assigned

    priority = 1 if emergency else 2
    patients_queue.put((priority, patient.admission_time, patient.id))
    patient_records[patient.id] = patient
    print(f"✅ Patient admitted with ID: {patient.id}, Room: {room_assigned}")

# Discharge a patient and free up their room
def discharge_patient():
    patient_id = input("Enter patient ID to discharge: ")
    patient = patient_records.get(patient_id)
    if patient:
        patient.add_history("Discharged")
        if patient.room is not None:
            available_rooms.add(patient.room)
        del patient_records[patient_id]
        print(f"✅ {patient.name} has been discharged and Room {patient.room} is now available.")
    else:
        print("❌ Patient not found.")

# Display all admitted patients with basic details
def view_all_patients():
    if not patient_records:
        print("No patients currently admitted.")
        return
    for p in patient_records.values():
        print(f"ID: {p.id} | Name: {p.name} | Emergency: {p.emergency} | Room: {p.room} | Admitted: {p.admission_time}")

# Assign a doctor to a patient (create doctor if not already present)
def assign_doctor():
    doctor_name = input("Enter doctor name: ")
    specialty = input("Enter doctor's specialty: ")
    patient_id = input("Enter patient ID to assign: ")

    patient = patient_records.get(patient_id)
    if not patient:
        print("❌ Patient not found.")
        return

    doctor = find_doctor_by_name(doctor_name)
    if not doctor:
        doctor = Doctor(doctor_name, specialty)
        doctors.append(doctor)

    doctor.patients_queue.append(patient.id)
    patient.assigned_doctor = doctor.name
    patient.add_history(f"Assigned to Dr. {doctor.name}")
    print(f"✅ {patient.name} assigned to Dr. {doctor.name} ({doctor.specialty})")

# View detailed history of actions taken on a patient
def view_patient_history():
    patient_id = input("Enter patient ID to view history: ")
    patient = patient_records.get(patient_id)
    if not patient:
        print("❌ Patient not found.")
        return
    print(f"\n📜 History for {patient.name}:")
    for event, timestamp in patient.history:
        print(f"- {timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {event}")

def search_patients():
    term = input("Enter search term (name, doctor, reason): ").lower()
    matches = [p for p in patient_records.values()
               if term in p.name.lower() or
                  (p.assigned_doctor and term in p.assigned_doctor.lower()) or
                  term in p.reason.lower()]
    if matches:
        for p in matches:
            print(f"ID: {p.id} | Name: {p.name} | Doctor: {p.assigned_doctor} | Room: {p.room} | Reason: {p.reason}")
    else:
        print("🔍 No matching patients found.")

# Sort patients by name, admission time, or emergency status
def sort_patients():
    print("Sort by(Choose 1, 2 or 3): 1. Name  2. Admission Time  3. Emergency Status")
    choice = input("Choice: ")
    patients = list(patient_records.values())
    if choice == '1':
        patients.sort(key=lambda p: p.name)
    elif choice == '2':
        patients.sort(key=lambda p: p.admission_time)
    elif choice == '3':
        patients.sort(key=lambda p: not p.emergency)
    else:
        print("❌ Invalid choice.")
        return

    for p in patients:
        print(f"ID: {p.id} | Name: {p.name} | Emergency: {p.emergency} | Room: {p.room} | Admitted: {p.admission_time}")

# Export current patient data to a JSON file
def export_data():
    data = []
    for p in patient_records.values():
        data.append({
            'id': p.id,
            'name': p.name,
            'age': p.age,
            'reason': p.reason,
            'emergency': p.emergency,
            'room': p.room,
            'doctor': p.assigned_doctor,
            'admission_time': p.admission_time.strftime('%Y-%m-%d %H:%M:%S'),
            'history': [(e, t.strftime('%Y-%m-%d %H:%M:%S')) for e, t in p.history]
        })
    with open("patients_data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("📁 Patient data exported to patients_data.json")

def authenticate_admin():
    username = input("Username: ")
    password = input("Password: ")
    if ADMIN_CREDENTIALS.get(username) == password:
        print("✅ Login successful.")
        return True
    print("❌ Invalid credentials.")
    return False


# Main program loop for user interaction
def main():
    print("\n🔒 Admin Login Required")
    if not authenticate_admin():
        return
    
    while True:
        print("\n--- Hospital Patient Management ---")
        print("1. Admit Patient")
        print("2. Discharge Patient")
        print("3. View All Patients")
        print("4. Assign Doctor")
        print("5. View Patient History")
        print("6. Search Patients")
        print("7. Sort Patients")
        print("8. Export Data to JSON")
        print("9. Exit")

        choice = input("Enter choice: ")
        if choice == '1':
            admit_patient()
        elif choice == '2':
            discharge_patient()
        elif choice == '3':
            view_all_patients()
        elif choice == '4':
            assign_doctor()
        elif choice == '5':
            view_patient_history()
        elif choice == '6':
            search_patients()
        elif choice == '7':
            sort_patients()
        elif choice == '8':
            export_data()
        elif choice == '9':
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == '__main__':
    main()
