-- ALTER TABLE commands for Set1
ALTER TABLE INPATIENT_ADMISSIONS ALTER COLUMN Discharge_Date DROP NOT NULL;

-- ALTER TABLE commands for Set2
-- 1st command:
ALTER TABLE APPOINTMENTS ADD COLUMN Status VARCHAR(20) DEFAULT 'Scheduled';

-- 2nd command:
CREATE SEQUENCE invoices_id_seq;
ALTER TABLE INVOICES ALTER COLUMN Invoice_ID SET DEFAULT nextval('invoices_id_seq');
SELECT setval('invoices_id_seq', (SELECT COALESCE(MAX(Invoice_ID), 1) FROM INVOICES));

-- 3rd command:
CREATE SEQUENCE visits_id_seq;
ALTER TABLE VISITS ALTER COLUMN Visit_ID SET DEFAULT nextval('visits_id_seq');
SELECT setval('visits_id_seq', (SELECT COALESCE(MAX(Visit_ID), 1) FROM VISITS));

-- ALTER TABLE commands for Trigger1
ALTER TABLE PATIENTS ADD COLUMN Last_Updated TIMESTAMP;