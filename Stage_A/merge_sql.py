import os

# --- Configuration & Path Setup ---
# Get the root directory where this script is located (Stage_A folder)
root_dir = os.path.dirname(os.path.abspath(__file__))

# Define the exact relative paths for each file based on the directory structure.
# The order is strictly maintained to prevent Foreign Key constraint violations.
files_to_merge = [
    os.path.join(root_dir, 'manualInserts', 'DEPARTMENTS.sql'),
    os.path.join(root_dir, 'mockarooFiles', 'PATIENTS.sql'),
    os.path.join(root_dir, 'mockarooFiles', 'MEDICATIONS.sql'),
    os.path.join(root_dir, 'mockarooFiles', 'STAFF.sql'),
    os.path.join(root_dir, 'Programming', 'ROOMS.sql'),
    os.path.join(root_dir, 'Programming', 'BEDS.sql'),
    os.path.join(root_dir, 'Programming', 'VISITS.sql'),
    os.path.join(root_dir, 'Programming', 'INVOICES.sql'),
    os.path.join(root_dir, 'Programming', 'APPOINTMENTS.sql'),
    os.path.join(root_dir, 'Programming', 'INPATIENT_ADMISSIONS.sql'),
    os.path.join(root_dir, 'Programming', 'PRESCRIPTIONS.sql')
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