-- ============================================================================
-- Section 8: ROLLBACK Demonstration
-- ============================================================================

-- Display the state BEFORE the change (Screenshot requested)
SELECT Room_ID, Room_Number, Room_Type FROM ROOMS WHERE Room_ID = 1;

-- Begin the transaction and execute the UPDATE
BEGIN;

UPDATE ROOMS 
SET Room_Type = 'VIP_Temporary' 
WHERE Room_ID = 1;

-- Display the state AFTER the update, while still INSIDE the transaction (Screenshot requested)
SELECT Room_ID, Room_Number, Room_Type FROM ROOMS WHERE Room_ID = 1;

-- Cancel and revert all changes
ROLLBACK;

-- Display the state AFTER the rollback to prove the data reverted correctly (Screenshot requested)
SELECT Room_ID, Room_Number, Room_Type FROM ROOMS WHERE Room_ID = 1;


-- ============================================================================
-- Section 9: COMMIT Demonstration
-- ============================================================================

-- Display the state BEFORE the change (Screenshot requested)
SELECT Medication_ID, Medication_Name FROM MEDICATIONS WHERE Medication_ID = 1;

-- Begin the transaction and execute the UPDATE
BEGIN;

UPDATE MEDICATIONS 
SET Medication_Name = Medication_Name || ' (Updated)' 
WHERE Medication_ID = 1;

-- Display the state AFTER the update, while still INSIDE the transaction (Screenshot requested)
SELECT Medication_ID, Medication_Name FROM MEDICATIONS WHERE Medication_ID = 1;

-- Permanently save the transaction to the database
COMMIT;

-- Display the state AFTER the commit to prove the data was successfully saved (Screenshot requested)
SELECT Medication_ID, Medication_Name FROM MEDICATIONS WHERE Medication_ID = 1;

-- (Optional: Revert the dummy text to keep the database clean for development purposes)
-- UPDATE MEDICATIONS SET Medication_Name = REPLACE(Medication_Name, ' (Updated)', '') WHERE Medication_ID = 1;
