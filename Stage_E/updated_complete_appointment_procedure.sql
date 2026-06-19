-- ==============================================================================
-- Procedure: complete_appointment
-- Description: Marks an appointment status as 'Completed', automatically 
--              generates a new billing invoice, inserts a new record into 
--              the VISITS table, and optionally links a prescription.
-- ==============================================================================

CREATE OR REPLACE PROCEDURE complete_appointment(
    p_appointment_id INT, 
    p_patient_id INT, 
    p_cost DECIMAL,
    p_diagnosis VARCHAR,
    p_medication_id INT DEFAULT NULL, -- Optional parameter added for Stage E GUI integration
    p_dosage VARCHAR DEFAULT NULL     -- Optional parameter added for Stage E GUI integration
)
LANGUAGE plpgsql AS $$
DECLARE
    v_employee_id INT; -- Internal variable to hold the fetched Employee_ID
    v_visit_id INT;    -- Internal variable to hold the newly generated Visit_ID
BEGIN
    -- Fetch the associated Employee_ID from the APPOINTMENTS table
    SELECT Employee_ID INTO v_employee_id 
    FROM APPOINTMENTS 
    WHERE Appointment_ID = p_appointment_id;

    -- Safety check: Ensure the appointment exists
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Appointment ID % not found.', p_appointment_id;
    END IF;

    -- DML Command 1: Update appointment status to Completed
    UPDATE APPOINTMENTS
    SET Status = 'Completed'
    WHERE Appointment_ID = p_appointment_id;

    -- DML Command 2: Insert a new invoice for this patient
    INSERT INTO INVOICES (Total_Amount, Billing_Date, Patient_ID)
    VALUES (p_cost, CURRENT_DATE, p_patient_id);
    
    -- DML Command 3: Insert a new visit record and capture the generated Visit_ID
    INSERT INTO VISITS (Visit_Date, Diagnosis, Patient_ID, Employee_ID)
    VALUES (CURRENT_DATE, p_diagnosis, p_patient_id, v_employee_id)
    RETURNING Visit_ID INTO v_visit_id;

    -- DML Command 4: Insert a new prescription only if medication details are provided
    IF p_medication_id IS NOT NULL AND p_dosage IS NOT NULL THEN
        INSERT INTO PRESCRIPTIONS (Dosage, Visit_ID, Medication_ID)
        VALUES (p_dosage, v_visit_id, p_medication_id);
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error in complete_appointment execution: %', SQLERRM;
END;
$$;