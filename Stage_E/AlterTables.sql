-- This sql code adds sequences to the primary key columns of some tables
-- to ensure that new records can be inserted without manual ID management.
-- we alredy did this for some of the other entities in the stage d,
-- and now we did it for the some of the remaining entities.

-- 1. APPOINTMENTS
CREATE SEQUENCE appointments_id_seq;
ALTER TABLE APPOINTMENTS ALTER COLUMN Appointment_ID SET DEFAULT nextval('appointments_id_seq');
SELECT setval('appointments_id_seq', (SELECT COALESCE(MAX(Appointment_ID), 1) FROM APPOINTMENTS));

-- 2. INPATIENT_ADMISSIONS
CREATE SEQUENCE inpatient_admissions_id_seq;
ALTER TABLE INPATIENT_ADMISSIONS ALTER COLUMN Admission_ID SET DEFAULT nextval('inpatient_admissions_id_seq');
SELECT setval('inpatient_admissions_id_seq', (SELECT COALESCE(MAX(Admission_ID), 1) FROM INPATIENT_ADMISSIONS));

-- 3. PRESCRIPTIONS
CREATE SEQUENCE prescriptions_id_seq;
ALTER TABLE PRESCRIPTIONS ALTER COLUMN Prescription_ID SET DEFAULT nextval('prescriptions_id_seq');
SELECT setval('prescriptions_id_seq', (SELECT COALESCE(MAX(Prescription_ID), 1) FROM PRESCRIPTIONS));

-- 4. STAFF
CREATE SEQUENCE staff_id_seq;
ALTER TABLE STAFF ALTER COLUMN Employee_ID SET DEFAULT nextval('staff_id_seq');
SELECT setval('staff_id_seq', (SELECT COALESCE(MAX(Employee_ID), 1) FROM STAFF));

-- 5. MEDICATIONS
CREATE SEQUENCE medications_id_seq;
ALTER TABLE MEDICATIONS ALTER COLUMN Medication_ID SET DEFAULT nextval('medications_id_seq');
SELECT setval('medications_id_seq', (SELECT COALESCE(MAX(Medication_ID), 1) FROM MEDICATIONS));

-- 6. DEPARTMENTS
CREATE SEQUENCE departments_id_seq;
ALTER TABLE DEPARTMENTS ALTER COLUMN Department_ID SET DEFAULT nextval('departments_id_seq');
SELECT setval('departments_id_seq', (SELECT COALESCE(MAX(Department_ID), 1) FROM DEPARTMENTS));

-- 7. ROOMS
CREATE SEQUENCE rooms_id_seq;
ALTER TABLE ROOMS ALTER COLUMN Room_ID SET DEFAULT nextval('rooms_id_seq');
SELECT setval('rooms_id_seq', (SELECT COALESCE(MAX(Room_ID), 1) FROM ROOMS));

-- 8. BEDS
CREATE SEQUENCE beds_id_seq;
ALTER TABLE BEDS ALTER COLUMN Bed_ID SET DEFAULT nextval('beds_id_seq');
SELECT setval('beds_id_seq', (SELECT COALESCE(MAX(Bed_ID), 1) FROM BEDS));