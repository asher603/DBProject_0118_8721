import psycopg2
from psycopg2 import Error

class DatabaseManager:
    """
    A class to manage all database connections and operations for the Hospital Management System.
    """

    def __init__(self):
        # TODO: Replace with your actual database credentials
        self.db_config = {
            "host": "localhost",
            "database": "your_database_name",
            "user": "postgres",
            "password": "your_password",
            "port": "5432"
        }
        self.connection = None
        self.connect()

    def connect(self):
        """Establish a connection to the database."""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print("Database connection successfully established.")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        """Close the database connection safely."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def execute_read_query(self, query, params=None):
        """
        Execute a SELECT query and return the fetched records along with column names.
        
        :param query: SQL query string.
        :param params: Tuple of parameters to prevent SQL injection.
        :return: Tuple containing a list of records and a list of column names.
        """
        if not self.connection or self.connection.closed:
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            records = cursor.fetchall()
            
            # Extract column names from the cursor description for dynamic UI tables
            column_names = [desc[0] for desc in cursor.description]
            
            cursor.close()
            return records, column_names
        
        except Error as e:
            print(f"Error executing read query: {e}")
            return None, None

    def execute_write_query(self, query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query.
        
        :param query: SQL query string.
        :param params: Tuple of parameters to prevent SQL injection.
        :return: Boolean indicating success or failure.
        """
        if not self.connection or self.connection.closed:
            self.connect()

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
    # SPECIFIC CRUD OPERATIONS FOR THE HOSPITAL MANAGEMENT SYSTEM
    # -------------------------------------------------------------------------

    def get_all_patients(self):
        """Retrieve all patients from the PATIENTS table."""
        query = "SELECT * FROM PATIENTS ORDER BY Patient_ID ASC;"
        return self.execute_read_query(query)

    def get_staff_with_departments(self):
        """
        Retrieve staff details along with their department names instead of department IDs.
        This satisfies the project requirement: "use foreign keys to display the actual value instead of the ID".
        """
        query = """
            SELECT 
                s.Employee_ID, 
                s.First_Name, 
                s.Last_Name, 
                s.Role, 
                d.Department_Name 
            FROM STAFF s
            JOIN DEPARTMENTS d ON s.Department_ID = d.Department_ID
            ORDER BY s.Employee_ID ASC;
        """
        return self.execute_read_query(query)

    def get_patient_by_id(self, patient_id):
        """
        Fetch a specific patient's details for the UPDATE screen.
        
        :param patient_id: The ID of the patient.
        """
        query = "SELECT * FROM PATIENTS WHERE Patient_ID = %s;"
        return self.execute_read_query(query, (patient_id,))

    def update_patient_info(self, patient_id, first_name, last_name, phone, address):
        """
        Update basic information for a specific patient.
        
        :param patient_id: The unique ID of the patient.
        :param first_name: Updated first name.
        :param last_name: Updated last name.
        :param phone: Updated phone number.
        :param address: Updated address.
        :return: True if successful, False otherwise.
        """
        query = """
            UPDATE PATIENTS 
            SET First_Name = %s, Last_Name = %s, Phone_Number = %s, Address = %s 
            WHERE Patient_ID = %s;
        """
        params = (first_name, last_name, phone, address, patient_id)
        return self.execute_write_query(query, params)