import csv
import random
from datetime import timedelta, date
import os

# --- Configuration ---
# Set the directory to where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

START_DT = date(2022, 1, 1)
END_DT = date(2026, 1, 1)

DEPARTMENTS_LIST = [
    (1, 'Cardiology'), (2, 'Neurology'), (3, 'Pediatrics'), 
    (4, 'Orthopedics'), (5, 'Emergency'), (6, 'Internal Medicine')
]

def random_date(start_date, end_date):
    """Generates a random date between two date objects."""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    if days_between_dates <= 0: return start_date
    return start_date + timedelta(days=random.randrange(days_between_dates))

def create_csv(filename, headers, data):
    """Helper function to write data rows to a CSV file in the script's directory."""
    # Build the full absolute path
    file_path = os.path.join(script_dir, filename)
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"Successfully created: {file_path}")

# --- Generation ---

# 1. DEPARTMENTS.CSV
create_csv('DEPARTMENTS.csv', ['Department_ID', 'Department_Name'], DEPARTMENTS_LIST)

# 2. INPATIENT_ADMISSIONS.CSV
admissions_data = []
for i in range(1, 501):
    adm_date = random_date(START_DT, END_DT)
    dis_date = adm_date + timedelta(days=random.randint(1, 20))
    # Columns: Admission_ID, Admission_Date, Discharge_Date, Patient_ID, Bed_ID
    admissions_data.append([i, adm_date, dis_date, random.randint(1, 500), random.randint(1, 500)])

create_csv('INPATIENT_ADMISSIONS.csv', 
           ['Admission_ID', 'Admission_Date', 'Discharge_Date', 'Patient_ID', 'Bed_ID'], 
           admissions_data)

print(f"\nDone! All files generated in: {script_dir}")