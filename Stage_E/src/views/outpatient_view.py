import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class OutpatientView(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_appointments = self.tabview.add("Appointments & Scheduling")
        self.tab_complete_proc = self.tabview.add("Action: Complete Appointment")
        self.tab_history_func = self.tabview.add("Patient Medical History")

        self.setup_appointments_tab()
        self.setup_complete_proc_tab()
        self.setup_history_func_tab()

    def setup_appointments_tab(self):
        self.tab_appointments.grid_columnconfigure(0, weight=3)
        self.tab_appointments.grid_columnconfigure(1, weight=2)
        self.tab_appointments.grid_rowconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self.tab_appointments, fg_color="transparent")
        left_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(search_frame, text="Filter By:").pack(side="left")
        self.cmb_filter_type = ctk.CTkComboBox(search_frame, values=["Patient Name", "Staff Name"], width=120, state="readonly", command=lambda e: self.load_appointments_data())
        self.cmb_filter_type.set("Patient Name")
        self.cmb_filter_type.pack(side="left", padx=5)

        self.ent_search = ctk.CTkEntry(search_frame, placeholder_text="Type name...", width=150)
        self.ent_search.pack(side="left", padx=5)
        self.ent_search.bind("<KeyRelease>", lambda e: self.load_appointments_data())

        columns = ("app_id", "date", "patient", "staff", "room", "status")
        self.tree_app = ttk.Treeview(left_frame, columns=columns, show="headings")
        for col in columns: self.tree_app.heading(col, text=col.replace("_", " ").title())
        for col in columns: self.tree_app.column(col, anchor="center", width=70 if col in ["app_id", "room", "status"] else 110)
        self.tree_app.grid(row=1, column=0, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(left_frame, command=self.tree_app.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree_app.configure(yscrollcommand=scrollbar.set)

        form_frame = ctk.CTkFrame(self.tab_appointments)
        form_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form_frame, text="Book Appointment", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)
        fields = ["Date & Time (YYYY-MM-DD HH:MM):", "Patient ID:", "Employee ID:", "Room ID:"]
        self.entries = []
        for i, text in enumerate(fields):
            ctk.CTkLabel(form_frame, text=text).grid(row=i+1, column=0, padx=10, pady=8, sticky="e")
            entry = ctk.CTkEntry(form_frame)
            entry.grid(row=i+1, column=1, padx=10, pady=8, sticky="ew")
            self.entries.append(entry)

        ctk.CTkButton(form_frame, text="Book", command=self.book_appointment_action).grid(row=5, column=0, columnspan=2, pady=15)
        self.load_appointments_data()

    def load_appointments_data(self):
        for row in self.tree_app.get_children(): self.tree_app.delete(row)
        term, f_type = self.ent_search.get().strip(), self.cmb_filter_type.get()
        records, _ = self.db_manager.get_detailed_appointments(search_term=term if term else None, filter_type=f_type)
        if records:
            for rec in records:
                f_rec = list(rec); f_rec[1] = str(f_rec[1])
                self.tree_app.insert("", tk.END, values=f_rec)

    def book_appointment_action(self):
        vals = [e.get().strip() for e in self.entries]
        if all(vals) and self.db_manager.add_new_appointment(*vals):
            messagebox.showinfo("Booked", "Success.")
            for e in self.entries: e.delete(0, tk.END)
            self.load_appointments_data()

    def setup_complete_proc_tab(self):
        form_frame = ctk.CTkFrame(self.tab_complete_proc, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(form_frame, text="Trigger 'complete_appointment' Procedure", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)

        labels = ["Appointment ID:", "Patient ID:", "Cost ($):", "Diagnosis:"]
        self.proc_entries = []
        for i, text in enumerate(labels):
            ctk.CTkLabel(form_frame, text=text).grid(row=i+1, column=0, padx=10, pady=8, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=220)
            entry.grid(row=i+1, column=1, padx=10, pady=8)
            self.proc_entries.append(entry)

        ctk.CTkButton(form_frame, text="Execute Checkout Cascade", fg_color="green", command=self.run_complete_appointment_procedure).grid(row=5, column=0, columnspan=2, pady=20)

    def run_complete_appointment_procedure(self):
        vals = [e.get().strip() for e in self.proc_entries]
        if all(vals) and self.db_manager.call_complete_appointment_procedure(*vals):
            messagebox.showinfo("Success", "Procedure executed."); self.load_appointments_data()

    def setup_history_func_tab(self):
        self.tab_history_func.grid_columnconfigure(0, weight=1)
        self.tab_history_func.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.tab_history_func, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=10, pady=15, sticky="w")

        ctk.CTkLabel(search_frame, text="Patient ID:").grid(row=0, column=0, padx=5)
        self.ent_func_pid = ctk.CTkEntry(search_frame, width=150)
        self.ent_func_pid.grid(row=0, column=1, padx=5)
        ctk.CTkButton(search_frame, text="Fetch History", command=self.run_patient_history_function).grid(row=0, column=2, padx=10)

        table_frame = ctk.CTkFrame(self.tab_history_func, fg_color="transparent")
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("visit_id", "visit_date", "diagnosis")
        self.tree_hist = ttk.Treeview(table_frame, columns=columns, show="headings")
        for c in columns: self.tree_hist.heading(c, text=c.replace("_", " ").title())
        self.tree_hist.grid(row=0, column=0, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree_hist.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_hist.configure(yscrollcommand=scrollbar.set)

    def run_patient_history_function(self):
        p_id = self.ent_func_pid.get().strip()
        if not p_id: return
        for row in self.tree_hist.get_children(): self.tree_hist.delete(row)
        records = self.db_manager.call_get_patient_history_function(p_id)
        if records:
            for rec in records:
                f_rec = list(rec); f_rec[1] = str(f_rec[1])
                self.tree_hist.insert("", tk.END, values=f_rec)