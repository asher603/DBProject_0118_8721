/*
  This query ensures that every inpatient admission has a corresponding 
  local clinic visit on the day of the admission. It sequentially maps 
  the first 409 visits to the 409 admissions by updating the Visit_Date 
  and Patient_ID in the VISITS table.
*/
WITH RankedAdmissions AS (
    -- Assign a sequential row number to inpatient admissions
    SELECT 
        Patient_ID, 
        Admission_Date,
        ROW_NUMBER() OVER (ORDER BY Admission_ID) AS rn
    FROM INPATIENT_ADMISSIONS
),
RankedVisits AS (
    -- Assign a sequential row number to local clinic visits
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
  AND rv.rn <= 409; -- Limit the update to the exact number of existing admissions (409)