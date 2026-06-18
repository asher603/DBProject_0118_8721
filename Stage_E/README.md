# Hospital Management System - Stage E (GUI)

---

## 1. Tools & Workflow
* **Language & UI Framework:** Python 3.10+ using the `customtkinter` library to build a modern, responsive Graphical User Interface.
* **Database & Driver:** Cloud-hosted PostgreSQL via **Supabase**, utilizing the `psycopg2` driver for secure, direct database communication.
* **Workflow Architecture:**
  - **CRUD Operations:** Designed full insert, read, update, and delete screens across all 11 tables using a unified auto-increment ID generation policy.
  - **Data Integration (Foreign Keys):** Implemented relational SQL `JOIN` statements across all views to display descriptive names (e.g., patient names, department names) instead of raw numeric IDs.
  - **Advanced Components Integration:** Embedded direct operational hooks to trigger complex analytical queries from Stage B, alongside the execution of transactions, stored procedures, and ref cursors from Stage D.

---

## 2. How to Run the Application

### Prerequisites
1. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```
   
   

2. Ensure your `.env` file is present in the root directory with valid Supabase credentials:
   
   ```bash
   DB_HOST=
   DB_NAME=
   DB_USER=
   DB_PASSWORD=
   DB_PORT=
   ```

### Execution
Run the following command from the terminal inside the `Stage_E` directory:

```bash
python src/main.py
```

---

## 3. Application Screenshots

### Patient Directory & Registration
![Patients View](./images/01_patients_view.png)

### Dynamic Update & Fetch Operations
![Patients Update](./images/02_patients_update.png)

### Staff Directory with Dropdown Mappings
![Staff and Departments View](./images/03_staff_view.png)

### Appointments Scheduling & Stage D Procedure
![Appointments and Visits](./images/04_outpatient_view.png)

### Drug Formulary & Inventory Management
![Pharmacy and Medications](./images/05_pharmacy_view.png)

### Financial Ledger & Invoices Registry
![Billing and Invoices](./images/06_billing_view.png)

### Executive Analytical Reports (Stage B & D Controls)
![Reports and Operations](./images/07_reports_view.png)