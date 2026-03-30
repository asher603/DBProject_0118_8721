-- ==========================================
-- 1. First View: Local Clinic Visits 
-- ==========================================

-- Create the view for local visits
CREATE OR REPLACE VIEW v_local_clinic_visits AS
SELECT 
    v.Visit_ID,
    v.Visit_Date::TIMESTAMP AS Event_Date, -- Cast to timestamp for consistency
    p.First_Name || ' ' || p.Last_Name AS Patient_Name,
    s.First_Name || ' ' || s.Last_Name AS Staff_Name,
    v.Diagnosis
FROM VISITS v
JOIN PATIENTS p ON v.Patient_ID = p.Patient_ID
JOIN STAFF s ON v.Employee_ID = s.Employee_ID;

-- Query 1: Fetch all visits where the diagnosis includes the word 'Allergy'
SELECT * FROM v_local_clinic_visits 
WHERE Diagnosis LIKE '%Allergy%';

-- Query 2: Count of visits per staff member
SELECT Staff_Name, COUNT(Visit_ID) AS Total_Visits
FROM v_local_clinic_visits
GROUP BY Staff_Name
ORDER BY Total_Visits DESC;


-- ==========================================
-- 2. Second View: Remote Partner Treatments
-- ==========================================

-- Create the view from the partner's perspective
-- We join TREATMENT with PERSON twice: once for patient name, once for doctor name
CREATE OR REPLACE VIEW v_remote_treatments_info AS
SELECT 
    rt.treatment_date AS Event_Date,
    pers_p.firstname || ' ' || pers_p.lastname AS Patient_Name,
    pers_d.firstname || ' ' || pers_d.lastname AS Staff_Name,
    rt.patient_id
FROM remote_partner.treatment rt
JOIN remote_partner.person pers_p ON rt.patient_id = pers_p.id
JOIN remote_partner.person pers_d ON rt.doctor_id = pers_d.id;

-- Query 1: Fetch all remote treatments from 2023 onwards
SELECT * FROM v_remote_treatments_info 
WHERE Event_Date >= '2023-01-01';

-- Query 2: List of unique patients treated at the partner's facility
SELECT DISTINCT Patient_Name 
FROM v_remote_treatments_info;


-- ==========================================
-- 3. Third View: Unified Outpatient History
-- ==========================================

-- Create the integrated view combining both systems
CREATE OR REPLACE VIEW v_unified_outpatient_history AS
-- Local visits from our system
SELECT 
    p.Patient_ID, 
    p.First_Name || ' ' || p.Last_Name AS Patient_Name, 
    v.Visit_Date::TIMESTAMP AS Event_Date, 
    'Local Visit' AS Event_Type,
    s.First_Name || ' ' || s.Last_Name AS Staff_Name
FROM PATIENTS p
JOIN VISITS v ON p.Patient_ID = v.Patient_ID
JOIN STAFF s ON v.Employee_ID = s.Employee_ID

UNION ALL

-- Remote treatments from the partner's system
SELECT 
    rt.patient_id AS Patient_ID, 
    pers_p.firstname || ' ' || pers_p.lastname AS Patient_Name, 
    rt.treatment_date AS Event_Date, 
    'Remote Treatment' AS Event_Type,
    pers_d.firstname || ' ' || pers_d.lastname AS Staff_Name
FROM remote_partner.treatment rt
JOIN remote_partner.person pers_p ON rt.patient_id = pers_p.id
JOIN remote_partner.person pers_d ON rt.doctor_id = pers_d.id;

-- Query 1: Fetch the complete integrated history for a specific patient
SELECT * FROM v_unified_outpatient_history 
WHERE Patient_ID = 328308725
ORDER BY Event_Date DESC;

-- Query 2: Statistical breakdown of events by type
SELECT Event_Type, COUNT(*) AS Total_Events
FROM v_unified_outpatient_history
GROUP BY Event_Type;