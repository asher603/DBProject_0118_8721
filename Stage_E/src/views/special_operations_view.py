import customtkinter as ctk
from tkinter import messagebox

class SpecialOperationsView(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_back_click):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_back_click = on_back_click

        # Top navigation bar
        self.top_nav_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_nav_bar.pack(fill="x", padx=25, pady=(20, 0))

        self.btn_back = ctk.CTkButton(self.top_nav_bar, text="← Back to Main Menu", command=self.on_back_click, fg_color="gray", width=180, height=35, font=("Arial", 13, "bold"))
        self.btn_back.pack(side="left")

        # Workspace split into structural tabbed action items
        self.tab_panel = ctk.CTkTabview(self)
        self.tab_panel.pack(fill="both", expand=True, padx=25, pady=15)

        self.tab_beds_admissions = self.tab_panel.add("Admissions & Beds")
        self.tab_queries = self.tab_panel.add("Analytics Reports")

        self.setup_beds_admissions_interface()
        self.setup_queries_interface()

    # ----------------------------------------------------------------------
    # TAB 1: ADMISSIONS & BEDS PROTOCOLS
    # ----------------------------------------------------------------------
    def setup_beds_admissions_interface(self):
        # Upper Lookup Card (Available Beds Capacity)
        func_card = ctk.CTkFrame(self.tab_beds_admissions, corner_radius=12)
        func_card.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(func_card, text="Department Available Beds", font=("Arial", 16, "bold")).pack(anchor="w", padx=25, pady=(15, 10))
        
        input_row = ctk.CTkFrame(func_card, fg_color="transparent")
        input_row.pack(fill="x", padx=25, pady=(5, 15))
        
        ctk.CTkLabel(input_row, text="Department:", font=("Arial", 14)).pack(side="left", padx=5)
        
        self.dept_mapping = self.fetch_departments_list()
        self.combo_dept = ctk.CTkComboBox(input_row, values=list(self.dept_mapping.keys()), state="readonly", width=350, height=35, font=("Arial", 13))
        self.combo_dept.pack(side="left", padx=15)
        
        btn_check_beds = ctk.CTkButton(input_row, text="Check Capacity", command=self.run_get_available_beds_call, fg_color="blue", width=160, height=35, font=("Arial", 13, "bold"))
        btn_check_beds.pack(side="left", padx=5)

        self.lbl_beds_result = ctk.CTkLabel(func_card, text="Status: Awaiting query...", font=("Arial", 13, "italic"))
        self.lbl_beds_result.pack(anchor="w", padx=25, pady=(0, 15))

        # Lower Lookup Card (Patient Discharge Protocol)
        proc_card = ctk.CTkFrame(self.tab_beds_admissions, corner_radius=12)
        proc_card.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(proc_card, text="Patient Discharge Protocol", font=("Arial", 16, "bold")).pack(anchor="w", padx=25, pady=(15, 10))
        
        proc_row = ctk.CTkFrame(proc_card, fg_color="transparent")
        proc_row.pack(fill="x", padx=25, pady=(5, 15))
        
        ctk.CTkLabel(proc_row, text="Admission ID:", font=("Arial", 14)).pack(side="left", padx=5)
        self.entry_admission_id = ctk.CTkEntry(proc_row, placeholder_text="e.g. 401", width=220, height=35, font=("Arial", 13))
        self.entry_admission_id.pack(side="left", padx=15)
        
        btn_discharge = ctk.CTkButton(proc_row, text="Discharge Patient", command=self.run_discharge_patient_call, fg_color="purple", hover_color="#5D207A", width=180, height=35, font=("Arial", 13, "bold"))
        btn_discharge.pack(side="left", padx=5)
        
        ctk.CTkLabel(proc_card, text="*Note: Logs discharge timestamp and releases the assigned bed.", font=("Arial", 12, "italic")).pack(anchor="w", padx=25, pady=(0, 15))

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
            messagebox.showwarning("Input Missing", "Please select a department first.")
            return
            
        try:
            res = self.db_manager.call_get_available_beds_function(dept_id)
            self.lbl_beds_result.configure(text=f"Status: {res} available beds remaining in {dept_name}.")
        except Exception as e:
            messagebox.showerror("Execution Failure", str(e))

    def run_discharge_patient_call(self):
        adm_id_txt = self.entry_admission_id.get().strip()
        if not adm_id_txt or not adm_id_txt.isdigit():
            messagebox.showerror("Validation Failure", "A valid numeric Admission ID is required.")
            return
            
        try:
            success = self.db_manager.call_discharge_procedure(int(adm_id_txt))
            if success:
                messagebox.showinfo("Success", f"Patient admission ID [{adm_id_txt}] discharged successfully.")
                self.entry_admission_id.delete(0, "end")
            else:
                messagebox.showerror("Error", "Procedure execution failed on database node.")
        except Exception as e:
            messagebox.showerror("Execution Aborted", str(e))

    # ----------------------------------------------------------------------
    # TAB 2: ANALYTICS REPORTS (BUSINESS COMPLEX QUERIES)
    # ----------------------------------------------------------------------
    def setup_queries_interface(self):
        ctk.CTkLabel(self.tab_queries, text="Select Report:", font=("Arial", 15, "bold")).pack(anchor="w", padx=25, pady=(15, 5))
        
        control_row = ctk.CTkFrame(self.tab_queries, fg_color="transparent")
        control_row.pack(fill="x", padx=25, pady=5)

        # FIXED: Added back the structured 'Report X:' anchors combined with clean concise descriptive text
        self.query_dropdown = ctk.CTkOptionMenu(
            control_row, 
            values=["Report 1: Patients with Billings Over 1500", "Report 2: Monthly Average Hospitalization Stays"], 
            width=480, height=35, font=("Arial", 13)
        )
        self.query_dropdown.pack(side="left", padx=(0, 15))

        btn_run = ctk.CTkButton(control_row, text="Execute", command=self.run_stage_b_query, fg_color="blue", width=140, height=35, font=("Arial", 13, "bold"))
        btn_run.pack(side="left")

        # Output Terminal - Expanded height layout
        self.txt_output = ctk.CTkTextbox(self.tab_queries, font=("Courier New", 13), width=950, height=450)
        self.txt_output.pack(fill="both", expand=True, padx=25, pady=20)
        
        self.txt_output.insert("1.0", "execute to view table")

    def run_stage_b_query(self):
        choice = self.query_dropdown.get()
        self.txt_output.delete("1.0", "end")

        try:
            # FIXED: Safely reverted to stable, decoupled prefix scan condition routing
            if "Report 1" in choice:
                rows = self.db_manager.get_top_billing_patients()
                header = f"{'First Name':<15}{'Last Name':<15}{'Phone Number':<18}{'Total Billed ($)':<18}{'Invoices':<10}\n" + "-"*76 + "\n"
            else:
                rows = self.db_manager.get_monthly_average_stays()
                header = f"{'Year':<10}{'Month':<10}{'Total Admissions':<20}{'Avg Stay (Days)':<15}\n" + "-"*55 + "\n"

            self.txt_output.insert("end", header)
            for r in rows:
                items = list(r.values())
                if "Report 1" in choice:
                    line = f"{str(items[0]):<15}{str(items[1]):<15}{str(items[2]):<18}{str(items[3]):<18}{str(items[4]):<10}\n"
                else:
                    line = f"{str(items[0]):<10}{str(items[1]):<10}{str(items[2]):<20}{str(items[3]):<15}\n"
                self.txt_output.insert("end", line)

        except Exception as e:
            self.txt_output.insert("end", f"SQL Operational Failure Encountered:\n{str(e)}")