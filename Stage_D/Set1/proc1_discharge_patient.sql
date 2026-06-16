-- ==============================================================================
-- Procedure: discharge_patient
-- Description: Discharges an inpatient by setting their discharge date,
--              so that his bed will now be considered available for new patients.
-- ==============================================================================

CREATE OR REPLACE PROCEDURE discharge_patient(p_admission_id INT)
LANGUAGE plpgsql AS $$
DECLARE


    v_exists INT;
BEGIN
    -- Implicit cursor to check if the admission exists
    SELECT 1 INTO v_exists 
    FROM INPATIENT_ADMISSIONS 
    WHERE Admission_ID = p_admission_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Admission ID % does not exist.', p_admission_id;
    END IF;

    -- DML Command: Update discharge date to today
    UPDATE INPATIENT_ADMISSIONS
    SET Discharge_Date = CURRENT_DATE
    WHERE Admission_ID = p_admission_id;
    
END;
$$;