import random
from datetime import timedelta, date
import os

# --- Configuration: Rich Lists for realistic data ---
START_DT = date(2022, 1, 1)
END_DT = date(2026, 1, 1)

# Expanded list of medical diagnoses
DIAGNOSES = [
    'Flu', 'Covid-19', 'Migraine', 'Fracture', 'Sprain', 'Checkup', 'Diabetes Type 2', 
    'Hypertension', 'Asthma', 'Allergy', 'Bronchitis', 'Anemia', 'Pneumonia', 
    'Gastroenteritis', 'Concussion', 'Dermatitis', 'Appendicitis', 'Sinusitis', 
    'Urinary Tract Infection', 'Tonsillitis', 'Common Cold', 'Otitis Media'
]

# Diverse medical dosages
DOSAGES = [
    '5mg once daily', '10mg twice daily', '20mg once daily', '50mg twice daily',
    '100mg once daily', '250mg twice daily', '500mg every 8 hours',
    '500mg twice daily', '1000mg once daily', '2.5mg once daily', '15mg every 12 hours'
]

# Hospital department room types
ROOM_TYPES = [
    'General Ward', 'ICU', 'Emergency Room', 'Operating Theater', 'Pediatric Ward', 
    'Maternity Ward', 'Oncology Clinic', 'Cardiology Unit', 'Radiology Suite', 'Isolation Room'
]

# Set the directory to where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

def random_date(start_date, end_date):
    """Generates a random date between two date objects."""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    if days_between_dates <= 0: return start_date
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def write_sql_file(filename, table_name, columns, values):
    """Writes the generated data into a SQL INSERT file."""
    file_path = os.path.join(script_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES\n")
        for i, val_row in enumerate(values):
            line = f"({', '.join(map(str, val_row))})"
            line += ";" if i == len(values) - 1 else ",\n"
            f.write(line)

print("Starting data generation with structured logic...")

# --- 1. ROOMS: 5 floors, 20 rooms each, linked to one of 6 departments ---
rooms_data = []
room_id_counter = 1
for floor in range(1, 6): 
    for room_num in range(1, 21): 
        formatted_room_num = f"'R-{floor}{room_num:02d}'"
        r_type = f"'{random.choice(ROOM_TYPES)}'"
        dept_id = random.randint(1, 6) # Links to existing 6 departments
        rooms_data.append((room_id_counter, formatted_room_num, r_type, dept_id))
        room_id_counter += 1
write_sql_file('ROOMS.sql', 'ROOMS', ['Room_ID', 'Room_Number', 'Room_Type', 'Department_ID'], rooms_data)

# --- 2. BEDS: 500 beds total, 5 beds per room ---
beds_data = []
for i in range(1, 501):
    bed_num = f"'Bed-{i}'"
    room_id = ((i - 1) // 5) + 1 # Assigns 5 beds to each room ID sequentially
    beds_data.append((i, bed_num, room_id))
write_sql_file('BEDS.sql', 'BEDS', ['Bed_ID', 'Bed_Number', 'Room_ID'], beds_data)

# --- 3. VISITS: 20,000 records linked to Patients and Staff ---
visits_data = []
for i in range(1, 20001):
    v_date = f"'{random_date(START_DT, END_DT)}'"
    diag = f"'{random.choice(DIAGNOSES)}'"
    visits_data.append((i, v_date, diag, random.randint(1, 500), random.randint(1, 500)))
write_sql_file('VISITS.sql', 'VISITS', ['Visit_ID', 'Visit_Date', 'Diagnosis', 'Patient_ID', 'Employee_ID'], visits_data)

# --- 4. INVOICES: 20,000 billing records ---
invoices_data = []
for i in range(1, 20001):
    amount = round(random.uniform(100.0, 10000.0), 2)
    b_date = f"'{random_date(START_DT, END_DT)}'"
    invoices_data.append((i, amount, b_date, random.randint(1, 500)))
write_sql_file('INVOICES.sql', 'INVOICES', ['Invoice_ID', 'Total_Amount', 'Billing_Date', 'Patient_ID'], invoices_data)

# --- 5. APPOINTMENTS: 500 future-dated appointments ---
appointments_data = []
for i in range(1, 501):
    a_date = f"'{random_date(date(2026, 4, 1), date(2027, 1, 1))}'"
    appointments_data.append((i, a_date, random.randint(1, 500), random.randint(1, 500), random.randint(1, 100)))
write_sql_file('APPOINTMENTS.sql', 'APPOINTMENTS', ['Appointment_ID', 'Appointment_Date', 'Patient_ID', 'Employee_ID', 'Room_ID'], appointments_data)

# --- 6. PRESCRIPTIONS: 500 medication orders linked to visits ---
prescriptions_data = []
for i in range(1, 501):
    dosage = f"'{random.choice(DOSAGES)}'"
    prescriptions_data.append((i, dosage, random.randint(1, 20000), random.randint(1, 500)))
write_sql_file('PRESCRIPTIONS.sql', 'PRESCRIPTIONS', ['Prescription_ID', 'Dosage', 'Visit_ID', 'Medication_ID'], prescriptions_data)

# --- 7. INPATIENT_ADMISSIONS: 500 hospital stays with valid date logic ---
admissions_data = []
for i in range(1, 501):
    adm_date = random_date(START_DT, END_DT)
    dis_date = adm_date + timedelta(days=random.randint(1, 20)) # Discharge is always after Admission
    admissions_data.append((i, f"'{adm_date}'", f"'{dis_date}'", random.randint(1, 500), random.randint(1, 500)))
write_sql_file('INPATIENT_ADMISSIONS.sql', 'INPATIENT_ADMISSIONS', ['Admission_ID', 'Admission_Date', 'Discharge_Date', 'Patient_ID', 'Bed_ID'], admissions_data)

print(f"Success! Generated 7 SQL files in the '{script_dir}' directory.")
print("Files: ROOMS.sql, BEDS.sql, VISITS.sql, INVOICES.sql, APPOINTMENTS.sql, PRESCRIPTIONS.sql, INPATIENT_ADMISSIONS.sql")