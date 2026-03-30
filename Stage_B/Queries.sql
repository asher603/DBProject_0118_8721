-- ==============================================================================
-- 1. Dual Queries (4 Queries * 2 Methods = 8 Queries Total)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Query 1: Find details of patients who visited the hospital in the year 2024.
-- Future UI mapping: Filtering patients by yearly visit history for receptionists.
-- ------------------------------------------------------------------------------

-- Method 1: Using IN (Builds a list of IDs to check against)
SELECT Patient_ID, First_Name, Last_Name, Phone_Number 
FROM PATIENTS 
WHERE Patient_ID IN (
    SELECT Patient_ID 
    FROM VISITS 
    WHERE EXTRACT(YEAR FROM Visit_Date) = 2024
);

-- Method 2: Using EXISTS (More efficient, uses short-circuit logic)
SELECT Patient_ID, First_Name, Last_Name, Phone_Number 
FROM PATIENTS p
WHERE EXISTS (
    SELECT 1 
    FROM VISITS v 
    WHERE v.Patient_ID = p.Patient_ID 
      AND EXTRACT(YEAR FROM v.Visit_Date) = 2024
);

-- ------------------------------------------------------------------------------
-- Query 2: Find staff members who have more than 5 appointments in May.
-- Future UI mapping: Workload management dashboard for department heads.
-- ------------------------------------------------------------------------------

-- Method 1: Using GROUP BY and HAVING (Direct and Optimizer-friendly)
SELECT s.Employee_ID, s.First_Name, s.Last_Name, COUNT(a.Appointment_ID) AS Total_Appointments
FROM STAFF s
JOIN APPOINTMENTS a ON s.Employee_ID = a.Employee_ID
WHERE EXTRACT(MONTH FROM a.Appointment_Date) = 5
GROUP BY s.Employee_ID, s.First_Name, s.Last_Name
HAVING COUNT(a.Appointment_ID) > 5
ORDER BY Total_Appointments DESC;

-- Method 2: Using an Inline View / Derived Table (Less optimal, creates temp table in memory)
SELECT Employee_ID, First_Name, Last_Name, Total_Appointments
FROM (
    SELECT Employee_ID, COUNT(Appointment_ID) AS Total_Appointments
    FROM APPOINTMENTS
    WHERE EXTRACT(MONTH FROM Appointment_Date) = 5
    GROUP BY Employee_ID
) AS app_counts
JOIN STAFF s USING (Employee_ID)
WHERE app_counts.Total_Appointments > 5
ORDER BY Total_Appointments DESC;

-- ------------------------------------------------------------------------------
-- Query 3: Find rooms that have no beds assigned to them (Empty/Maintenance rooms).
-- Future UI mapping: Resource management screen for logistics.
-- ------------------------------------------------------------------------------

-- Method 1: Using NOT IN (Vulnerable to NULL values causing full table scans)
SELECT Room_ID, Room_Number, Room_Type
FROM ROOMS
WHERE Room_ID NOT IN (
    SELECT Room_ID 
    FROM BEDS 
    WHERE Room_ID IS NOT NULL
);

-- Method 2: Using LEFT JOIN and IS NULL (Safe, utilizes indexes efficiently)
SELECT r.Room_ID, r.Room_Number, r.Room_Type
FROM ROOMS r
LEFT JOIN BEDS b ON r.Room_ID = b.Room_ID
WHERE b.Bed_ID IS NULL;

-- ------------------------------------------------------------------------------
-- Query 4: Find the total number of hospitalizations per department in 2024.
-- Future UI mapping: Executive dashboard displaying busy departments.
-- ------------------------------------------------------------------------------

-- Method 1: Using a Correlated Subquery in SELECT (Extremely inefficient: N+1 problem)
SELECT 
    (SELECT Department_Name FROM DEPARTMENTS d WHERE d.Department_ID = r.Department_ID) AS Dept_Name,
    COUNT(ia.Admission_ID) AS Total_Admissions
FROM INPATIENT_ADMISSIONS ia
JOIN BEDS b ON ia.Bed_ID = b.Bed_ID
JOIN ROOMS r ON b.Room_ID = r.Room_ID
WHERE EXTRACT(YEAR FROM ia.Admission_Date) = 2024
GROUP BY r.Department_ID
ORDER BY Total_Admissions DESC;

-- Method 2: Using standard chained JOINs (Highly efficient, mapped in memory once)
SELECT 
    d.Department_Name,
    COUNT(ia.Admission_ID) AS Total_Admissions
FROM INPATIENT_ADMISSIONS ia
JOIN BEDS b ON ia.Bed_ID = b.Bed_ID
JOIN ROOMS r ON b.Room_ID = r.Room_ID
JOIN DEPARTMENTS d ON r.Department_ID = d.Department_ID
WHERE EXTRACT(YEAR FROM ia.Admission_Date) = 2024
GROUP BY d.Department_Name
ORDER BY Total_Admissions DESC;


-- ==============================================================================
-- 2. Advanced SELECT Queries (4 Queries)
-- ==============================================================================

-- Query 5: Patients with total combined invoice amounts greater than 1500.
-- Useful for financial warnings and billing department.
SELECT 
    p.First_Name, p.Last_Name, p.Phone_Number, 
    SUM(i.Total_Amount) as Total_Billed,
    COUNT(i.Invoice_ID) as Invoice_Count
FROM PATIENTS p
JOIN INVOICES i ON p.Patient_ID = i.Patient_ID
GROUP BY p.Patient_ID, p.First_Name, p.Last_Name, p.Phone_Number
HAVING SUM(i.Total_Amount) > 1500
ORDER BY Total_Billed DESC;

-- Query 6: Group prescribed medications during the 1st Quarter, by Month text.
-- Demonstrates TO_CHAR and EXTRACT for inventory statistics.
SELECT 
    m.Medication_Name, 
    TO_CHAR(v.Visit_Date, 'Month') AS Visit_Month,
    COUNT(pr.Prescription_ID) AS Prescriptions_Count
FROM MEDICATIONS m
JOIN PRESCRIPTIONS pr ON m.Medication_ID = pr.Medication_ID
JOIN VISITS v ON pr.Visit_ID = v.Visit_ID
WHERE EXTRACT(MONTH FROM v.Visit_Date) BETWEEN 1 AND 3
GROUP BY m.Medication_Name, TO_CHAR(v.Visit_Date, 'Month')
ORDER BY Prescriptions_Count DESC;

-- Query 7: Staff members who handled the most UNIQUE patients that have NO invoices.
-- Uses complex NOT IN nesting combined with COUNT(DISTINCT).
SELECT s.First_Name, s.Last_Name, s.Role, COUNT(DISTINCT v.Patient_ID) as Unique_Patients_Handled
FROM STAFF s
JOIN VISITS v ON s.Employee_ID = v.Employee_ID
WHERE v.Patient_ID NOT IN (
    SELECT Patient_ID FROM INVOICES
)
GROUP BY s.Employee_ID, s.First_Name, s.Last_Name, s.Role
ORDER BY Unique_Patients_Handled DESC;

-- Query 8: Average length of stay (in days) grouped by admission Year and Month.
-- Uses date arithmetic (Discharge_Date - Admission_Date).
SELECT 
    EXTRACT(YEAR FROM Admission_Date) AS Year,
    EXTRACT(MONTH FROM Admission_Date) AS Month,
    COUNT(Admission_ID) AS Total_Admissions,
    ROUND(AVG(Discharge_Date - Admission_Date), 2) AS Avg_Stay_Days
FROM INPATIENT_ADMISSIONS
GROUP BY EXTRACT(YEAR FROM Admission_Date), EXTRACT(MONTH FROM Admission_Date)
ORDER BY Year DESC, Month DESC;


-- ==============================================================================
-- 3. UPDATE Operations
-- ==============================================================================

-- Update 1: Upgrade emergency rooms to 'Intensive_Care_Unit'.
UPDATE ROOMS 
SET Room_Type = 'Intensive_Care_Unit'
WHERE Department_ID IN (
    SELECT Department_ID FROM DEPARTMENTS WHERE Department_Name LIKE '%Emergency%'
);

-- Update 2: Add a 10% penalty fee to invoices for patients with invalid phone numbers (< 10 chars).
UPDATE INVOICES 
SET Total_Amount = Total_Amount * 1.10
WHERE Patient_ID IN (
    SELECT Patient_ID FROM PATIENTS WHERE LENGTH(Phone_Number) < 10
);

-- Update 3: Archive addresses for patients who haven't visited or had an appointment since 2020.
UPDATE PATIENTS
SET Address = 'Archived Address'
WHERE Patient_ID NOT IN (
    SELECT DISTINCT Patient_ID FROM VISITS WHERE EXTRACT(YEAR FROM Visit_Date) >= 2020
)
AND Patient_ID NOT IN (
    SELECT DISTINCT Patient_ID FROM APPOINTMENTS WHERE EXTRACT(YEAR FROM Appointment_Date) >= 2020
);


-- ==============================================================================
-- 4. DELETE Operations
-- ==============================================================================

-- Delete 1: Cancel all appointments assigned to employees leaving a 'Closed Department'.
DELETE FROM APPOINTMENTS 
WHERE Employee_ID IN (
    SELECT Employee_ID FROM STAFF WHERE Department_ID = (
        SELECT Department_ID FROM DEPARTMENTS WHERE Department_Name = 'Closed Department'
    )
);

-- Delete 2: Remove bed records from rooms that belong to the 'Maintenance' department.
DELETE FROM BEDS 
WHERE Room_ID IN (
    SELECT r.Room_ID FROM ROOMS r
    JOIN DEPARTMENTS d ON r.Department_ID = d.Department_ID
    WHERE d.Department_Name = 'Maintenance'
);

-- Delete 3: Delete pre 2023 invoices for young patients (born 2008+)
DELETE FROM INVOICES
WHERE Billing_Date < TO_DATE('2023-01-01', 'YYYY-MM-DD')
AND Patient_ID IN (
    SELECT Patient_ID 
    FROM PATIENTS 
    WHERE EXTRACT(YEAR FROM Date_Of_Birth) >= 2008
);
