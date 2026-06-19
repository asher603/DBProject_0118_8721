import customtkinter as ctk
from tkinter import ttk, messagebox
from views.detail_popup import EntityDetailPopup

class GenericCrudView(ctk.CTkFrame):
    def __init__(self, parent, db_manager, on_back_click):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_back_click = on_back_click
        
        # Config map with explicit sorting logic and per-column search criteria filters
        self.entity_config = {
            "Patients": {
                "table": "PATIENTS", "pk": "patient_id", 
                "cols": ["patient_id", "first_name", "last_name", "date_of_birth", "phone_number", "address"], 
                "labels": ["Patient ID", "First Name", "Last Name", "DOB", "Phone", "Address"], "write": True,
                "sort_order": "patient_id ASC",
                "search_filters": {"Patient ID": "patient_id", "First Name": "first_name", "Last Name": "last_name"}
            },
            "Staff": {
                "table": "STAFF", "pk": "employee_id", 
                "cols": ["employee_id", "first_name", "last_name", "role", "department_name"], 
                "labels": ["Employee ID", "First Name", "Last Name", "Role", "Department"], "write": True, 
                "select_query": "SELECT s.Employee_ID, s.First_Name, s.Last_Name, s.Role, d.Department_Name FROM STAFF s JOIN DEPARTMENTS d ON s.Department_ID = d.Department_ID", 
                "fk_fields": {"Department": "SELECT Department_ID, Department_Name FROM DEPARTMENTS"},
                "sort_order": "s.Employee_ID ASC",
                "search_filters": {"Employee ID": "employee_id", "First Name": "first_name", "Role": "role"}
            },
            "Departments": {
                "table": "DEPARTMENTS", "pk": "department_id", 
                "cols": ["department_id", "department_name"], 
                "labels": ["Department ID", "Department Name"], "write": True,
                "sort_order": "department_id ASC",
                "search_filters": {"Department ID": "department_id", "Department Name": "department_name"}
            },
            "Rooms": {
                "table": "ROOMS", "pk": "room_id", 
                "cols": ["room_id", "room_number", "room_type", "department_name"], 
                "labels": ["Room ID", "Room Number", "Room Type", "Department Name"], "write": True,
                "select_query": "SELECT r.Room_ID, r.Room_Number, r.Room_Type, d.Department_Name FROM ROOMS r JOIN DEPARTMENTS d ON r.Department_ID = d.Department_ID", 
                "fk_fields": {"Department": "SELECT Department_ID, Department_Name FROM DEPARTMENTS"},
                "sort_order": "r.Room_ID ASC",
                "search_filters": {"Room ID": "room_id", "Room Number": "room_number"}
            },
            "Beds": {
                "table": "BEDS", "pk": "bed_id", 
                "cols": ["bed_id", "bed_number", "room_number"], 
                "labels": ["Bed ID", "Bed Number", "Room Number"], "write": True,
                "select_query": "SELECT b.Bed_ID, b.Bed_Number, r.Room_Number FROM BEDS b JOIN ROOMS r ON b.Room_ID = r.Room_ID", 
                "fk_fields": {"Room": "SELECT Room_ID, Room_Number FROM ROOMS"},
                "sort_order": "b.Bed_ID ASC",
                "search_filters": {"Bed ID": "bed_id", "Bed Number": "bed_number"}
            },
            "Medications": {
                "table": "MEDICATIONS", "pk": "medication_id", 
                "cols": ["medication_id", "medication_name"], 
                "labels": ["Medication ID", "Medication Name"], "write": True,
                "sort_order": "medication_id ASC",
                "search_filters": {"Medication ID": "medication_id", "Medication Name": "medication_name"}
            },
            "Appointments": {
                "table": "APPOINTMENTS", "pk": "appointment_id", 
                "cols": ["appointment_id", "appointment_date", "patient_name", "staff_name", "room_number", "status"], 
                "labels": ["Appt ID", "Date", "Patient", "Doctor/Staff", "Room", "Status"], "write": True,
                "select_query": "SELECT a.Appointment_ID, a.Patient_ID, a.Appointment_Date, (p.First_Name || ' ' || p.Last_Name) as patient_name, (s.First_Name || ' ' || s.Last_Name) as staff_name, r.Room_Number, a.Status FROM APPOINTMENTS a JOIN PATIENTS p ON a.Patient_ID = p.Patient_ID JOIN STAFF s ON a.Employee_ID = s.Employee_ID JOIN ROOMS r ON a.Room_ID = r.Room_ID",
                "fk_fields": {"Patient": "SELECT Patient_ID, (First_Name || ' ' || Last_Name) FROM PATIENTS", "Staff": "SELECT Employee_ID, (First_Name || ' ' || Last_Name) FROM STAFF", "Room": "SELECT Room_ID, Room_Number FROM ROOMS"},
                "sort_order": "a.Appointment_Date DESC",
                "search_filters": {"Appointment ID": "appointment_id", "Patient Name": "patient_name", "Status": "status"}
            },
            "Inpatient Admissions": {
                "table": "INPATIENT_ADMISSIONS", "pk": "admission_id", 
                "cols": ["admission_id", "admission_date", "discharge_date", "patient_name", "bed_number"], 
                "labels": ["Admission ID", "Admit Date", "Discharge Date", "Patient", "Bed Number"], "write": True,
                "select_query": "SELECT i.Admission_ID, i.Admission_Date, i.Discharge_Date, (p.First_Name || ' ' || p.Last_Name) as patient_name, b.Bed_Number FROM INPATIENT_ADMISSIONS i JOIN PATIENTS p ON i.Patient_ID = p.Patient_ID JOIN BEDS b ON i.Bed_ID = b.Bed_ID",
                "fk_fields": {"Patient": "SELECT Patient_ID, (First_Name || ' ' || Last_Name) FROM PATIENTS", "Bed": "SELECT Bed_ID, Bed_Number FROM BEDS"},
                "sort_order": "i.Admission_Date DESC",
                "search_filters": {"Admission ID": "admission_id", "Patient Name": "patient_name"}
            },
            "Visits": {
                "table": "VISITS", "pk": "visit_id", 
                "cols": ["visit_id", "visit_date", "diagnosis", "patient_name", "staff_name"], 
                "labels": ["Visit ID", "Date", "Diagnosis", "Patient", "Attending Staff"], "write": False,
                "select_query": "SELECT v.Visit_ID, v.Visit_Date, v.Diagnosis, (p.First_Name || ' ' || p.Last_Name) as patient_name, (s.First_Name || ' ' || s.Last_Name) as staff_name FROM VISITS v JOIN PATIENTS p ON v.Patient_ID = p.Patient_ID JOIN STAFF s ON v.Employee_ID = s.Employee_ID",
                "sort_order": "v.visit_date DESC",
                "search_filters": {"Visit ID": "visit_id", "Diagnosis": "diagnosis", "Patient Name": "patient_name"}
            },
            "Invoices": {
                "table": "INVOICES", "pk": "invoice_id", 
                "cols": ["invoice_id", "total_amount", "billing_date", "patient_name"], 
                "labels": ["Invoice ID", "Amount ($)", "Billing Date", "Patient"], "write": False,
                "select_query": "SELECT inv.Invoice_ID, inv.Total_Amount, inv.Billing_Date, (p.First_Name || ' ' || p.Last_Name) as patient_name FROM INVOICES inv JOIN PATIENTS p ON inv.Patient_ID = p.Patient_ID",
                "sort_order": "inv.billing_date DESC",
                "search_filters": {"Invoice ID": "invoice_id", "Patient Name": "patient_name"}
            },
            "Prescriptions": {
                "table": "PRESCRIPTIONS", "pk": "prescription_id", 
                "cols": ["prescription_id", "dosage", "visit_id", "medication_name"], 
                "labels": ["Prescription ID", "Dosage Instructions", "Visit ID", "Medication Name"], "write": False,
                "select_query": "SELECT pr.Prescription_ID, pr.Dosage, pr.Visit_ID, m.Medication_Name FROM PRESCRIPTIONS pr JOIN MEDICATIONS m ON pr.Medication_ID = m.Medication_ID",
                "sort_order": "pr.prescription_id ASC",
                "search_filters": {"Prescription ID": "prescription_id", "Medication Name": "medication_name", "Visit ID": "visit_id"}
            }
        }

        # Top Control Header Setup
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=15)

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
        # Rebuilt targeted Filter Sub-bar layout with Column dropdown routing
        self.search_frame = ctk.CTkFrame(self.tab_list, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(self.search_frame, text="Filter By:", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        
        self.filter_col_dropdown = ctk.CTkOptionMenu(self.search_frame, width=150, values=["Patient ID"])
        self.filter_col_dropdown.pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type criteria filter text...", width=250)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_table_records())

        # Treeview Styles and Setup
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white", rowheight=28)
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

        # Sync available targeting filter keys dynamically into dropdown menu options bar
        filter_labels = list(cfg["search_filters"].keys())
        self.filter_col_dropdown.configure(values=filter_labels)
        self.filter_col_dropdown.set(filter_labels[0])
        self.search_entry.delete(0, "end")

        # Rebuild Tree Columns
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = cfg["cols"]
        for col, label in zip(cfg["cols"], cfg["labels"]):
            self.tree.heading(col, text=label, anchor="w")
            self.tree.column(col, width=130, anchor="w")

        # Construct specific ORDER BY extraction query matching date/ID metadata parameters rules
        base_select = cfg.get("select_query", f"SELECT * FROM {cfg['table']}")
        query = f"{base_select} ORDER BY {cfg['sort_order']}"
        
        self.all_fetched_records = self.db_manager.fetch_all(query)
        self.populate_tree(self.all_fetched_records)

        # Reset and Rebuild the Dynamic Create Form Tab
        for w in self.tab_create.winfo_children():
            w.destroy()

        if not cfg["write"]:
            ctk.CTkLabel(self.tab_create, text=f"Direct creation blocked for {current} transactional log data.\nKindly generate these records dynamically utilizing business procedures.", font=("Arial", 15, "italic"), text_color="orange").pack(pady=50)
            return

        self.build_dynamic_insert_form(cfg)

    def populate_tree(self, record_list):
        self.tree.delete(*self.tree.get_children())
        for row in record_list:
            values = [row.get(col.lower(), "") for col in self.tree["columns"]]
            self.tree.insert("", "end", iid=row[self.entity_config[self.entity_dropdown.get()]["pk"]], values=values)

    def filter_table_records(self):
        txt = self.search_entry.get().strip().lower()
        if not txt:
            self.populate_tree(self.all_fetched_records)
            return

        current = self.entity_dropdown.get()
        cfg = self.entity_config[current]
        
        selected_label = self.filter_col_dropdown.get()
        target_col_key = cfg["search_filters"][selected_label]

        filtered = []
        for r in self.all_fetched_records:
            val = str(r.get(target_col_key.lower(), "")).strip().lower()
            
            # CRITICAL RULE: If searching by an ID field, enforce strict absolute matching (==)
            if "id" in target_col_key.lower():
                if val == txt:
                    filtered.append(r)
            else:
                # Textual search uses standard loose inclusion mapping lookup scan
                if txt in val:
                    filtered.append(r)
                    
        self.populate_tree(filtered)

    def on_row_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        pk_val = selected_item[0]
        current_entity = self.entity_dropdown.get()
        
        EntityDetailPopup(self, pk_val, self.entity_config[current_entity], self.db_manager, on_modified_callback=self.load_current_entity_data)

    def build_dynamic_insert_form(self, cfg):
        scroll_form = ctk.CTkScrollableFrame(self.tab_create, width=500, height=450)
        scroll_form.pack(pady=20, fill="both", expand=True)

        self.form_inputs = {}
        self.fk_mappings = {}

        for col, label in zip(cfg["cols"], cfg["labels"]):
            if col == cfg["pk"]:
                continue
            
            ctk.CTkLabel(scroll_form, text=f"{label}:", font=("Arial", 13, "bold")).pack(anchor="w", padx=30, pady=(10, 2))
            
            fk_found = False
            if "fk_fields" in cfg:
                for fk_key, lookup_q in cfg["fk_fields"].items():
                    if col.lower().startswith(fk_key.lower()) or fk_key.lower() in col.lower():
                        fk_found = True
                        rows = self.db_manager.fetch_all(lookup_q)
                        
                        option_dict = {}
                        for r in rows:
                            items = list(r.values())
                            option_dict[str(items[1])] = items[0]
                        
                        self.fk_mappings[col] = option_dict
                        combo = ctk.CTkComboBox(scroll_form, values=list(option_dict.keys()), width=350, state="readonly")
                        combo.pack(anchor="w", padx=30, pady=5)
                        self.form_inputs[col] = combo
                        break

            if not fk_found:
                # 2. FIX: Check if field is a Date or DateTime and split inputs into structured typing slots
                if "date" in col.lower() or "dob" in col.lower():
                    date_frame = ctk.CTkFrame(scroll_form, fg_color="transparent")
                    date_frame.pack(anchor="w", padx=30, pady=5)
                    
                    entry_d = ctk.CTkEntry(date_frame, width=45, placeholder_text="DD")
                    entry_d.pack(side="left", padx=2)
                    ctk.CTkLabel(date_frame, text="/").pack(side="left")
                    
                    entry_m = ctk.CTkEntry(date_frame, width=45, placeholder_text="MM")
                    entry_m.pack(side="left", padx=2)
                    ctk.CTkLabel(date_frame, text="/").pack(side="left")
                    
                    entry_y = ctk.CTkEntry(date_frame, width=65, placeholder_text="YYYY")
                    entry_y.pack(side="left", padx=2)
                    
                    entry_t = None
                    # If it's a full medical log timestamp (not DOB), append Time typed slots
                    if "birth" not in col.lower() and "dob" not in col.lower():
                        ctk.CTkLabel(date_frame, text="  Time (HH:MM):").pack(side="left", padx=(5, 2))
                        entry_t = ctk.CTkEntry(date_frame, width=60, placeholder_text="12:00")
                        entry_t.pack(side="left", padx=2)
                        
                    self.form_inputs[col] = {
                        "is_date": True,
                        "day": entry_d,
                        "month": entry_m,
                        "year": entry_y,
                        "time": entry_t
                    }
                else:
                    entry = ctk.CTkEntry(scroll_form, width=350, placeholder_text=f"Enter {label}")
                    entry.pack(anchor="w", padx=30, pady=5)
                    self.form_inputs[col] = entry

        btn_save = ctk.CTkButton(self.tab_create, text=f"Save New {self.entity_dropdown.get()} Record", 
                                 command=lambda: self.submit_new_record(cfg), fg_color="green", font=("Arial", 14, "bold"))
        btn_save.pack(pady=20)

    def submit_new_record(self, cfg):
        fields = []
        placeholders = []
        values = []

        for col, widget in self.form_inputs.items():
            db_col_name = col
            if col == "department_name": db_col_name = "department_id"
            if col == "room_number": db_col_name = "room_id"
            if col == "bed_number": db_col_name = "bed_id"
            if col == "patient_name": db_col_name = "patient_id"
            if col == "staff_name": db_col_name = "employee_id"
            if col == "medication_name": db_col_name = "medication_id"

            # 2. FIX: Reconstruct and format components back to native SQL structure safely
            if isinstance(widget, dict) and widget.get("is_date"):
                d = widget["day"].get().strip()
                m = widget["month"].get().strip()
                y = widget["year"].get().strip()
                if not d or not m or not y:
                    messagebox.showerror("Validation Error", f"Please fill out all date components (DD/MM/YYYY) for '{col}'.")
                    return
                
                date_part = f"{y}-{m.zfill(2)}-{d.zfill(2)}"
                
                if widget["time"]:
                    t = widget["time"].get().strip()
                    if not t:
                        messagebox.showerror("Validation Error", f"Please enter a time (HH:MM) for '{col}'.")
                        return
                    if ":" not in t:
                        messagebox.showerror("Validation Error", f"Time format for '{col}' must be HH:MM.")
                        return
                    val = f"{date_part} {t}:00"
                else:
                    val = date_part
            else:
                val = widget.get()
                if not val:
                    messagebox.showerror("Validation Error", f"Field '{col}' cannot be left blank.")
                    return
                
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