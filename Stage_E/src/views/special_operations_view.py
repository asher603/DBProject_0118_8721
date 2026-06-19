import customtkinter as ctk
from tkinter import ttk, messagebox

class SpecialOperationsView(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_back_click): # Added on_back_click parameter
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_back_click = on_back_click # Saved the callback for navigation

        # NEW: Top navigation bar hosting the persistent back button to return to the main hub
        self.top_nav_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_nav_bar.pack(fill="x", padx=20, pady=(15, 0))

        self.btn_back = ctk.CTkButton(self.top_nav_bar, text="← Back to Main Menu", command=self.on_back_click, fg_color="gray", width=160)
        self.btn_back.pack(side="left")

        # Workspace split into structural tabbed action items
        self.tab_panel = ctk.CTkTabview(self)
        self.tab_panel.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_proc = self.tab_panel.add("Process Operations Hub (Stage D Procedures)")
        self.tab_queries = self.tab_panel.add("Complex Diagnostic Analytics (Stage B Queries)")

        self.setup_procedures_interface()
        self.setup_queries_interface()

    # ----------------------------------------------------------------------
    # STAGE D PROCEDURES & FUNCTIONS INTEGRATION
    # ----------------------------------------------------------------------
    def setup_procedures_interface(self):
        # Description header info
        lbl_info = ctk.CTkLabel(self.tab_proc, text="Active Scheduled Appointments Waiting Queue", font=("Arial", 14, "bold"), text_color="cyan")
        lbl_info.pack(anchor="w", padx=15, pady=10)

        # Table showing Scheduled Appointments using analytical dynamic joins
        self.tree_frame = ctk.CTkFrame(self.tab_proc)
        self.tree_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(self.tree_frame, columns=["id", "date", "patient_id", "patient_name", "doctor", "status"], show="headings", height=10)
        self.tree.pack(fill="both", expand=True, side="left")

        # Headings setup
        headings = [("id", "Appt ID"), ("date", "Date"), ("patient_id", "Patient ID"), ("patient_name", "Patient Name"), ("doctor", "Assigned Doctor"), ("status", "Status")]
        for col, txt in headings:
            self.tree.heading(col, text=txt, anchor="w")
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right")

        # Command Button to trigger process execution sequence
        self.btn_complete = ctk.CTkButton(self.tab_proc, text="⚡ Complete Appointment & Issue Prescription/Billing", 
                                           command=self.open_completion_dialog_popup, fg_color="green", font=("Arial", 14, "bold"), height=40)
        self.btn_complete.pack(pady=15)

        self.refresh_scheduled_appointments_queue()

    def refresh_scheduled_appointments_queue(self):
        self.tree.delete(*self.tree.get_children())
        query = """
            SELECT a.Appointment_ID, a.Appointment_Date, a.Patient_ID, 
                   (p.First_Name || ' ' || p.Last_Name) as patient_name, 
                   (s.First_Name || ' ' || s.Last_Name) as doctor_name, a.Status 
            FROM APPOINTMENTS a 
            JOIN PATIENTS p ON a.Patient_ID = p.Patient_ID 
            JOIN STAFF s ON a.Employee_ID = s.Employee_ID 
            WHERE a.Status = 'Scheduled'
            ORDER BY a.Appointment_Date ASC
        """
        rows = self.db_manager.fetch_all(query)
        for r in rows:
            self.tree.insert("", "end", iid=r["appointment_id"], values=[r["appointment_id"], r["appointment_date"], r["patient_id"], r["patient_name"], r["doctor_name"], r["status"]])

    def open_completion_dialog_popup(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Missing", "Please pick an active scheduled appointment from the data directory queue first.")
            return
        
        appt_id = selected[0]
        item_values = self.tree.item(appt_id, "values")
        patient_id = item_values[2]
        patient_name = item_values[3]

        # Launching the precise custom Popup we discussed
        PopupCompletionWindow(self, appt_id, patient_id, patient_name, self.db_manager, on_done_callback=self.refresh_scheduled_appointments_queue)

    # ----------------------------------------------------------------------
    # STAGE B COMPLEX QUERIES INTEGRATION
    # ----------------------------------------------------------------------
    def setup_queries_interface(self):
        ctk.CTkLabel(self.tab_queries, text="Select Analytics Report Query to Run:", font=("Arial", 14, "bold")).pack(anchor="w", padx=20, pady=10)
        
        self.query_dropdown = ctk.CTkOptionMenu(self.tab_queries, values=["Report 1: Top Revenue Billing Patients Directory", "Report 2: Highly Active Patient Load Distributions (Year 2024)"], width=450)
        self.query_dropdown.pack(anchor="w", padx=20, pady=5)

        btn_run = ctk.CTkButton(self.tab_queries, text="Execute Complex Reporting Analytical Scan", command=self.run_stage_b_query, fg_color="blue", font=("Arial", 13, "bold"))
        btn_run.pack(anchor="w", padx=20, pady=10)

        # Output Text View Terminal
        self.txt_output = ctk.CTkTextbox(self.tab_queries, font=("Courier New", 12), width=900, height=350)
        self.txt_output.pack(fill="both", expand=True, padx=20, pady=10)

    def run_stage_b_query(self):
        choice = self.query_dropdown.get()
        self.txt_output.delete("1.0", "end")

        if "Report 1" in choice:
            # Query 1 from Stage B: Invoices ranking high-tier financial summaries
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
            # Query 2 from Stage B: Admissions filter summary matching calendar context limits
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
# SUB-COMPONENT POPUP DIALOG WINDOW (COMPLETE APPOINTMENT SCREEN TRANSACTIONAL POPUP)
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

        # Cost Input fields
        ctk.CTkLabel(self, text="Billing Ledger Base Fee Total Amount ($):").pack(anchor="w", padx=45, pady=(5, 0))
        self.entry_cost = ctk.CTkEntry(self, width=370)
        self.entry_cost.insert(0, "150.00")
        self.entry_cost.pack(pady=5)

        # Diagnosis Entry box
        ctk.CTkLabel(self, text="Official Medical Diagnosis Summary:").pack(anchor="w", padx=45, pady=(5, 0))
        self.txt_diag = ctk.CTkTextbox(self, width=370, height=90)
        self.txt_diag.pack(pady=5)

        # Visual Separator Line
        ctk.CTkFrame(self, height=2, width=380, fg_color="gray").pack(pady=15)

        # The Optional Prescription Checkbox Logic built specifically for your DB constraints
        self.check_var = ctk.StringVar(value="off")
        self.chk_include = ctk.CTkCheckBox(self, text="Include Prescription Medication Formula", 
                                            variable=self.check_var, onvalue="on", offvalue="off", command=self.toggle_inputs)
        self.chk_include.pack(anchor="w", padx=45, pady=5)

        # Medication Dynamic Combobox (Hiding raw numeric IDs!)
        ctk.CTkLabel(self, text="Select Catalogs Drug Item:").pack(anchor="w", padx=45, pady=(5, 0))
        self.med_data = self.fetch_medications_list()
        self.combo_med = ctk.CTkComboBox(self, values=list(self.med_data.keys()), state="disabled", width=370)
        self.combo_med.pack(pady=5)

        # Dosage Entry Field
        ctk.CTkLabel(self, text="Specific Dosage Directions:").pack(anchor="w", padx=45, pady=(5, 0))
        self.entry_dose = ctk.CTkEntry(self, width=370, state="disabled", placeholder_text="e.g. 1 pill every 8 hours")
        self.entry_dose.pack(pady=5)

        # Confirm Submit Button
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

        # Active Validation Check for fields matching your constraints
        if self.check_var.get() == "on":
            selected_med = self.combo_med.get()
            med_id = self.med_data.get(selected_med)
            dosage = self.entry_dose.get().strip()
            
            if not med_id or not dosage:
                messagebox.showerror("Prescription Error", "You checked the prescription box. You must pick a drug item and provide exact dosage instructions.")
                return

        try:
            # Calling your updated Procedure created inside Stage_E!
            sql = "CALL complete_appointment(%s, %s, %s, %s, %s, %s)"
            self.db_manager.execute_non_query(sql, (self.appt_id, self.patient_id, cost, diag, med_id, dosage))
            
            messagebox.showinfo("Success", "Procedure execution committed! Visited record logged, invoice generated, and prescription generated successfully.")
            self.on_done_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Transaction Aborted", str(e))