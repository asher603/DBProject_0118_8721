-- Index 1: Foreign Key Index on BEDS
-- Improves performance for JOIN operations between ROOMS and BEDS.
CREATE INDEX idx_beds_room_id ON BEDS(Room_ID);

-- Index 2: Foreign Key Index on INVOICES
-- Speeds up queries and subqueries filtering by Patient_ID.
CREATE INDEX idx_invoices_patient_id ON INVOICES(Patient_ID);

-- Index 3: Date Index on VISITS
-- Optimizes queries filtering by specific dates or date ranges.
CREATE INDEX idx_visits_date ON VISITS(Visit_Date);