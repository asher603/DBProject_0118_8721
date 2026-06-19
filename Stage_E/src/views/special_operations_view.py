import customtkinter as ctk
from tkinter import ttk, messagebox

class SpecialOperationsView(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_back_click):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_back_click = on_back_click

        # Top navigation bar hosting the persistent back button to return to the main hub
        self.top_nav_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_nav_bar.pack(fill="x", padx=20, pady=(15, 0))

        self.btn_back = ctk.CTkButton(self.top_nav_bar, text="← Back to Main Menu", command=self.on_back_click, fg_color="gray", width=160)
        self.btn_back.pack(side="left")

        # Workspace split into structural tabbed action items
        self.tab_panel = ctk.CTkTabview(self)
        self.tab_panel.pack(fill="both", expand=True, padx=20, pady=10)

        # 4. RESTRUCTURED TABS: Tab 1 runs Clinical Bed Management Tools; Tab 2 runs Analytical Reports
        self.tab_beds_admissions = self.tab_panel.add("Admissions & Bed Management (Stage D Subprograms)")
        self.tab_queries = self.tab_panel.add("Complex Diagnostic Analytics (Stage B Queries)")

        self.setup_beds_admissions_interface()
        self.setup_queries_interface()

    # ----------------------------------------------------------------------
    # TAB 1: STAGE D SUBPROGRAMS (GET AVAILABLE BEDS & DISCHARGE)
    # ----------------------------------------------------------------------
    def setup_beds_admissions_interface(self):
        # Split into upper section (Function lookup) and lower section (Procedure call)
        
        # --- SECTION A: FUNCTION (get_available_beds) ---
        func_frame = ctk.CTkLabel(self.tab_beds_admissions, text="") # Structural wrapping frame anchor
        func_card = ctk.CTkFrame(self.tab_beds_admissions, corner_radius=12)
        func_card.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(func_card, text="Check Department Available Beds Capacity (get_available_beds function)", 
                     font=("Arial", 13, "bold"), text_color="cyan").pack(anchor="w", padx=20, pady=10)
        
        input_row = ctk.CTkFrame(func_card, fg_color="transparent")
        input_row.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(input_row, text="Select Target Medical Department:").pack(side="left", padx=5)
        
        # Pull department options from database dynamically
        self.dept_mapping = self.fetch_departments_list()
        self.combo_dept = ctk.CTkComboBox(input_row, values=list(self.dept_mapping.keys()), state="readonly", width=300)
        self.combo_dept.pack(side="left", padx=10)
        
        btn_check_beds = ctk.CTkButton(input_row, text="Query Available Capacity", command=self.run_get_available_beds_call, fg_color="blue")
        btn_check_beds.pack(side="left", padx=10)

        self.lbl_beds_result = ctk.CTkLabel(func_card, text="Result Status: Awaiting Input Query...", font=("Arial", 12, "italic"), text_color="yellow")
        self.lbl_beds_result.pack(anchor="w", padx=20, pady=(5, 15))

        # --- SECTION B: PROCEDURE (discharge_patient) ---
        proc_card = ctk.CTkFrame(self.tab_beds_admissions, corner_radius=12)
        proc_card.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(proc_card, text="Process Hospital Discharge Protocol (discharge_patient procedure)", 
                     font=("Arial", 13, "bold"), text_color="orange").pack(anchor="w", padx=20, pady=10)
        
        proc_row = ctk.CTkFrame(proc_card, fg_color="transparent")
        proc_row.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(proc_row, text="Enter Target Inpatient Admission ID Key:").pack(side="left", padx=5)
        self.entry_admission_id = ctk.CTkEntry(proc_row, placeholder_text="e.g. 401", width=180)
        self.entry_admission_id.pack(side="left", padx=10)
        
        btn_discharge = ctk.CTkButton(proc_row, text="⚡ Commit Patient Discharge", command=self.run_discharge_patient_call, fg_color="purple", hover_color="#5D207A")
        btn_discharge.pack(side="left", padx=10)
        
        ctk.CTkLabel(proc_card, text="*Note: Executing this subprogram logs the current timestamp onto the target system discharge log record and releases the bed.", 
                     font=("Arial", 11, "italic"), text_color="gray").pack(anchor="w", padx=20, pady=(5, 15))

    def fetch_departments_list(self):
        try:
            rows = self.db_manager.fetch_all("SELECT Department_ID, Department_Name FROM DEPARTMENTS ORDER BY Department_Name")
            return {r["department_name"]: r["department_id"] for r in rows}
        except:
            return {"Emergency Medicine": 1}

    def run_get_available_beds_call(self):
        dept_name = self.combo_dept.get()
        dept_id = self.dept_mapping.get(dept_name)
        if not dept_id:
            messagebox.showwarning("Input Missing", "Kindly select a hospital department partition from the option drop list menu.")
            return
            
        # Execute the database linkage function call logic securely
        try:
            res = self.db_manager.call_get_available_beds_function(dept_id)
            self.lbl_beds_result.configure(text=f"Result Status: Confirmed [{res}] unallocated/available beds remaining inside {dept_name} sector.", text_color="lightgreen")
        except Exception as e:
            messagebox.showerror("Execution Failure", str(e))

    def run_discharge_patient_call(self):
        adm_id_txt = self.entry_admission_id.get().strip()
        if not adm_id_txt or not adm_id_txt.isdigit():
            messagebox.showerror("Validation Failure", "A clean valid numeric Admission ID surrogate value input criteria is required.")
            return
            
        try:
            success = self.db_manager.call_discharge_procedure(int(adm_id_txt))
            if success:
                messagebox.showinfo("Success", f"Discharge logs committed. Patient admission tracker ID [{adm_id_txt}] updated successfully.")
                self.entry_admission_id.delete(0, "end")
            else:
                messagebox.showerror("Error", "Server rejected procedure execution block. Review server trace parameters.")
        except Exception as e:
            messagebox.showerror("Execution Aborted", str(e))

    # ----------------------------------------------------------------------
    # TAB 2: STAGE B COMPLEX QUERIES INTEGRATION
    # ----------------------------------------------------------------------
    def setup_queries_interface(self):
        ctk.CTkLabel(self.tab_queries, text="Select Analytics Report Query to Run:", font=("Arial", 14, "bold")).pack(anchor="w", padx=20, pady=10)
        
        self.query_dropdown = ctk.CTkOptionMenu(self.tab_queries, values=["Report 1: Top Revenue Billing Patients Directory", "Report 2: Highly Active Patient Load Distributions (Year 2024)"], width=450)
        self.query_dropdown.pack(anchor="w", padx=20, pady=5)

        btn_run = ctk.CTkButton(self.tab_queries, text="Execute Complex Reporting Analytical Scan", command=self.run_stage_b_query, fg_color="blue", font=("Arial", 13, "bold"))
        btn_run.pack(anchor="w", padx=20, pady=10)

        self.txt_output = ctk.CTkTextbox(self.tab_queries, font=("Courier New", 12), width=900, height=350)
        self.txt_output.pack(fill="both", expand=True, padx=20, pady=10)

    def run_stage_b_query(self):
        choice = self.query_dropdown.get()
        self.txt_output.delete("1.0", "end")

        if "Report 1" in choice:
            sql = """
                SELECT p.Patient_ID, p.First_Name, p.Last_Name, SUM(i.Total_Amount) as accumulated_spend
                FROM PATIENTS p 
                JOIN INVOICES i ON p.Patient_ID = i.Patient_ID
                GROUP BY p.Patient_ID, p.First_Name, p.Last_Name
                HAVING SUM(i.Total_Amount) > 100
                ORDER BY accumulated_spend DESC
            """
            header = f"{'ID':<8}{'First Name':<15}{'Last Name':<15}{'Total Paid ($)':<15}\n" + "-"*55 + "\n"
        else:
            sql = """
                SELECT p.Patient_ID, p.First_Name, p.Last_Name, COUNT(ia.Admission_ID) as hospitalization_count
                FROM PATIENTS p
                JOIN INPATIENT_ADMISSIONS ia ON p.Patient_ID = ia.Patient_ID
                WHERE ia.Admission_Date >= '2024-01-01'
                GROUP BY p.Patient_ID, p.First_Name, p.Last_Name
                ORDER BY hospitalization_count DESC
            """
            header = f"{'ID':<8}{'First Name':<15}{'Last Name':<15}{'Hospital Stays':<15}\n" + "-"*55 + "\n"

        try:
            rows = self.db_manager.fetch_all(sql)
            self.txt_output.insert("end", header)
            for r in rows:
                items = list(r.values())
                line = f"{str(items[0]):<8}{str(items[1]):<15}{str(items[2]):<15}{str(items[3]):<15}\n"
                self.txt_output.insert("end", line)
        except Exception as e:
            self.txt_output.insert("end", f"SQL Operational Failure Encountered:\n{str(e)}")


# --------------------------------------------------------------------------
# SUB-COMPONENT POPUP DIALOG WINDOW (RETAINED WIZARD SUBPROGRAM LINK)
# --------------------------------------------------------------------------
class PopupCompletionWindow(ctk.CTkToplevel):
    def __init__(self, parent, appt_id, patient_id, patient_name, db_manager, on_done_callback):
        super().__init__(parent)
        self.db_manager = db_manager
        self.appt_id = appt_id
        self.patient_id = patient_id
        self.on_done_callback = on_done_callback

        self.title("Execute Appointment Closing Procedures Workflow")
        self.geometry("460x580")
        self.transient(parent)
        self.grab_set()

        ctk.CTkLabel(self, text=f"Logging Operational Closing for:\n{patient_name}", font=("Arial", 15, "bold"), text_color="cyan").pack(pady=15)

        ctk.CTkLabel(self, text="Billing Ledger Base Fee Total Amount ($):").pack(anchor="w", padx=45, pady=(5, 0))
        self.entry_cost = ctk.CTkEntry(self, width=370)
        self.entry_cost.insert(0, "150.00")
        self.entry_cost.pack(pady=5)

        ctk.CTkLabel(self, text="Official Medical Diagnosis Summary:").pack(anchor="w", padx=45, pady=(5, 0))
        self.txt_diag = ctk.CTkTextbox(self, width=370, height=90)
        self.txt_diag.pack(pady=5)

        ctk.CTkFrame(self, height=2, width=380, fg_color="gray").pack(pady=15)

        self.check_var = ctk.StringVar(value="off")
        self.chk_include = ctk.CTkCheckBox(self, text="Include Prescription Medication Formula", 
                                            variable=self.check_var, onvalue="on", offvalue="off", command=self.toggle_inputs)
        self.chk_include.pack(anchor="w", padx=45, pady=5)

        ctk.CTkLabel(self, text="Select Catalogs Drug Item:").pack(anchor="w", padx=45, pady=(5, 0))
        self.med_data = self.fetch_medications_list()
        self.combo_med = ctk.CTkComboBox(self, values=list(self.med_data.keys()), state="disabled", width=370)
        self.combo_med.pack(pady=5)

        ctk.CTkLabel(self, text="Specific Dosage Directions:").pack(anchor="w", padx=45, pady=(5, 0))
        self.entry_dose = ctk.CTkEntry(self, width=370, state="disabled", placeholder_text="e.g. 1 pill every 8 hours")
        self.entry_dose.pack(pady=5)

        self.btn_submit = ctk.CTkButton(self, text="Confirm Visit & Complete Transaction", command=self.commit_procedure, fg_color="green", font=("Arial", 14, "bold"), height=35)
        self.btn_submit.pack(pady=25)

    def fetch_medications_list(self):
        rows = self.db_manager.fetch_all("SELECT Medication_ID, Medication_Name FROM MEDICATIONS ORDER BY Medication_Name")
        return {r["medication_name"]: r["medication_id"] for r in rows}

    def toggle_inputs(self):
        state = "readonly" if self.check_var.get() == "on" else "disabled"
        entry_state = "normal" if self.check_var.get() == "on" else "disabled"
        self.combo_med.configure(state=state)
        self.entry_dose.configure(state=entry_state)

    def commit_procedure(self):
        cost = self.entry_cost.get()
        diag = self.txt_diag.get("1.0", "end-1c").strip()
        
        med_id = None
        dosage = None

        if not diag:
            messagebox.showerror("Validation Failed", "Medical diagnosis write-up cannot be submitted blank.")
            return

        if self.check_var.get() == "on":
            selected_med = self.combo_med.get()
            med_id = self.med_data.get(selected_med)
            dosage = self.entry_dose.get().strip()
            
            if not med_id or not dosage:
                messagebox.showerror("Prescription Error", "You checked the prescription box. You must pick a drug item and provide exact dosage instructions.")
                return

        try:
            # Replaced manual string building inside dynamic view with structural database wrapper engine call safely
            success = self.db_manager.call_complete_appointment_procedure(self.appt_id, self.patient_id, cost, diag, med_id, dosage)
            if success:
                messagebox.showinfo("Success", "Procedure execution committed! Visit logged, invoice generated, and prescription generated successfully.")
                self.on_done_callback()
                self.destroy()
            else:
                messagebox.showerror("Database Transaction Aborted", "Procedure returned failure execution status code on database node.")
        except Exception as e:
            messagebox.showerror("Database Transaction Aborted", str(e))