-- 1. UNIQUE Constraint: Ensures no two patients share the same phone number.
ALTER TABLE PATIENTS ADD CONSTRAINT unique_phone UNIQUE (Phone_Number);

-- Query to trigger constraint violation (For Screenshot):
-- Please input an already existing phone number into the values before running.
-- INSERT INTO PATIENTS (Patient_ID, First_Name, Last_Name, Date_Of_Birth, Phone_Number, Address)
-- VALUES (999, 'Test', 'Patient', '2000-01-01', '<INSERT_EXISTING_PHONE_HERE>', 'Tel Aviv');


-- 2. CHECK Constraint: Validates that a phone number length is at least 9 digits/characters.
ALTER TABLE PATIENTS ADD CONSTRAINT chk_phone_length CHECK (LENGTH(Phone_Number) >= 9);

-- Query to trigger constraint violation (For Screenshot):
-- INSERT INTO PATIENTS (Patient_ID, First_Name, Last_Name, Date_Of_Birth, Phone_Number, Address)
-- VALUES (998, 'Short', 'Phone', '1990-01-01', '123', 'Haifa');


-- 3. CHECK Constraint (Date Logic): In this hospital system, appointments must be from the year 2000 onwards.
ALTER TABLE APPOINTMENTS ADD CONSTRAINT chk_appointment_date CHECK (EXTRACT(YEAR FROM Appointment_Date) >= 2000);

-- Query to trigger constraint violation (For Screenshot):
-- INSERT INTO APPOINTMENTS (Appointment_ID, Appointment_Date, Patient_ID, Employee_ID, Room_ID)
-- VALUES (997, '1995-05-05', 1, 1, 1);
