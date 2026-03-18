import os

# --- Configuration & Path Setup ---
# Get the root directory where this script is located (Stage_A folder)
root_dir = os.path.dirname(os.path.abspath(__file__))

# Define the exact relative paths for each file based on the directory structure.
# The order is strictly maintained to prevent Foreign Key constraint violations.
files_to_merge = [
    # Level 0: Independent tables (no foreign keys)
    os.path.join(root_dir, 'DataImportFiles', 'DEPARTMENTS.sql'),
    os.path.join(root_dir, 'mockarooFiles', 'PATIENTS.sql'),
    os.path.join(root_dir, 'mockarooFiles', 'MEDICATIONS.sql'),

    # Level 1: Tables depending on Level 0
    os.path.join(root_dir, 'mockarooFiles', 'STAFF.sql'),       # Depends on DEPARTMENTS
    os.path.join(root_dir, 'Programming', 'ROOMS.sql'),        # Depends on DEPARTMENTS
    os.path.join(root_dir, 'Programming', 'INVOICES.sql'),     # Depends on PATIENTS

    # Level 2: Tables depending on Level 1
    os.path.join(root_dir, 'Programming', 'BEDS.sql'),         # Depends on ROOMS
    os.path.join(root_dir, 'Programming', 'VISITS.sql'),       # Depends on PATIENTS and STAFF
    os.path.join(root_dir, 'Programming', 'APPOINTMENTS.sql'), # Depends on PATIENTS, STAFF, and ROOMS

    # Level 3: Final dependencies
    os.path.join(root_dir, 'Programming', 'PRESCRIPTIONS.sql'), # Depends on VISITS and MEDICATIONS
    os.path.join(root_dir, 'DataImportFiles', 'INPATIENT_ADMISSIONS.sql') # Depends on PATIENTS and BEDS
]

# The output file will be created in the root of Stage_A
output_file = os.path.join(root_dir, 'insertTables.sql')

print("Starting to merge SQL files...")

# --- Merging Process ---
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Write the main header for the submission file
    outfile.write("-- ==========================================\n")
    outfile.write("-- Hospital Database Full Data Insertion\n")
    outfile.write("-- Combined for Stage A submission\n")
    outfile.write("-- Student ID: 215340118\n")
    outfile.write("-- ==========================================\n\n")
    
    for file_path in files_to_merge:
        # Extract just the filename for the section headers
        filename = os.path.basename(file_path)
        
        # Check if the file exists before attempting to read it
        if os.path.exists(file_path):
            outfile.write(f"\n\n-- ==========================================\n")
            outfile.write(f"-- Data for table: {filename.replace('.sql', '')}\n")
            outfile.write(f"-- ==========================================\n\n")
            
            # Read the content of the current SQL file and append it
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
            
            print(f"[SUCCESS] Added {filename} to the merge.")
        else:
            print(f"[WARNING] File not found and skipped: {file_path}")

print(f"\nAll done! The merged file is ready at: {output_file}")