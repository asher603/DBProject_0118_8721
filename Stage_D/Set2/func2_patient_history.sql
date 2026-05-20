-- ==============================================================================
-- Function: get_patient_history
-- Description: Returns a Ref Cursor containing the complete medical visit 
--              history and diagnoses for a specific patient.
-- ==============================================================================

CREATE OR REPLACE FUNCTION get_patient_history(p_patient_id INT)
RETURNS refcursor AS $$
DECLARE
    v_ref_cursor refcursor;
    v_exists BOOLEAN;
BEGIN
    -- Check if patient exists
    SELECT EXISTS(SELECT 1 FROM PATIENTS WHERE Patient_ID = p_patient_id) INTO v_exists;
    
    IF NOT v_exists THEN
        RAISE EXCEPTION 'Patient ID % not found.', p_patient_id;
    END IF;

    -- Open the ref cursor for the patient's visits
    OPEN v_ref_cursor FOR
        SELECT Visit_ID, Visit_Date, Diagnosis
        FROM VISITS
        WHERE Patient_ID = p_patient_id
        ORDER BY Visit_Date DESC;

    -- Return the cursor itself
    RETURN v_ref_cursor;
END;
$$ LANGUAGE plpgsql;