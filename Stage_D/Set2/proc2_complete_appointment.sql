-- ==============================================================================
-- Procedure: complete_appointment
-- Description: Marks an appointment status as 'Completed' and automatically 
--              generates a new billing invoice using the auto-increment sequence.
-- ==============================================================================

CREATE OR REPLACE PROCEDURE complete_appointment(p_appointment_id INT, p_patient_id INT, p_cost DECIMAL)
LANGUAGE plpgsql AS $$
BEGIN
    -- DML Command 1: Update appointment status
    UPDATE APPOINTMENTS
    SET Status = 'Completed'
    WHERE Appointment_ID = p_appointment_id;

    -- DML Command 2: Insert a new invoice for this patient
    INSERT INTO INVOICES (Total_Amount, Billing_Date, Patient_ID)
    VALUES (p_cost, CURRENT_DATE, p_patient_id);
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'An error occurred during appointment completion: %', SQLERRM;
END;
$$;