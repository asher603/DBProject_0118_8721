-- ==============================================================================
-- Trigger1
-- Trigger & Observer Function: trg_patient_update / set_last_updated
-- Description: Automatically injects the exact current timestamp into the 
--              Last_Updated column whenever a patient's record is modified.
-- ==============================================================================

-- The observer function to automatically update the timestamp
CREATE OR REPLACE FUNCTION set_last_updated()
RETURNS TRIGGER AS $$
BEGIN
    -- Inject the current exact time into the row before it saves
    NEW.Last_Updated := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger definition executing before UPDATE on PATIENTS
CREATE TRIGGER trg_patient_update
BEFORE UPDATE ON PATIENTS
FOR EACH ROW
EXECUTE FUNCTION set_last_updated();




-- ==============================================================================
-- Trigger2
-- Trigger & Observer Function: trg_validate_appointment / validate_appointment_date
-- Description: Validates new appointments prior to insertion, raising an 
--              exception if the scheduled date is in the past.
-- ==============================================================================

-- The observer function to validate appointment scheduling dates
CREATE OR REPLACE FUNCTION validate_appointment_date()
RETURNS TRIGGER AS $$
BEGIN
    -- Prevent scheduling an appointment in the past using dynamic CURRENT_DATE
    IF NEW.Appointment_Date < CURRENT_DATE THEN
        RAISE EXCEPTION 'Validation Failed: Cannot schedule an appointment in the past (Date: %).', NEW.Appointment_Date;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger definition executing before INSERT on APPOINTMENTS
CREATE TRIGGER trg_validate_appointment
BEFORE INSERT ON APPOINTMENTS
FOR EACH ROW
EXECUTE FUNCTION validate_appointment_date();