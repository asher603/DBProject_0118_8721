import customtkinter as ctk
from tkinter import ttk, messagebox
from views.detail_popup import EntityDetailPopup

class GenericCrudView(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_back_click): # Added on_back_click parameter
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_back_click = on_back_click # Saved the callback for navigation
        
        # Define the Metadata Map for all 11 entities to handle display joins automatically
        self.entity_config = {
            "Patients": {"table": "PATIENTS", "pk": "patient_id", "cols": ["patient_id", "first_name", "last_name", "date_of_birth", "phone_number", "address"], "labels": ["Patient ID", "First Name", "Last Name", "DOB", "Phone", "Address"], "write": True},
            "Staff": {"table": "STAFF", "pk": "employee_id", "cols": ["employee_id", "first_name", "last_name", "role", "department_name"], "labels": ["Employee ID", "First Name", "Last Name", "Role", "Department"], "write": True, 
                      "select_query": "SELECT s.Employee_ID, s.First_Name, s.Last_Name, s.Role, d.Department_Name FROM STAFF s JOIN DEPARTMENTS d ON s.Department_ID = d.Department_ID", "fk_fields": {"Department": "SELECT Department_ID, Department_Name FROM DEPARTMENTS"}},
            "Departments": {"table": "DEPARTMENTS", "pk": "department_id", "cols": ["department_id", "department_name"], "labels": ["Department ID", "Department Name"], "write": True},
            "Rooms": {"table": "ROOMS", "pk": "room_id", "cols": ["room_id", "room_number", "room_type", "department_name"], "labels": ["Room ID", "Room Number", "Room Type", "Department Name"], "write": True,
                      "select_query": "SELECT r.Room_ID, r.Room_Number, r.Room_Type, d.Department_Name FROM ROOMS r JOIN DEPARTMENTS d ON r.Department_ID = d.Department_ID", "fk_fields": {"Department": "SELECT Department_ID, Department_Name FROM DEPARTMENTS"}},
            "Beds": {"table": "BEDS", "pk": "bed_id", "cols": ["bed_id", "bed_number", "room_number"], "labels": ["Bed ID", "Bed Number", "Room Number"], "write": True,
                     "select_query": "SELECT b.Bed_ID, b.Bed_Number, r.Room_Number FROM BEDS b JOIN ROOMS r ON b.Room_ID = r.Room_ID", "fk_fields": {"Room": "SELECT Room_ID, Room_Number FROM ROOMS"}},
            "Medications": {"table": "MEDICATIONS", "pk": "medication_id", "cols": ["medication_id", "medication_name"], "labels": ["Medication ID", "Medication Name"], "write": True},
            "Appointments": {"table": "APPOINTMENTS", "pk": "appointment_id", "cols": ["appointment_id", "appointment_date", "patient_name", "staff_name", "room_number", "status"], "labels": ["Appt ID", "Date", "Patient", "Doctor/Staff", "Room", "Status"], "write": True,
                             "select_query": "SELECT a.Appointment_ID, a.Appointment_Date, (p.First_Name || ' ' || p.Last_Name) as patient_name, (s.First_Name || ' ' || s.Last_Name) as staff_name, r.Room_Number, a.Status FROM APPOINTMENTS a JOIN PATIENTS p ON a.Patient_ID = p.Patient_ID JOIN STAFF s ON a.Employee_ID = s.Employee_ID JOIN ROOMS r ON a.Room_ID = r.Room_ID",
                             "fk_fields": {"Patient": "SELECT Patient_ID, (First_Name || ' ' || Last_Name) FROM PATIENTS", "Staff": "SELECT Employee_ID, (First_Name || ' ' || Last_Name) FROM STAFF", "Room": "SELECT Room_ID, Room_Number FROM ROOMS"}},
            "Inpatient Admissions": {"table": "INPATIENT_ADMISSIONS", "pk": "admission_id", "cols": ["admission_id", "admission_date", "discharge_date", "patient_name", "bed_number"], "labels": ["Admission ID", "Admit Date", "Discharge Date", "Patient", "Bed Number"], "write": True,
                                      "select_query": "SELECT i.Admission_ID, i.Admission_Date, i.Discharge_Date, (p.First_Name || ' ' || p.Last_Name) as patient_name, b.Bed_Number FROM INPATIENT_ADMISSIONS i JOIN PATIENTS p ON i.Patient_ID = p.Patient_ID JOIN BEDS b ON i.Bed_ID = b.Bed_ID",
                                      "fk_fields": {"Patient": "SELECT Patient_ID, (First_Name || ' ' || Last_Name) FROM PATIENTS", "Bed": "SELECT Bed_ID, Bed_Number FROM BEDS"}},
            "Visits": {"table": "VISITS", "pk": "visit_id", "cols": ["visit_id", "visit_date", "diagnosis", "patient_name", "staff_name"], "labels": ["Visit ID", "Date", "Diagnosis", "Patient", "Attending Staff"], "write": False,
                       "select_query": "SELECT v.Visit_ID, v.Visit_Date, v.Diagnosis, (p.First_Name || ' ' || p.Last_Name) as patient_name, (s.First_Name || ' ' || s.Last_Name) as staff_name FROM VISITS v JOIN PATIENTS p ON v.Patient_ID = p.Patient_ID JOIN STAFF s ON v.Employee_ID = s.Employee_ID"},
            "Invoices": {"table": "INVOICES", "pk": "invoice_id", "cols": ["invoice_id", "total_amount", "billing_date", "patient_name"], "labels": ["Invoice ID", "Amount ($)", "Billing Date", "Patient"], "write": False,
                         "select_query": "SELECT inv.Invoice_ID, inv.Total_Amount, inv.Billing_Date, (p.First_Name || ' ' || p.Last_Name) as patient_name FROM INVOICES inv JOIN PATIENTS p ON inv.Patient_ID = p.Patient_ID"},
            "Prescriptions": {"table": "PRESCRIPTIONS", "pk": "prescription_id", "cols": ["prescription_id", "dosage", "visit_id", "medication_name"], "labels": ["Prescription ID", "Dosage Instructions", "Visit ID", "Medication Name"], "write": False,
                              "select_query": "SELECT pr.Prescription_ID, pr.Dosage, pr.Visit_ID, m.Medication_Name FROM PRESCRIPTIONS pr JOIN MEDICATIONS m ON pr.Medication_ID = m.Medication_ID"}
        }

        # Top Control Header Setup
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=15)

        # NEW: Return Back Button to drop out to main choice menu
        self.btn_back = ctk.CTkButton(self.top_frame, text="← Back to Main Menu", command=self.on_back_click, fg_color="gray", width=160)
        self.btn_back.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(self.top_frame, text="Select Dataset Entity:", font=("Arial", 14, "bold")).pack(side="left", padx=5)
        
        self.entity_dropdown = ctk.CTkOptionMenu(self.top_frame, values=list(self.entity_config.keys()), command=self.on_entity_changed)
        self.entity_dropdown.pack(side="left", padx=10)
        self.entity_dropdown.set("Patients")

        # Workspace Area setup for Tab View
        self.tab_panel = ctk.CTkTabview(self)
        self.tab_panel.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tab_list = self.tab_panel.add("Records Directory List")
        self.tab_create = self.tab_panel.add("Register New Entry Record")

        self.setup_list_tab()
        self.load_current_entity_data()

    def on_entity_changed(self, choice):
        self.load_current_entity_data()

    def setup_list_tab(self):
        # Search Sub-bar
        self.search_frame = ctk.CTkFrame(self.tab_list, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Live Search Text Filter...", width=300)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_table_records())

        # Treeview Styles and Setup
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2a2a2a", foreground="white", fieldbackground="#2a2a2a", rowheight=28)
        style.map("Treeview", background=[("selected", "#1f538d")])

        self.tree_frame = ctk.CTkFrame(self.tab_list)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(self.tree_frame, selectmode="browse", show="headings")
        self.tree.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right")

        self.tree.bind("<Double-1>", self.on_row_double_click)

    def load_current_entity_data(self):
        current = self.entity_dropdown.get()
        cfg = self.entity_config[current]

        # 1. Reset and Rebuild Tree Columns
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = cfg["cols"]
        for col, label in zip(cfg["cols"], cfg["labels"]):
            self.tree.heading(col, text=label, anchor="w")
            self.tree.column(col, width=130, anchor="w")

        # Fetch Data using Join Queries to hide raw IDs
        query = cfg.get("select_query", f"SELECT * FROM {cfg['table']} ORDER BY {cfg['pk']} DESC")
        self.all_fetched_records = self.db_manager.fetch_all(query)
        self.populate_tree(self.all_fetched_records)

        # 2. Reset and Rebuild the Dynamic Create Form Tab
        for w in self.tab_create.winfo_children():
            w.destroy()

        if not cfg["write"]:
            ctk.CTkLabel(self.tab_create, text=f"Direct creation blocked for {current} transactional log data.\nKindly generate these records dynamically utilizing 'Complete Appointment' procedures.", font=("Arial", 15, "italic"), text_color="orange").pack(pady=50)
            return

        self.build_dynamic_insert_form(cfg)

    def populate_tree(self, record_list):
        self.tree.delete(*self.tree.get_children())
        for row in record_list:
            # Safely extract dictionary values mapped against target column list order
            values = [row.get(col.lower(), "") for col in self.tree["columns"]]
            self.tree.insert("", "end", iid=row[self.entity_config[self.entity_dropdown.get()]["pk"]], values=values)

    def filter_table_records(self):
        txt = self.search_entry.get().lower()
        if not txt:
            self.populate_tree(self.all_fetched_records)
            return
        filtered = [r for r in self.all_fetched_records if any(str(v).lower().find(txt) != -1 for v in r.values())]
        self.populate_tree(filtered)

    def on_row_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        pk_val = selected_item[0] # The iid contains the PK integer value
        current_entity = self.entity_dropdown.get()
        
        # Launch Master-Detail Popup window
        EntityDetailPopup(self, pk_val, self.entity_config[current_entity], self.db_manager, on_modified_callback=self.load_current_entity_data)

    def build_dynamic_insert_form(self, cfg):
        scroll_form = ctk.CTkScrollableFrame(self.tab_create, width=500, height=450)
        scroll_form.pack(pady=20, fill="both", expand=True)

        self.form_inputs = {}
        self.fk_mappings = {} # Holds resolved internal mapping {FieldName: {DisplayName: InternalID}}

        # Loop configuration schema bypassing the internal serial primary key auto-generated values
        for col, label in zip(cfg["cols"], cfg["labels"]):
            if col == cfg["pk"]:
                continue
            
            ctk.CTkLabel(scroll_form, text=f"{label}:", font=("Arial", 13, "bold")).pack(anchor="w", padx=30, pady=(10, 2))
            
            # Contextual ForeignKey field lookup replacement using Dropdowns instead of Numeric input entry boxes
            fk_found = False
            if "fk_fields" in cfg:
                for fk_key, lookup_q in cfg["fk_fields"].items():
                    if col.lower().startswith(fk_key.lower()) or fk_key.lower() in col.lower():
                        fk_found = True
                        rows = self.db_manager.fetch_all(lookup_q)
                        
                        # Populate choice lists mapping display names back to raw surrogate integer keys safely
                        option_dict = {}
                        for r in rows:
                            items = list(r.values())
                            option_dict[str(items[1])] = items[0] # Key=Name, Value=ID
                        
                        self.fk_mappings[col] = option_dict
                        combo = ctk.CTkComboBox(scroll_form, values=list(option_dict.keys()), width=350, state="readonly")
                        combo.pack(anchor="w", padx=30, pady=5)
                        self.form_inputs[col] = combo
                        break

            if not fk_found:
                entry = ctk.CTkEntry(scroll_form, width=350, placeholder_text=f"Enter {label}")
                entry.pack(anchor="w", padx=30, pady=5)
                self.form_inputs[col] = entry

        # Save Action submission triggers
        btn_save = ctk.CTkButton(self.tab_create, text=f"Save New {self.entity_dropdown.get()} Record", 
                                 command=lambda: self.submit_new_record(cfg), fg_color="green", font=("Arial", 14, "bold"))
        btn_save.pack(pady=20)

    def submit_new_record(self, cfg):
        fields = []
        placeholders = []
        values = []

        for col, widget in self.form_inputs.items():
            # Standardize structural column nomenclature mapping to database fields
            db_col_name = col
            if col == "department_name": db_col_name = "department_id"
            if col == "room_number": db_col_name = "room_id"
            if col == "bed_number": db_col_name = "bed_id"
            if col == "patient_name": db_col_name = "patient_id"
            if col == "staff_name": db_col_name = "employee_id"
            if col == "medication_name": db_col_name = "medication_id"

            val = widget.get()
            if not val:
                messagebox.showerror("Validation Error", f"Field '{col}' cannot be left blank.")
                return
            
            # Resolve display textual values back to integer keys internally
            if col in self.fk_mappings:
                val = self.fk_mappings[col].get(val)

            fields.append(db_col_name)
            placeholders.append("%s")
            values.append(val)

        try:
            query = f"INSERT INTO {cfg['table']} ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
            self.db_manager.execute_non_query(query, tuple(values))
            messagebox.showinfo("Success", "Record inserted successfully into Database!")
            self.load_current_entity_data()
            self.tab_panel.set("Records Directory List")
        except Exception as e:
            messagebox.showerror("Database Query Execution Error", str(e))