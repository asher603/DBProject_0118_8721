import os
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor  # Added for dynamic dictionary row mapping
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class DatabaseManager:
    """
    A class to manage all database connections and operations for the Hospital Management System.
    Updated for Stage E to support dynamic metadata-driven CRUD and extended subprograms.
    """

    def __init__(self):
        # Fetch database credentials from environment variables securely
        self.db_config = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": os.getenv("DB_PORT", "5432")
        }
        self.connection = None
        self.connect()

    def connect(self):
        """Establish a connection to the database."""
        try:
            # Ensure no essential connection variables are missing
            if not all([self.db_config["host"], self.db_config["password"]]):
                print("Error: Missing database credentials in .env file.")
                return

            self.connection = psycopg2.connect(**self.db_config)
            print("Database connection successfully established.")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        """Close the database connection safely."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    # -------------------------------------------------------------------------
    # STAGE E STABLE GENERIC EXECUTORS (Dictionary-backed Rows)
    # -------------------------------------------------------------------------

    def fetch_all(self, query, params=None):
        """
        Execute a SELECT query and return rows as dictionaries {column_name: value}.
        Crucial for metadata-driven dynamic CRUD views.
        """
        if not self.connection or self.connection.closed:
            self.connect()
        if not self.connection:
            return []
        try:
            # RealDictCursor formats result records as Python dictionaries dynamically
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            records = cursor.fetchall()
            cursor.close()
            return records
        except Error as e:
            print(f"Error executing fetch_all query: {e}")
            return []

    def fetch_one(self, query, params=None):
        """Execute a SELECT query and return a single row record as a dictionary."""
        if not self.connection or self.connection.closed:
            self.connect()
        if not self.connection:
            return None
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            record = cursor.fetchone()
            cursor.close()
            return record
        except Error as e:
            print(f"Error executing fetch_one query: {e}")
            return None

    def execute_non_query(self, query, params=None):
        """Execute an INSERT, UPDATE, DELETE, or CALL statement with full transaction commit."""
        if not self.connection or self.connection.closed:
            self.connect()
        if not self.connection:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing non-query transaction: {e}")
            self.connection.rollback()
            raise e  # Propagate the database error exception up to the GUI alerts display

    # -------------------------------------------------------------------------
    # LEGACY / BACKWARD COMPATIBILITY EXECUTORS
    # -------------------------------------------------------------------------

    def execute_read_query(self, query, params=None):
        """Legacy tuple-based query reader retained for backward compatibility."""
        if not self.connection or self.connection.closed:
            self.connect()
        if not self.connection:
            return None, None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            records = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            cursor.close()
            return records, column_names
        except Error as e:
            print(f"Error executing read query: {e}")
            return None, None

    def execute_write_query(self, query, params=None):
        """Legacy DML writer retained for backward compatibility."""
        if not self.connection or self.connection.closed:
            self.connect()
        if not self.connection:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing write query: {e}")
            self.connection.rollback()
            return False

    # -------------------------------------------------------------------------
    # EXTENDED APPOINTMENTS & SUBPROGRAMS MODULE READERS
    # -------------------------------------------------------------------------

    def call_complete_appointment_procedure(self, appointment_id, patient_id, cost, diagnosis, medication_id=None, dosage=None):
        """
        Invoke the updated Stage D complete_appointment stored procedure safely.
        Accepts optional parameters to accommodate dynamic prescription generation.
        """
        if not self.connection or self.connection.closed:
            self.connect()
        if not self.connection:
            return False
        try:
            cursor = self.connection.cursor()
            # Updated from 4 parameters to 6 parameters to support prescription data flow
            cursor.execute("CALL complete_appointment(%s, %s, %s, %s, %s, %s);", 
                           (int(appointment_id), int(patient_id), float(cost), diagnosis, 
                            int(medication_id) if medication_id else None, 
                            dosage if dosage else None))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error executing complete_appointment procedure: {e}")
            self.connection.rollback()
            return False

    def call_get_patient_history_function(self, patient_id):
        """Invoke Stage D get_patient_history function and consume ref cursor."""
        if not self.connection or self.connection.closed:
            self.connect()
        if not self.connection:
            return None
        try:
            cursor = self.connection.cursor()
            cursor.callproc("get_patient_history", [int(patient_id)])
            ref_cursor_name = cursor.fetchone()[0]
            
            cursor.execute(f'FETCH ALL FROM "{ref_cursor_name}";')
            records = cursor.fetchall()
            
            cursor.close()
            return records
        except Exception as e:
            print(f"Error consuming get_patient_history ref cursor: {e}")
            self.connection.rollback()
            return None

    def call_get_available_beds_function(self, department_id):
        """Invoke Stage D get_available_beds database function."""
        if not self.connection or self.connection.closed:
            self.connect()
        if not self.connection:
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT get_available_beds(%s);", (int(department_id),))
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        except Exception as e:
            print(f"Error calling get_available_beds function: {e}")
            self.connection.rollback()
            return None

    def call_discharge_procedure(self, admission_id):
        """Invoke Stage D discharge_patient procedure."""
        if not self.connection or self.connection.closed:
            self.connect()
        if not self.connection:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute("CALL discharge_patient(%s);", (int(admission_id),))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error calling discharge_patient procedure: {e}")
            self.connection.rollback()
            return False
        
    def get_top_billing_patients(self):
        """Fetch patients with total combined invoice amounts greater than 1500."""
        sql = """
            SELECT 
                p.First_Name, p.Last_Name, p.Phone_Number, 
                SUM(i.Total_Amount) as Total_Billed,
                COUNT(i.Invoice_ID) as Invoice_Count
            FROM PATIENTS p
            JOIN INVOICES i ON p.Patient_ID = i.Patient_ID
            GROUP BY p.Patient_ID, p.First_Name, p.Last_Name, p.Phone_Number
            HAVING SUM(i.Total_Amount) > 1500
            ORDER BY Total_Billed DESC;
        """
        return self.fetch_all(sql)

    def get_monthly_average_stays(self):
        """Fetch average length of stay (in days) grouped by admission Year and Month."""
        sql = """
            SELECT 
                EXTRACT(YEAR FROM Admission_Date) AS Year,
                EXTRACT(MONTH FROM Admission_Date) AS Month,
                COUNT(Admission_ID) AS Total_Admissions,
                ROUND(AVG(Discharge_Date - Admission_Date), 2) AS Avg_Stay_Days
            FROM INPATIENT_ADMISSIONS
            GROUP BY EXTRACT(YEAR FROM Admission_Date), EXTRACT(MONTH FROM Admission_Date)
            ORDER BY Year DESC, Month DESC;
        """
        return self.fetch_all(sql)