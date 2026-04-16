# Database Project - Stage A
## System Name: MediFlow HMS (Hospital Management System)

**Student 1 Name:** Asher Abensour  
**Student 2 Name:** Shimon Khakshour

---

## Table of Contents
1. [Introduction](#introduction)
2. [UI Characterization](#ui-characterization)
3. [Database Design (ERD & DSD)](#database-design)
4. [Data Dictionary](#data-dictionary)
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

### Data Dictionary
This section outlines the purpose, fields, and structural relationships of every table within the database.

#### 1. DEPARTMENTS
**Purpose:** Stores information about the different hospital departments.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Department_ID` | **PK** | Unique identifier for the department. |
| `Department_Name` | Attribute | Name of the hospital department. |

**Relationships:** One-to-Many with `STAFF` and `ROOMS`.

#### 2. STAFF
**Purpose:** Manages hospital employees, including doctors, nurses, and administrative staff.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Employee_ID` | **PK** | Unique identifier for the employee. |
| `First_Name` | Attribute | Employee's first name. |
| `Last_Name` | Attribute | Employee's last name. |
| `Role` | Attribute | Job title or medical role. |
| `Department_ID` | **FK** | Links the employee to a specific department. |

**Relationships:** Many-to-One with `DEPARTMENTS`. One-to-Many with `APPOINTMENTS` and `VISITS`.

#### 3. ROOMS
**Purpose:** Details the physical rooms available within the hospital's departments.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Room_ID` | **PK** | Unique identifier for the room. |
| `Room_Number` | Attribute | Physical room number. |
| `Room_Type` | Attribute | Classification of the room (e.g., Surgery, Ward). |
| `Department_ID` | **FK** | Links the room to its designated department. |

**Relationships:** Many-to-One with `DEPARTMENTS`. One-to-Many with `BEDS` and `APPOINTMENTS`.

#### 4. BEDS
**Purpose:** Tracks individual beds located within specific hospital rooms.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Bed_ID` | **PK** | Unique identifier for the bed. |
| `Bed_Number` | Attribute | Specific number or identifier of the bed. |
| `Room_ID` | **FK** | Links the bed to the room it is located in. |

**Relationships:** Many-to-One with `ROOMS`. One-to-Many with `INPATIENT_ADMISSIONS`.

#### 5. PATIENTS
**Purpose:** Core table storing demographics and contact information for all registered patients.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Patient_ID` | **PK** | Unique identifier for the patient. |
| `First_Name` | Attribute | Patient's first name. |
| `Last_Name` | Attribute | Patient's last name. |
| `Date_Of_Birth` | Attribute | Patient's birth date. |
| `Phone_Number` | Attribute | Contact phone number. |
| `Address` | Attribute | Residential address. |

**Relationships:** One-to-Many with `APPOINTMENTS`, `VISITS`, `INPATIENT_ADMISSIONS`, and `INVOICES`.

#### 6. APPOINTMENTS
**Purpose:** Manages scheduled future consultations between patients and staff.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Appointment_ID` | **PK** | Unique identifier for the scheduled appointment. |
| `Appointment_Date` | Attribute | Date and time of the appointment. |
| `Patient_ID` | **FK** | Links to the patient who booked the appointment. |
| `Employee_ID` | **FK** | Links to the assigned medical staff member. |
| `Room_ID` | **FK** | Links to the room where the appointment will take place. |

**Relationships:** Many-to-One with `PATIENTS`, `STAFF`, and `ROOMS`.

#### 7. VISITS
**Purpose:** Logs actual medical encounters, linking patients to the attending staff and recording the diagnosis.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Visit_ID` | **PK** | Unique identifier for the visit event. |
| `Visit_Date` | Attribute | Date the visit occurred. |
| `Diagnosis` | Attribute | Medical conclusion or findings. |
| `Patient_ID` | **FK** | Links to the visited patient. |
| `Employee_ID` | **FK** | Links to the attending staff member. |

**Relationships:** Many-to-One with `PATIENTS` and `STAFF`. One-to-Many with `PRESCRIPTIONS`.

#### 8. INPATIENT_ADMISSIONS
**Purpose:** Tracks hospital stays, logging when a patient is admitted to and discharged from a specific bed.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Admission_ID` | **PK** | Unique identifier for the admission record. |
| `Admission_Date` | Attribute | Date the patient was admitted. |
| `Discharge_Date` | Attribute | Date the patient was discharged. |
| `Patient_ID` | **FK** | Links to the admitted patient. |
| `Bed_ID` | **FK** | Links to the specific bed assigned. |

**Relationships:** Many-to-One with `PATIENTS` and `BEDS`.

#### 9. INVOICES
**Purpose:** Handles billing details and tracks financial charges for patient services.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Invoice_ID` | **PK** | Unique identifier for the invoice. |
| `Total_Amount` | Attribute | Total cost billed to the patient. |
| `Billing_Date` | Attribute | Date the invoice was generated. |
| `Patient_ID` | **FK** | Links to the billed patient. |

**Relationships:** Many-to-One with `PATIENTS`.

#### 10. MEDICATIONS
**Purpose:** A catalog dictionary of all available medicines and drugs in the pharmacy.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Medication_ID` | **PK** | Unique identifier for the medicine. |
| `Medication_Name` | Attribute | The generic or brand name of the drug. |

**Relationships:** One-to-Many with `PRESCRIPTIONS`.

#### 11. PRESCRIPTIONS
**Purpose:** Connects a specific patient visit to prescribed medications and their dosages.
| Field Name | Role | Description |
| :--- | :--- | :--- |
| `Prescription_ID` | **PK** | Unique identifier for the prescription record. |
| `Dosage` | Attribute | Prescribed amount and instructions. |
| `Visit_ID` | **FK** | Links the prescription to the specific medical visit. |
| `Medication_ID` | **FK** | Links to the specific medication prescribed. |

**Relationships:** Many-to-One with `VISITS` and `MEDICATIONS`.

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