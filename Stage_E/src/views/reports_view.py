import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class ReportsView(ctk.CTkFrame):
    """
    A view class integrating Stage B analytical queries and Stage D system infrastructure controls.
    Displays dynamic report outputs using a shared spreadsheet layout.
    """
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        # Frame grid initialization
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tabview navigation matching general design criteria
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_queries = self.tabview.add("Management Reports (Stage B)")
        self.tab_procedures = self.tabview.add("Advanced Controls (Stage D)")

        # Setup individual frame blocks
        self.setup_queries_tab()
        self.setup_procedures_tab()

    # -------------------------------------------------------------------------
    # TAB 1: MANAGEMENT REPORTS (STAGE B QUERIES)
    # -------------------------------------------------------------------------
    def setup_queries_tab(self):
        self.tab_queries.grid_columnconfigure(0, weight=1)
        self.tab_queries.grid_rowconfigure(2, weight=1)

        # Top Control Area for Query Execution Buttons
        btn_frame = ctk.CTkFrame(self.tab_queries, fg_color="transparent")
        btn_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        lbl_desc = ctk.CTkLabel(btn_frame, text="Execute Executive Decisions Data Queries:", font=ctk.CTkFont(weight="bold"))
        lbl_desc.pack(side="left", padx=5)

        self.btn_q1 = ctk.CTkButton(btn_frame, text="2024 Active Patients (Q1)", width=180, command=self.run_patients_2024_report)
        self.btn_q1.pack(side="left", padx=10)

        self.btn_q5 = ctk.CTkButton(btn_frame, text="High Financial Billings (Q5)", width=180, command=self.run_high_billing_report)
        self.btn_q5.pack(side="left", padx=10)

        # Separator Line
        lbl_line = ctk.CTkLabel(self.tab_queries, text="__________________________________________________________________________________________________", fg_color="transparent")
        lbl_line.grid(row=1, column=0, pady=5)

        # Shared Treeview Area for Data Display
        self.tree_reports = ttk.Treeview(self.tab_queries, show="headings")
        self.tree_reports.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def clear_tree_columns(self):
        """Wipe existing columns and items to prepare for new structural data mappings."""
        for row in self.tree_reports.get_children():
            self.tree_reports.delete(row)
        self.tree_reports["columns"] = ()

    def run_patients_2024_report(self):
        """Trigger Stage B Query 1 (EXISTS query for 2024 patient encounters)."""
        self.clear_tree_columns()
        
        records, columns = self.db_manager.run_report_patients_2024()
        if records is None or len(records) == 0:
            messagebox.showinfo("Empty Report", "No tracking metrics match criteria for Year 2024.")
            return

        # Dynamically map incoming table column configurations
        self.tree_reports["columns"] = columns
        for col in columns:
            self.tree_reports.heading(col, text=col.replace("_", " ").title())
            self.tree_reports.column(col, anchor="center", width=150)

        for rec in records:
            self.tree_reports.insert("", tk.END, values=rec)

    def run_high_billing_report(self):
        """Trigger Stage B Query 5 (Aggregated financials > 1500 calculation)."""
        self.clear_tree_columns()

        records, columns = self.db_manager.run_report_high_billing()
        if records is None or len(records) == 0:
            messagebox.showinfo("Empty Report", "No ledger accounts exceed financial trigger thresholds ($1500).")
            return

        self.tree_reports["columns"] = columns
        for col in columns:
            self.tree_reports.heading(col, text=col.replace("_", " ").title())
            self.tree_reports.column(col, anchor="center", width=180)

        for rec in records:
            self.tree_reports.insert("", tk.END, values=rec)

    # -------------------------------------------------------------------------
    # TAB 2: ADVANCED SYSTEM INFRASTRUCTURE CONTROLS (STAGE D FUNCTIONS/PROCEDURES)
    # -------------------------------------------------------------------------
    def setup_procedures_tab(self):
        # Center interaction boxes inside frame layout
        wrapper_frame = ctk.CTkFrame(self.tab_procedures, fg_color="transparent")
        wrapper_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Block A: Function 1 Execution Area (Available Beds Calculator)
        func_frame = ctk.CTkLabel(wrapper_frame, text="Execute 'get_available_beds' Function", font=ctk.CTkFont(size=15, weight="bold"))
        func_frame.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        ctk.CTkLabel(wrapper_frame, text="Department ID:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_func_deptid = ctk.CTkEntry(wrapper_frame, width=180, placeholder_text="Numeric ID")
        self.ent_func_deptid.grid(row=1, column=1, padx=10, pady=10)

        run_func_btn = ctk.CTkButton(wrapper_frame, text="Calculate Available Beds", command=self.run_available_beds_function)
        run_func_btn.grid(row=2, column=0, columnspan=2, pady=(5, 20))

        # Separator line block
        lbl_line = ctk.CTkLabel(wrapper_frame, text="_______________________________________________________", fg_color="transparent")
        lbl_line.grid(row=3, column=0, columnspan=2, pady=10)

        # Block B: Procedure 1 Execution Area (Discharge Patient Processor)
        proc_frame = ctk.CTkLabel(wrapper_frame, text="Trigger 'discharge_patient' Procedure", font=ctk.CTkFont(size=15, weight="bold"))
        proc_frame.grid(row=4, column=0, columnspan=2, pady=(10, 5))

        ctk.CTkLabel(wrapper_frame, text="Admission ID:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.ent_proc_admid = ctk.CTkEntry(wrapper_frame, width=180, placeholder_text="Target Admission Record")
        self.ent_proc_admid.grid(row=5, column=1, padx=10, pady=10)

        run_proc_btn = ctk.CTkButton(wrapper_frame, text="Discharge & Liberate Bed", fg_color="green", hover_color="#226422", command=self.run_discharge_procedure)
        run_proc_btn.grid(row=6, column=0, columnspan=2, pady=5)

    def run_available_beds_function(self):
        """Invoke get_available_beds database scalar function using parameter data arrays."""
        dept_id = self.ent_func_deptid.get().strip()
        if not dept_id:
            messagebox.showwarning("Input Missing", "Please declare a valid Department ID constraint.")
            return

        result = self.db_manager.call_get_available_beds_function(dept_id)
        if result is not None:
            messagebox.showinfo("Function Output", f"Operational calculation complete.\n\nAvailable Beds in Dept {dept_id}: {result}")
            self.ent_func_deptid.delete(0, tk.END)
        else:
            messagebox.showerror("Execution Failed", "Failed to resolve inventory. Verify if Department ID is registered.")

    def run_discharge_procedure(self):
        """Invoke discharge_patient stored transactional code blocks directly."""
        adm_id = self.ent_proc_admid.get().strip()
        if not adm_id:
            messagebox.showwarning("Input Missing", "Please declare an active Admission ID instance index.")
            return

        success = self.db_manager.call_discharge_procedure(adm_id)
        if success:
            messagebox.showinfo("Procedure Successful", f"Procedure executed completely:\n\n1. Discharge date assigned to current operational time stamp.\n2. Associated bed flag reverted to vacant indices.")
            self.ent_proc_admid.delete(0, tk.END)
        else:
            messagebox.showerror("Execution Error", "Database rejected execution pipelines. Check if Admission ID is currently open.")