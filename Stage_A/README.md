# Database Project - Stage A
## System Name: MediFlow HMS (Hospital Management System)

**Student 1 Name:** Asher Abensour  
**Student 2 Name:** Shimon Khakshour

---

## Table of Contents
1. [Introduction](#introduction)
2. [UI Characterization](#ui-characterization)
3. [Database Design (ERD & DSD)](#database-design)
4. [Data Population Methods](#data-population-methods)
5. [Backup and Recovery](#backup-and-recovery)

---

## Introduction
**MediFlow HMS** is a comprehensive Hospital Management System designed to streamline medical and administrative workflows. The system follows a **Top-Down** approach, where business requirements and user interface designs dictated the underlying database structure. 

**Core Functionality:**
* **Patient Management:** Comprehensive tracking of registration, personal details, and medical history.
* **Staff Coordination:** Managing medical personnel roles and department assignments.
* **Inpatient Logistics:** Real-time tracking of room and bed occupancy across different hospital wards.
* **Clinical Records:** Documenting visits, diagnoses, and medical prescriptions.
* **Financial Management:** Generating invoices and managing billing for medical services.

---

## UI Characterization
The system interface was meticulously characterized using **Google AI Studio**. Each screen was designed to represent a core functional module of the hospital, ensuring that the database supports all necessary data entry and retrieval points.

**Characterization Link:** [https://ai.studio/apps/b3ae05ac-49e8-4a7c-ac85-7703f4a17ebc](https://ai.studio/apps/b3ae05ac-49e8-4a7c-ac85-7703f4a17ebc)

### System Interface Detailed Mockups:

1. **Patient Registration:** Used for onboarding new patients and maintaining personal contact information.  
   ![Patient Registration](./images/UI_images/patience.png)

2. **Staff Directory:** A central hub for managing doctors, nurses, and administrative staff, including their specializations and status.  
   ![Staff Directory](./images/UI_images/staff_directory.png)

3. **Appointment & Room Scheduling:** Manages the scheduling of patient consultations and assigns them to specific doctors and rooms.  
   ![Appointments](./images/UI_images/appointments.png)

4. **Visit & Medical Records:** Facilitates the recording of visit IDs, diagnoses, and detailed clinical notes for each patient encounter.  
   ![Medical Records](./images/UI_images/medical_records.png)

5. **Pharmacy & Prescriptions:** Handles the issuance of medical prescriptions, including medication names, dosages, and instructions.  
   ![Pharmacy](./images/UI_images/pharmacy.png)

6. **Inpatient Ward Management:** Provides a real-time overview of ward capacity (ICU, Maternity, etc.) and current bed occupancy.  
   ![Wards](./images/UI_images/wards.png)

7. **Billing & Invoices:** Manages the financial aspect, generating invoices based on patient services and tracking payment status.  
   ![Billing](./images/UI_images/billing.png)

---

## Database Design
The database was designed using **ERD Plus** and is normalized to **3NF** to ensure data integrity.

### Entities and Attributes:
The system consists of 11 primary entities:
* **Patients**: `Patient_ID`, `First_Name`, `Last_Name`, `Date_Of_Birth`, `Phone_Number`, and `Address`.
* **Departments**: `Department_ID` and `Department_Name`.
* **Staff**: `Employee_ID`, `First_Name`, `Last_Name`, and `Role`.
* **Rooms & Beds**: `Room_ID` and `Bed_ID`.
* **Medical Events**: `Appointments`, `Visits`, and `Inpatient_Admissions`.
* **Pharmacy & Billing**: `Medications`, `Prescriptions`, and `Invoices`.

### Diagrams:
#### ERD Diagram (Conceptual)
![ERD Diagram](./images/diagrams_images/erd.png)

#### DSD Diagram (Physical Relational Schema)
![DSD Diagram](./images/diagrams_images/relational_schema.png)

---

## Data Population Methods
We utilized three distinct methods to populate the database with over 40,000 combined records:

1. **Mockaroo (folder: `mockarooFiles`):** Used to generate data for **Patients**, **Staff**, and **Medications**.
   *Example of this method:* 
   ![Mockaroo Setup](./images/data_generation_methods/from_mockaroo/generating_patients_data_using_mockaroo.png)

2. **Python Programming (folder: `Programming`):** A Python script was developed to generate data for **Rooms**, **Beds**, **Inpatient_Admissions**, **Visits**, **Invoices**, and **Prescriptions**.  
   *Example of this method:* 
   ![Python Script](./images/data_generation_methods/from_pyhton_script/generating_rooms_data_using_script.png)

3. **Data Import via CSV (folder: `DATAIMPORTFILES`):** A Python script was developed to create data for **DEPARTMENTS** and **INPATIENT_ADMISSIONS** as a csv file which was then used to create the sql file containing the insert commands.
   *Example of this method:* 
   ![Generate CSV Files](./images/data_generation_methods/from_csv/generate_csv_files.png)
   ![Convert CSV to SQL](./images/data_generation_methods/from_csv/convert_csv_to_sql.png)

**Data Volume Statistics:**
* **Patients Table**: 20,000 records.
* **Visits Table**: 20,000 records.
* **Rooms Table**: 100 records.
* **Departments Table**: 6 records.
* **Other Tables**: 500 records.

---

## Backup and Recovery
The database was fully backed up using the pgAdmin 4 Backup tool in **Custom** format to ensure data portability and integrity.

### Backup Execution:
The backup file was saved as `backup_2026_03_18.backup`.
* **pgAdmin Backup Settings:** 
![Backup Settings](./images/db_backup/backup/setting_the_options_for_the_backup.png)
* **Backup Creation Confirmation:** 
![Backup Confirmation](./images/db_backup/backup/confirnation_of_backup_creation.png)

### Restore Verification:
The restoration process was successfully performed on a separate machine within a clean test environment (`Hospital_Test`) to ensure system recoverability in case of failure.
* **Restore Success Confirmation:** 
![Restore Success](./images/db_backup/restore/restore_success.jpeg)
* **Post-Restore Data Validation:** A `SELECT` query was executed on the Patients table to verify the integrity of the restored data.
  ![Restore Verification](./images/db_backup/restore/restore_verification.jpeg)

---