-- ==============================================================================
-- Main Program: Set 2
-- Description: An anonymous DO block that completes an appointment, generates 
--              an invoice, and iterates over the patient's history Ref Cursor.
-- ==============================================================================

DO $$
DECLARE
    v_patient_id INT := 170;
    v_appointment_id INT := 200;
    v_visit_history refcursor;
    v_visit_record RECORD;
BEGIN
    -- 1. Call Procedure (Executes multiple DMLs: UPDATE and INSERT)
    CALL complete_appointment(v_appointment_id, v_patient_id, 150.0, 'Routine Checkup');
    RAISE NOTICE 'ACTION: Appointment % completed and invoice generated.', v_appointment_id;

    -- 2. Call Function (Returns Ref Cursor)
    v_visit_history := get_patient_history(v_patient_id);

    -- 3. Loop through the returned ref cursor and print
    RAISE NOTICE '--- Patient % Visit History ---', v_patient_id;
    LOOP
        FETCH v_visit_history INTO v_visit_record;
        EXIT WHEN NOT FOUND;
        
        RAISE NOTICE 'Visit ID: %, Date: %, Diagnosis: %', 
            v_visit_record.Visit_ID, v_visit_record.Visit_Date, v_visit_record.Diagnosis;
    END LOOP;

    -- Close the cursor when done
    CLOSE v_visit_history;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'An error occurred in the main program: %', SQLERRM;
END;
$$;