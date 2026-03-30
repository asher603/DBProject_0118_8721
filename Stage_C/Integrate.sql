-- 1. Local Visits from your system
SELECT 
    p.Patient_ID AS Patient_ID, 
    p.First_Name || ' ' || p.Last_Name AS Patient_Name, 
    rp_pat.BloodType AS Blood_Type, -- Enriched from partner's DB
    v.Visit_Date::timestamp AS Event_Date, 
    'ביקור מקומי' AS Event_Type,
    
    -- Local Doctor details
    v.Employee_ID AS Doctor_ID,
    s.First_Name || ' ' || s.Last_Name AS Doctor_Name,
    
    -- Local Medication and Diagnosis
    m.Medication_Name AS Medication_Name,
    v.Diagnosis AS Medical_Notes
    
FROM PATIENTS p
JOIN VISITS v ON p.Patient_ID = v.Patient_ID
JOIN STAFF s ON v.Employee_ID = s.Employee_ID
-- Join with partner's patient table just to get the Blood Type
LEFT JOIN remote_partner.PATIENT rp_pat ON p.Patient_ID = rp_pat.ID
-- Join with local prescriptions
LEFT JOIN PRESCRIPTIONS rx ON v.Visit_ID = rx.Visit_ID
LEFT JOIN MEDICATIONS m ON rx.Medication_ID = m.Medication_ID
WHERE p.Patient_ID = 328308725

UNION ALL

-- 2. Local Inpatient Admissions from your system
SELECT 
    p.Patient_ID AS Patient_ID, 
    p.First_Name || ' ' || p.Last_Name AS Patient_Name, 
    rp_pat.BloodType AS Blood_Type,
    ia.Admission_Date::timestamp AS Event_Date, 
    'אשפוז מקומי' AS Event_Type,
    
    -- No specific doctor linked in Inpatient_Admissions schema
    NULL::INT AS Doctor_ID,
    NULL AS Doctor_Name,
    
    -- Admission details
    NULL AS Medication_Name,
    'שחרור: ' || ia.Discharge_Date || ' | מיטה: ' || ia.Bed_ID AS Medical_Notes
    
FROM PATIENTS p
JOIN INPATIENT_ADMISSIONS ia ON p.Patient_ID = ia.Patient_ID
LEFT JOIN remote_partner.PATIENT rp_pat ON p.Patient_ID = rp_pat.ID
WHERE p.Patient_ID = 328308725

UNION ALL

-- 3. Remote Treatments from the partner's system
SELECT 
    p.Patient_ID AS Patient_ID, 
    p.First_Name || ' ' || p.Last_Name AS Patient_Name, 
    rp_pat.BloodType AS Blood_Type, 
    rt.Treatment_Date::timestamp AS Event_Date, 
    'טיפול שותף' AS Event_Type,
    
    -- Partner's Doctor details (from their PERSON table)
    rt.Doctor_ID AS Doctor_ID,
    r_per.FirstName || ' ' || r_per.LastName AS Doctor_Name,
    
    -- Partner's Medications
    rm.M_Name AS Medication_Name,
    'טיפול במערכת מרוחקת' AS Medical_Notes
    
FROM PATIENTS p
-- Connect to partner's remote tables
JOIN remote_partner.TREATMENT rt ON p.Patient_ID = rt.Patient_ID
JOIN remote_partner.PERSON r_per ON rt.Doctor_ID = r_per.ID
JOIN remote_partner.PATIENT rp_pat ON p.Patient_ID = rp_pat.ID
-- Join with partner's medication tables
LEFT JOIN remote_partner.MEDICATIONS_GIVEN rmg ON rt.Patient_ID = rmg.Patient_ID 
    AND rt.Doctor_ID = rmg.Doctor_ID AND rt.Treatment_Date = rmg.Treatment_Date
LEFT JOIN remote_partner.MEDICATION rm ON rmg.M_ID = rm.M_ID
WHERE p.Patient_ID = 328308725

ORDER BY Event_Date DESC;
