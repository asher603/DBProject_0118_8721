import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class PharmacyView(ctk.CTkFrame):
    """
    A view class providing a uniform CRUD interface for managing the MEDICATIONS and PRESCRIPTIONS tables.
    Adheres strictly to the pure auto-increment ID generation policy and joins names instead of showing raw foreign keys.
    """
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        # Frame layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tabview for dividing Prescriptions management and the Medication catalog
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_prescriptions = self.tabview.add("Prescriptions Log")
        self.tab_issue_prescription = self.tabview.add("Issue New Prescription")
        self.tab_medications_catalog = self.tabview.add("Medications Catalog (CRUD)")

        # In-memory dictionary to map Medication Names to Medication IDs for dropdowns
        self.med_map = {}
        self.load_medication_mapping()

        # Build UI components
        self.setup_prescriptions_tab()
        self.setup_issue_tab()
        self.setup_medications_tab()

    def load_medication_mapping(self):
        """Fetch all catalog medications to build a map from Name to ID for drop-down boxes."""
        records, _ = self.db_manager.get_all_medications()
        self.med_map = {}
        if records:
            for med_id, med_name in records:
                self.med_map[med_name] = med_id

    # -------------------------------------------------------------------------
    # TAB 1: PRESCRIPTIONS LOG (READ WITH MULTIPLE JOINS)
    # -------------------------------------------------------------------------
    def setup_prescriptions_tab(self):
        self.tab_prescriptions.grid_columnconfigure(0, weight=1)
        self.tab_prescriptions.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(self.tab_prescriptions, text="Active Patient Prescriptions", font=ctk.CTkFont(size=16, weight="bold"))
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        refresh_btn = ctk.CTkButton(self.tab_prescriptions, text="Refresh Registry", width=120, command=self.load_prescriptions_data)
        refresh_btn.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        # Treeview configured to display descriptive values instead of primary/foreign keys
        columns = ("pres_id", "patient_name", "doctor_name", "med_name", "dosage")
        self.tree_pres = ttk.Treeview(self.tab_prescriptions, columns=columns, show="headings")
        
        self.tree_pres.heading("pres_id", text="Prescription ID")
        self.tree_pres.heading("patient_name", text="Patient Name")
        self.tree_pres.heading("doctor_name", text="Prescribing Doctor")
        self.tree_pres.heading("med_name", text="Medication Name")
        self.tree_pres.heading("dosage", text="Dosage & Instructions")

        self.tree_pres.column("pres_id", width=110, anchor="center")
        self.tree_pres.column("patient_name", width=160, anchor="center")
        self.tree_pres.column("doctor_name", width=160, anchor="center")
        self.tree_pres.column("med_name", width=160, anchor="center")
        self.tree_pres.column("dosage", width=300, anchor="w")

        self.tree_pres.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.load_prescriptions_data()

    def load_prescriptions_data(self):
        """Populate the prescriptions spreadsheet view utilizing clean contextual join queries."""
        for row in self.tree_pres.get_children():
            self.tree_pres.delete(row)
        records, _ = self.db_manager.get_detailed_prescriptions()
        if records:
            for rec in records:
                self.tree_pres.insert("", tk.END, values=rec)

    # -------------------------------------------------------------------------
    # TAB 2: ISSUE NEW PRESCRIPTION (CREATE)
    # -------------------------------------------------------------------------
    def setup_issue_tab(self):
        form_frame = ctk.CTkFrame(self.tab_issue_prescription, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="Issue New Medical Prescription", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)

        ctk.CTkLabel(form_frame, text="Associated Visit ID:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_issue_visit_id = ctk.CTkEntry(form_frame, width=220, placeholder_text="Enter target medical encounter ID")
        self.ent_issue_visit_id.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Select Medication:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        med_options = list(self.med_map.keys()) if self.med_map else ["No Medications Cataloged"]
        self.cmb_issue_med = ctk.CTkComboBox(form_frame, values=med_options, width=220, state="readonly")
        self.cmb_issue_med.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Dosage & Instructions:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_issue_dosage = ctk.CTkEntry(form_frame, width=220, placeholder_text="e.g. 500mg, twice a day")
        self.ent_issue_dosage.grid(row=3, column=1, padx=10, pady=10)

        issue_btn = ctk.CTkButton(form_frame, text="Commit & Print Prescription", command=self.issue_prescription_action)
        issue_btn.grid(row=4, column=0, columnspan=2, pady=25)

    def issue_prescription_action(self):
        """Process input metrics and append a new prescription record utilizing backend pipelines."""
        visit_id = self.ent_issue_visit_id.get().strip()
        selected_med = self.cmb_issue_med.get()
        dosage = self.ent_issue_dosage.get().strip()

        if not all([visit_id, dosage]) or selected_med == "No Medications Cataloged":
            messagebox.showerror("Validation Error", "All fields must be evaluated before appending database indexes.")
            return

        med_id = self.med_map.get(selected_med)

        success = self.db_manager.add_new_prescription(dosage, visit_id, med_id)
        if success:
            messagebox.showinfo("Success", "Prescription safely added to the patient profile.")
            self.ent_issue_visit_id.delete(0, tk.END)
            self.ent_issue_dosage.delete(0, tk.END)
            self.load_prescriptions_data()
        else:
            messagebox.showerror("Database Error", "Failed to compile prescription entry. Verify if Visit ID exists.")

    # -------------------------------------------------------------------------
    # TAB 3: MEDICATIONS CATALOG (FULL CRUD FOR MEDICATIONS TABLE)
    # -------------------------------------------------------------------------
    def setup_medications_tab(self):
        self.tab_medications_catalog.grid_columnconfigure(0, weight=1)
        self.tab_medications_catalog.grid_columnconfigure(1, weight=1)
        self.tab_medications_catalog.grid_rowconfigure(1, weight=1)

        # Left Column: Catalog Table View
        ctk.CTkLabel(self.tab_medications_catalog, text="Drug Formulary Catalog", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        columns = ("med_id", "med_name")
        self.tree_med = ttk.Treeview(self.tab_medications_catalog, columns=columns, show="headings")
        self.tree_med.heading("med_id", text="Medication ID")
        self.tree_med.heading("med_name", text="Drug Generic Name")
        self.tree_med.column("med_id", width=120, anchor="center")
        self.tree_med.column("med_name", width=250, anchor="w")
        self.tree_med.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Right Column: Multi-action Control Area (Insert / Update / Delete)
        control_frame = ctk.CTkFrame(self.tab_medications_catalog)
        control_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        control_frame.grid_columnconfigure(1, weight=1)

        # Part A: Insert Section
        ctk.CTkLabel(control_frame, text="Add New Drug to Formulary", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(10,5))
        self.ent_catalog_add_name = ctk.CTkEntry(control_frame, placeholder_text="Enter medication brand/generic name")
        self.ent_catalog_add_name.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        add_med_btn = ctk.CTkButton(control_frame, text="Add Medication", command=self.add_medication_catalog_action)
        add_med_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Part B: Update / Delete Section (Fetch requirement fulfilled)
        ctk.CTkLabel(control_frame, text="_______________________________________").grid(row=3, column=0, columnspan=2, pady=10)
        ctk.CTkLabel(control_frame, text="Modify / Drop Catalog Item", font=ctk.CTkFont(weight="bold")).grid(row=4, column=0, columnspan=2, pady=5)

        ctk.CTkLabel(control_frame, text="Medication ID:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.ent_catalog_search_id = ctk.CTkEntry(control_frame, width=100)
        self.ent_catalog_search_id.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        fetch_med_btn = ctk.CTkButton(control_frame, text="Fetch", width=70, command=self.fetch_medication_catalog_action)
        fetch_med_btn.grid(row=5, column=1, padx=(110, 5), pady=5, sticky="w")

        ctk.CTkLabel(control_frame, text="Drug Name:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.ent_catalog_update_name = ctk.CTkEntry(control_frame, state="disabled")
        self.ent_catalog_update_name.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        self.btn_med_update = ctk.CTkButton(control_frame, text="Update Name", state="disabled", fg_color="green", hover_color="#226422", command=self.update_medication_catalog_action)
        self.btn_med_update.grid(row=7, column=0, pady=10, padx=5)

        self.btn_med_delete = ctk.CTkButton(control_frame, text="Remove Item", state="disabled", fg_color="red", hover_color="#8b1e1e", command=self.delete_medication_catalog_action)
        self.btn_med_delete.grid(row=7, column=1, pady=10, padx=5)

        self.refresh_medications_catalog()

    def refresh_medications_catalog(self):
        """Reload the list of database medication catalog items."""
        for row in self.tree_med.get_children():
            self.tree_med.delete(row)
        records, _ = self.db_manager.get_all_medications()
        if records:
            for rec in records:
                self.tree_med.insert("", tk.END, values=rec)
        self.load_medication_mapping()
        
        # Update dropdown options on the issuance tab dynamically
        med_options = list(self.med_map.keys()) if self.med_map else ["No Medications Cataloged"]
        self.cmb_issue_med.configure(values=med_options)

    def add_medication_catalog_action(self):
        name = self.ent_catalog_add_name.get().strip()
        if not name:
            return
        if self.db_manager.add_new_medication(name):
            messagebox.showinfo("Success", f"'{name}' added to hospital inventory formulary registries.")
            self.ent_catalog_add_name.delete(0, tk.END)
            self.refresh_medications_catalog()
        else:
            messagebox.showerror("Database Error", "Failed to catalog drug properties.")

    def fetch_medication_catalog_action(self):
        m_id = self.ent_catalog_search_id.get().strip()
        if not m_id:
            return
        records, _ = self.db_manager.get_medication_by_id(m_id)
        if not records:
            messagebox.showerror("Not Found", "No medication item registered under that ID.")
            return
        
        self.ent_catalog_update_name.configure(state="normal")
        self.ent_catalog_update_name.delete(0, tk.END)
        self.ent_catalog_update_name.insert(0, str(records[0][1]))
        
        self.btn_med_update.configure(state="normal")
        self.btn_med_delete.configure(state="normal")

    def update_medication_catalog_action(self):
        m_id = self.ent_catalog_search_id.get().strip()
        new_name = self.ent_catalog_update_name.get().strip()
        if not new_name:
            return
        if self.db_manager.update_medication_info(m_id, new_name):
            messagebox.showinfo("Updated", "Drug reference name successfully adjusted.")
            self.refresh_medications_catalog()
        else:
            messagebox.showerror("Database Error", "Failed to apply description changes.")

    def delete_medication_catalog_action(self):
        m_id = self.ent_catalog_search_id.get().strip()
        if not messagebox.askyesno("Confirm Removal", "Drop this medication from system lists entirely?"):
            return
        if self.db_manager.delete_medication(m_id):
            messagebox.showinfo("Removed", "Formulary item successfully dropped.")
            self.ent_catalog_update_name.delete(0, tk.END)
            self.ent_catalog_update_name.configure(state="disabled")
            self.ent_catalog_search_id.delete(0, tk.END)
            self.btn_med_update.configure(state="disabled")
            self.btn_med_delete.configure(state="disabled")
            self.refresh_medications_catalog()
        else:
            messagebox.showerror("Constraint Error", "Cannot remove drug. It is tied to active patient prescriptions.")