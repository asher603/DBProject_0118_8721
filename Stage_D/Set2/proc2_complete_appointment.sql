-- ==============================================================================
-- Procedure: complete_appointment
-- Description: Marks an appointment status as 'Completed', automatically 
--              generates a new billing invoice using the auto-increment sequence,
--              and inserts a new record into the VISITS table.
-- ==============================================================================

CREATE OR REPLACE PROCEDURE complete_appointment(
    p_appointment_id INT, 
    p_patient_id INT, 
    p_cost DECIMAL,
    p_diagnosis VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_employee_id INT; -- Internal variable to hold the fetched Employee_ID
BEGIN
    -- Fetch the associated Employee_ID from the APPOINTMENTS table
    SELECT Employee_ID INTO v_employee_id 
    FROM APPOINTMENTS 
    WHERE Appointment_ID = p_appointment_id;

    -- DML Command 1: Update appointment status
    UPDATE APPOINTMENTS
    SET Status = 'Completed'
    WHERE Appointment_ID = p_appointment_id;

    -- DML Command 2: Insert a new invoice for this patient
    INSERT INTO INVOICES (Total_Amount, Billing_Date, Patient_ID)
    VALUES (p_cost, CURRENT_DATE, p_patient_id);
    
    -- DML Command 3: Insert a new visit record for this patient
    INSERT INTO VISITS (Visit_Date, Diagnosis, Patient_ID, Employee_ID)
    VALUES (CURRENT_DATE, p_diagnosis, p_patient_id, v_employee_id);
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'An error occurred during appointment completion: %', SQLERRM;
END;
$$;