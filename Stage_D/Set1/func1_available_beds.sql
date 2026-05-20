-- ==============================================================================
-- Function: get_available_beds
-- Description: Retrieves the total number of currently available (unoccupied) 
--              beds in the hospital.
-- ==============================================================================

CREATE OR REPLACE FUNCTION get_available_beds(p_dept_id INT)
RETURNS INT AS $$
DECLARE
    v_dept_exists BOOLEAN;
    v_total_beds INT := 0;
    v_occupied_beds INT := 0;
    v_bed_record RECORD;
    v_is_occupied INT;
    
    -- Explicit cursor to get all beds in the department
    c_beds CURSOR FOR 
        SELECT b.Bed_ID 
        FROM BEDS b
        JOIN ROOMS r ON b.Room_ID = r.Room_ID
        WHERE r.Department_ID = p_dept_id;
BEGIN
    -- Check if department exists
    SELECT EXISTS(SELECT 1 FROM DEPARTMENTS WHERE Department_ID = p_dept_id) INTO v_dept_exists;
    
    IF NOT v_dept_exists THEN
        RAISE EXCEPTION 'Department ID % not found.', p_dept_id;
    END IF;
    
    OPEN c_beds;
    
    -- Loop through all beds using the cursor
    LOOP
        FETCH c_beds INTO v_bed_record;
        EXIT WHEN NOT FOUND;
        
        v_total_beds := v_total_beds + 1;
        
        -- Check if current bed is occupied (Discharge_Date is null or in future)
        SELECT COUNT(*) INTO v_is_occupied
        FROM INPATIENT_ADMISSIONS
        WHERE Bed_ID = v_bed_record.Bed_ID 
          AND (Discharge_Date IS NULL OR Discharge_Date > CURRENT_DATE);
          
        IF v_is_occupied > 0 THEN
            v_occupied_beds := v_occupied_beds + 1;
        END IF;
    END LOOP;
    
    CLOSE c_beds;
    
    -- Return available beds
    RETURN v_total_beds - v_occupied_beds;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'An error occurred: %', SQLERRM;
        RETURN -1;
END;
$$ LANGUAGE plpgsql;