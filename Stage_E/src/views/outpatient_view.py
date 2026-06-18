import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class OutpatientView(ctk.CTkFrame):
    """
    A view class managing APPOINTMENTS and VISITS tables.
    Integrates Stage D stored procedures and ref cursor functions into the UI workflow.
    """
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tabview navigation setup
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_appointments = self.tabview.add("Appointments & Scheduling")
        self.tab_complete_proc = self.tabview.add("Action: Complete Appointment")
        self.tab_history_func = self.tabview.add("Patient Medical History")

        # Initialize individual component spaces
        self.setup_appointments_tab()
        self.setup_complete_proc_tab()
        self.setup_history_func_tab()

    # -------------------------------------------------------------------------
    # TAB 1: APPOINTMENTS DIRECTORY & NEW SCHEDULING
    # -------------------------------------------------------------------------
    def setup_appointments_tab(self):
        self.tab_appointments.grid_columnconfigure(0, weight=3)
        self.tab_appointments.grid_columnconfigure(1, weight=2)
        self.tab_appointments.grid_rowconfigure(1, weight=1)

        # Left Column: Active Appointments Table View
        ctk.CTkLabel(self.tab_appointments, text="Scheduled Appointments Log", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        refresh_btn = ctk.CTkButton(self.tab_appointments, text="Refresh Logs", width=100, command=self.load_appointments_data)
        refresh_btn.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        columns = ("app_id", "date", "patient", "staff", "room", "status")
        self.tree_app = ttk.Treeview(self.tab_appointments, columns=columns, show="headings")
        self.tree_app.heading("app_id", text="Appt ID")
        self.tree_app.heading("date", text="Date & Time")
        self.tree_app.heading("patient", text="Patient Name")
        self.tree_app.heading("staff", text="Attending Staff")
        self.tree_app.heading("room", text="Room")
        self.tree_app.heading("status", text="Status")

        for col in columns:
            self.tree_app.column(col, anchor="center", width=100 if col in ["app_id", "room", "status"] else 140)

        self.tree_app.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Right Column: Schedule Form Area
        form_frame = ctk.CTkFrame(self.tab_appointments)
        form_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form_frame, text="Schedule New Appointment", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)

        ctk.CTkLabel(form_frame, text="Date & Time:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_date = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD HH:MM")
        self.ent_add_date.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(form_frame, text="Patient ID:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_pid = ctk.CTkEntry(form_frame)
        self.ent_add_pid.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(form_frame, text="Employee ID:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_eid = ctk.CTkEntry(form_frame)
        self.ent_add_eid.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(form_frame, text="Room ID:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_rid = ctk.CTkEntry(form_frame)
        self.ent_add_rid.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        sched_btn = ctk.CTkButton(form_frame, text="Book Appointment", command=self.book_appointment_action)
        sched_btn.grid(row=5, column=0, columnspan=2, pady=20)

        self.load_appointments_data()

    def load_appointments_data(self):
        """Fetch all appointments utilizing structural join queries."""
        for row in self.tree_app.get_children():
            self.tree_app.delete(row)
        records, _ = self.db_manager.get_detailed_appointments()
        if records:
            for rec in records:
                formatted_rec = list(rec)
                formatted_rec[1] = str(formatted_rec[1]) # Safe datetime string parse
                self.tree_app.insert("", tk.END, values=formatted_rec)

    def book_appointment_action(self):
        """Submit new appointment data fields into secure query entry pipes."""
        date_val = self.ent_add_date.get().strip()
        p_id = self.ent_add_pid.get().strip()
        e_id = self.ent_add_eid.get().strip()
        r_id = self.ent_add_rid.get().strip()

        if not all([date_val, p_id, e_id, r_id]):
            messagebox.showerror("Validation Error", "All fields are mandatory to book an appointment.")
            return

        success = self.db_manager.add_new_appointment(date_val, p_id, e_id, r_id)
        if success:
            messagebox.showinfo("Success", "Appointment scheduled successfully.")
            for entry in [self.ent_add_date, self.ent_add_pid, self.ent_add_eid, self.ent_add_rid]:
                entry.delete(0, tk.END)
            self.load_appointments_data()
        else:
            messagebox.showerror("Database Error", "Failed to book appointment. Ensure references exist and date is valid.")

    # -------------------------------------------------------------------------
    # TAB 2: COMPLETE APPOINTMENT (STAGE D STORED PROCEDURE)
    # -------------------------------------------------------------------------
    def setup_complete_proc_tab(self):
        form_frame = ctk.CTkFrame(self.tab_complete_proc, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="Trigger 'complete_appointment' Stored Procedure", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)

        ctk.CTkLabel(form_frame, text="Appointment ID:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_proc_appid = ctk.CTkEntry(form_frame, width=220)
        self.ent_proc_appid.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Patient ID:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_proc_pid = ctk.CTkEntry(form_frame, width=220)
        self.ent_proc_pid.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Appointment Fee / Cost ($):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_proc_cost = ctk.CTkEntry(form_frame, width=220, placeholder_text="e.g. 150.00")
        self.ent_proc_cost.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Medical Diagnosis:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.ent_proc_diag = ctk.CTkEntry(form_frame, width=220, placeholder_text="Enter conclusion criteria")
        self.ent_proc_diag.grid(row=4, column=1, padx=10, pady=10)

        run_proc_btn = ctk.CTkButton(form_frame, text="Execute Checkout & Archive Visit", fg_color="green", hover_color="#226422", command=self.run_complete_appointment_procedure)
        run_proc_btn.grid(row=5, column=0, columnspan=2, pady=25)

    def run_complete_appointment_procedure(self):
        """Invoke complete_appointment database procedure directly using transaction wrappers."""
        app_id = self.ent_proc_appid.get().strip()
        p_id = self.ent_proc_pid.get().strip()
        cost = self.ent_proc_cost.get().strip()
        diag = self.ent_proc_diag.get().strip()

        if not all([app_id, p_id, cost, diag]):
            messagebox.showwarning("Missing Metrics", "Please fill all input fields before executing procedure cascades.")
            return

        success = self.db_manager.call_complete_appointment_procedure(app_id, p_id, cost, diag)
        if success:
            messagebox.showinfo("Procedure Successful", "Procedure completed successfully:\n1. Status flagged 'Completed'\n2. Invoice record generated\n3. Medical Visit log recorded")
            for entry in [self.ent_proc_appid, self.ent_proc_pid, self.ent_proc_cost, self.ent_proc_diag]:
                entry.delete(0, tk.END)
            self.load_appointments_data()
        else:
            messagebox.showerror("Execution Failed", "Database rejected procedure flow constraints. Verify IDs exist.")

    # -------------------------------------------------------------------------
    # TAB 3: PATIENT HISTORY LOGS (STAGE D REF CURSOR FUNCTION)
    # -------------------------------------------------------------------------
    def setup_history_func_tab(self):
        self.tab_history_func.grid_columnconfigure(0, weight=1)
        self.tab_history_func.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.tab_history_func, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=10, pady=15, sticky="w")

        ctk.CTkLabel(search_frame, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_func_pid = ctk.CTkEntry(search_frame, width=150)
        self.ent_func_pid.grid(row=0, column=1, padx=5, pady=5)

        fetch_hist_btn = ctk.CTkButton(search_frame, text="Fetch History (Ref Cursor)", command=self.run_patient_history_function)
        fetch_hist_btn.grid(row=0, column=2, padx=10, pady=5)

        # Result Tree View Table Structure
        columns = ("visit_id", "visit_date", "diagnosis")
        self.tree_hist = ttk.Treeview(self.tab_history_func, columns=columns, show="headings")
        self.tree_hist.heading("visit_id", text="Visit Record ID")
        self.tree_hist.heading("visit_date", text="Encounter Date")
        self.tree_hist.heading("diagnosis", text="Diagnosed Condition")

        self.tree_hist.column("visit_id", width=120, anchor="center")
        self.tree_hist.column("visit_date", width=150, anchor="center")
        self.tree_hist.column("diagnosis", width=400, anchor="w")

        self.tree_hist.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def run_patient_history_function(self):
        """Invoke get_patient_history and handle PostgreSQL ref cursor extraction securely."""
        p_id = self.ent_func_pid.get().strip()
        if not p_id:
            messagebox.showwarning("Input Missing", "Please specify a Patient ID index lookup parameter.")
            return

        for row in self.tree_hist.get_children():
            self.tree_hist.delete(row)

        records = self.db_manager.call_get_patient_history_function(p_id)
        if records is not None:
            if len(records) == 0:
                messagebox.showinfo("No History", "Patient found, but no historical encounter logs exist yet.")
                return
            for rec in records:
                formatted_rec = list(rec)
                formatted_rec[1] = str(formatted_rec[1]) # Safe parsing
                self.tree_hist.insert("", tk.END, values=formatted_rec)
        else:
            messagebox.showerror("Error", f"Failed to open history stream cursor. Patient ID {p_id} may not exist.")