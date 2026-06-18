import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class PharmacyView(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_prescriptions = self.tabview.add("Prescriptions Log")
        self.tab_issue_prescription = self.tabview.add("Issue New Prescription")
        self.tab_medications_catalog = self.tabview.add("Medications Catalog (CRUD)")

        self.med_map = {}
        self.load_medication_mapping()
        self.setup_prescriptions_tab()
        self.setup_issue_tab()
        self.setup_medications_tab()

    def load_medication_mapping(self):
        records, _ = self.db_manager.get_all_medications()
        self.med_map = {name: m_id for m_id, name in records} if records else {}

    def setup_prescriptions_tab(self):
        self.tab_prescriptions.grid_columnconfigure(0, weight=1)
        self.tab_prescriptions.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.tab_prescriptions, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(search_frame, text="Search By:").pack(side="left")
        self.cmb_filter_type = ctk.CTkComboBox(search_frame, values=["Patient Name", "Medication"], width=120, state="readonly", command=lambda e: self.load_prescriptions_data())
        self.cmb_filter_type.set("Patient Name")
        self.cmb_filter_type.pack(side="left", padx=5)

        self.ent_search = ctk.CTkEntry(search_frame, placeholder_text="Type text...", width=180)
        self.ent_search.pack(side="left", padx=5)
        self.ent_search.bind("<KeyRelease>", lambda e: self.load_prescriptions_data())

        table_frame = ctk.CTkFrame(self.tab_prescriptions, fg_color="transparent")
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("pres_id", "patient_name", "doctor_name", "med_name", "dosage")
        self.tree_pres = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns: self.tree_pres.heading(col, text=col.replace("_", " ").title())
        for col in columns: self.tree_pres.column(col, anchor="center", width=140)
        self.tree_pres.grid(row=0, column=0, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree_pres.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_pres.configure(yscrollcommand=scrollbar.set)
        
        self.load_prescriptions_data()

    def load_prescriptions_data(self):
        for row in self.tree_pres.get_children(): self.tree_pres.delete(row)
        term, f_type = self.ent_search.get().strip(), self.cmb_filter_type.get()
        records, _ = self.db_manager.get_detailed_prescriptions(search_term=term if term else None, filter_type=f_type)
        if records:
            for rec in records: self.tree_pres.insert("", tk.END, values=rec)

    def setup_issue_tab(self):
        form_frame = ctk.CTkFrame(self.tab_issue_prescription, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="Issue Prescription Form", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)
        ctk.CTkLabel(form_frame, text="Visit ID:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_issue_visit_id = ctk.CTkEntry(form_frame, width=220)
        self.ent_issue_visit_id.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Medication:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.cmb_issue_med = ctk.CTkComboBox(form_frame, values=list(self.med_map.keys()), width=220, state="readonly")
        self.cmb_issue_med.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Dosage Instructions:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_issue_dosage = ctk.CTkEntry(form_frame, width=220)
        self.ent_issue_dosage.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkButton(form_frame, text="Commit Entry", command=self.issue_prescription_action).grid(row=4, column=0, columnspan=2, pady=20)

    def issue_prescription_action(self):
        v_id, med, dosage = self.ent_issue_visit_id.get().strip(), self.cmb_issue_med.get(), self.ent_issue_dosage.get().strip()
        if self.db_manager.add_new_prescription(dosage, v_id, self.med_map.get(med)):
            messagebox.showinfo("Success", "Prescription safely added."); self.load_prescriptions_data()

    def setup_medications_tab(self):
        self.tab_medications_catalog.grid_columnconfigure(0, weight=1)
        self.tab_medications_catalog.grid_columnconfigure(1, weight=1)
        self.tab_medications_catalog.grid_rowconfigure(0, weight=1)

        table_frame = ctk.CTkFrame(self.tab_medications_catalog, fg_color="transparent")
        table_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("med_id", "med_name")
        self.tree_med = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree_med.heading("med_id", text="ID"); self.tree_med.heading("med_name", text="Generic Drug Name")
        self.tree_med.grid(row=0, column=0, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree_med.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_med.configure(yscrollcommand=scrollbar.set)

        control_frame = ctk.CTkFrame(self.tab_medications_catalog)
        control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        control_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(control_frame, text="Add New Formulary Drug", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)
        self.ent_catalog_add_name = ctk.CTkEntry(control_frame)
        self.ent_catalog_add_name.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(control_frame, text="Catalog Item", command=self.add_medication_catalog_action).grid(row=2, column=0, columnspan=2, pady=5)

        ctk.CTkLabel(control_frame, text="_______________________________________").grid(row=3, column=0, columnspan=2, pady=10)
        ctk.CTkLabel(control_frame, text="Manage Catalog Entry ID:").grid(row=4, column=0, padx=5, pady=5)
        self.ent_catalog_search_id = ctk.CTkEntry(control_frame, width=80)
        self.ent_catalog_search_id.grid(row=4, column=1, sticky="w", padx=5)
        ctk.CTkButton(control_frame, text="Fetch", width=60, command=self.fetch_medication_catalog_action).grid(row=4, column=1, padx=(95,5), sticky="w")

        self.ent_catalog_update_name = ctk.CTkEntry(control_frame, state="disabled")
        self.ent_catalog_update_name.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.btn_med_update = ctk.CTkButton(control_frame, text="Update", state="disabled", fg_color="green", command=self.update_medication_catalog_action)
        self.btn_med_update.grid(row=6, column=0, pady=5)
        self.btn_med_delete = ctk.CTkButton(control_frame, text="Drop", state="disabled", fg_color="red", command=self.delete_medication_catalog_action)
        self.btn_med_delete.grid(row=6, column=1, pady=5)
        
        self.refresh_medications_catalog()

    def refresh_medications_catalog(self):
        for row in self.tree_med.get_children(): self.tree_med.delete(row)
        records, _ = self.db_manager.get_all_medications()
        if records:
            for rec in records: self.tree_med.insert("", tk.END, values=rec)
        self.load_medication_mapping()
        self.cmb_issue_med.configure(values=list(self.med_map.keys()))

    def add_medication_catalog_action(self):
        name = self.ent_catalog_add_name.get().strip()
        if name and self.db_manager.add_new_medication(name):
            self.ent_catalog_add_name.delete(0, tk.END); self.refresh_medications_catalog()

    def fetch_medication_catalog_action(self):
        m_id = self.ent_catalog_search_id.get().strip()
        records, _ = self.db_manager.get_medication_by_id(m_id)
        if records:
            self.ent_catalog_update_name.configure(state="normal")
            self.ent_catalog_update_name.delete(0, tk.END); self.ent_catalog_update_name.insert(0, str(records[0][1]))
            self.btn_med_update.configure(state="normal"); self.btn_med_delete.configure(state="normal")

    def update_medication_catalog_action(self):
        if self.db_manager.update_medication_info(self.ent_catalog_search_id.get(), self.ent_catalog_update_name.get()):
            self.refresh_medications_catalog()

    def delete_medication_catalog_action(self):
        if self.db_manager.delete_medication(self.ent_catalog_search_id.get()):
            self.refresh_medications_catalog()