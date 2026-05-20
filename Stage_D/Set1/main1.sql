-- ==============================================================================
-- Main Program: Set 1
-- Description: An anonymous DO block that executes the discharge_patient 
--              procedure and verifies the updated count of available beds.
-- ==============================================================================

DO $$
DECLARE
    v_dept_id INT := 1;
    v_admission_id INT := 999;
    v_beds_before INT;
    v_beds_after INT;
BEGIN
    -- 1. Call the function before DML
    v_beds_before := get_available_beds(v_dept_id);
    RAISE NOTICE 'BEFORE: Department % has % available beds.', v_dept_id, v_beds_before;
    
    -- 2. Call the procedure to discharge a patient (DML UPDATE)
    CALL discharge_patient(v_admission_id);
    RAISE NOTICE 'ACTION: Patient from admission % discharged.', v_admission_id;
    
    -- 3. Call the function after DML to prove it worked
    v_beds_after := get_available_beds(v_dept_id);
    RAISE NOTICE 'AFTER: Department % now has % available beds.', v_dept_id, v_beds_after;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'An error occurred during the process: %', SQLERRM;
END;
$$;