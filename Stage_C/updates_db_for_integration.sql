WITH RankedAdmissions AS (
    SELECT 
        Patient_ID, 
        Admission_Date,
        ROW_NUMBER() OVER (ORDER BY Admission_ID) AS rn
    FROM INPATIENT_ADMISSIONS
),
RankedVisits AS (
    SELECT 
        Visit_ID,
        ROW_NUMBER() OVER (ORDER BY Visit_ID) AS rn
    FROM VISITS
)
UPDATE VISITS v
SET 
    Patient_ID = a.Patient_ID,
    Visit_Date = a.Admission_Date
FROM RankedVisits rv
JOIN RankedAdmissions a ON rv.rn = a.rn
WHERE v.Visit_ID = rv.Visit_ID
  AND rv.rn <= 409;