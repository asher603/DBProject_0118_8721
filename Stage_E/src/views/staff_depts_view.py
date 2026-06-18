import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class StaffDeptsView(ctk.CTkFrame):
    """
    A view class providing a complete CRUD interface for the STAFF and DEPARTMENTS tables.
    Fulfills the foreign key requirement by mapping Department Names instead of Department IDs.
    """
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        # Layout tracking configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tabview initialization for clear module grouping
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_view_all = self.tabview.add("Staff Directory")
        self.tab_add_staff = self.tabview.add("Add New Staff")
        self.tab_manage_staff = self.tabview.add("Update / Delete Staff")

        # In-memory dictionary to map Department Names to Department IDs
        self.dept_map = {}
        self.load_department_mapping()

        # Build individual tab view components
        self.setup_view_all_tab()
        self.setup_add_tab()
        self.setup_manage_tab()

    def load_department_mapping(self):
        """Fetch all departments to build a lookup dictionary mapping Names to IDs."""
        records, _ = self.db_manager.get_all_departments()
        self.dept_map = {}
        if records:
            for dept_id, dept_name in records:
                self.dept_map[dept_name] = dept_id

    # -------------------------------------------------------------------------
    # TAB 1: VIEW ALL STAFF (READ WITH JOIN)
    # -------------------------------------------------------------------------
    def setup_view_all_tab(self):
        self.tab_view_all.grid_columnconfigure(0, weight=1)
        self.tab_view_all.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(self.tab_view_all, text="Hospital Staff Directory", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        refresh_btn = ctk.CTkButton(self.tab_view_all, text="Refresh Directory", command=self.load_staff_data)
        refresh_btn.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        # Table configuration matching layout theme
        columns = ("id", "first_name", "last_name", "role", "department")
        self.tree = ttk.Treeview(self.tab_view_all, columns=columns, show="headings")
        
        self.tree.heading("id", text="Employee ID")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("role", text="Role")
        self.tree.heading("department", text="Assigned Department")

        self.tree.column("id", width=100, anchor="center")
        self.tree.column("first_name", width=150, anchor="center")
        self.tree.column("last_name", width=150, anchor="center")
        self.tree.column("role", width=150, anchor="center")
        self.tree.column("department", width=200, anchor="center")

        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.load_staff_data()

    def load_staff_data(self):
        """Fetch join data from database to safely populate the staff list views."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        records, _ = self.db_manager.get_staff_with_departments()
        if records:
            for rec in records:
                self.tree.insert("", tk.END, values=rec)

    # -------------------------------------------------------------------------
    # TAB 2: ADD NEW STAFF (CREATE)
    # -------------------------------------------------------------------------
    def setup_add_tab(self):
        form_frame = ctk.CTkFrame(self.tab_add_staff, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="First Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_fname = ctk.CTkEntry(form_frame, width=200)
        self.ent_add_fname.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Last Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_lname = ctk.CTkEntry(form_frame, width=200)
        self.ent_add_lname.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Role:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_role = ctk.CTkEntry(form_frame, width=200, placeholder_text="Doctor / Nurse / Admin")
        self.ent_add_role.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Department:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        
        # Populate drop-down list items based on mapped dictionary names keys
        dept_options = list(self.dept_map.keys()) if self.dept_map else ["No Departments Found"]
        self.cmb_add_dept = ctk.CTkComboBox(form_frame, values=dept_options, width=200, state="readonly")
        self.cmb_add_dept.grid(row=3, column=1, padx=10, pady=10)

        save_btn = ctk.CTkButton(form_frame, text="Hire Employee", command=self.add_staff_action)
        save_btn.grid(row=4, column=0, columnspan=2, pady=20)

    def add_staff_action(self):
        """Submit internal entity properties to backend infrastructure pipelines."""
        fname = self.ent_add_fname.get().strip()
        lname = self.ent_add_lname.get().strip()
        role = self.ent_add_role.get().strip()
        selected_dept = self.cmb_add_dept.get()

        if not all([fname, lname, role]) or selected_dept == "No Departments Found":
            messagebox.showerror("Validation Error", "All fields are required. Please check selected values.")
            return

        # Resolve Department ID using lookup map securely
        dept_id = self.dept_map.get(selected_dept)

        success = self.db_manager.add_new_staff(fname, lname, role, dept_id)
        if success:
            messagebox.showinfo("Success", f"Employee {fname} {lname} hired successfully.")
            self.ent_add_fname.delete(0, tk.END)
            self.ent_add_lname.delete(0, tk.END)
            self.ent_add_role.delete(0, tk.END)
            self.load_staff_data()
        else:
            messagebox.showerror("Database Error", "Failed to add employee record to storage engines.")

    # -------------------------------------------------------------------------
    # TAB 3: UPDATE / DELETE STAFF
    # -------------------------------------------------------------------------
    def setup_manage_tab(self):
        form_frame = ctk.CTkFrame(self.tab_manage_staff, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="Enter Employee ID to Fetch:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_manage_search_id = ctk.CTkEntry(form_frame, width=200)
        self.ent_manage_search_id.grid(row=0, column=1, padx=10, pady=10)

        fetch_btn = ctk.CTkButton(form_frame, text="Fetch Record", width=100, command=self.fetch_staff_for_update)
        fetch_btn.grid(row=0, column=2, padx=10, pady=10)

        lbl_line = ctk.CTkLabel(form_frame, text="_______________________________________________________", fg_color="transparent")
        lbl_line.grid(row=1, column=0, columnspan=3, pady=10)

        ctk.CTkLabel(form_frame, text="First Name:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_fname = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_fname.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Last Name:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_lname = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_lname.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Role:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_role = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_role.grid(row=4, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Department:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        dept_options = list(self.dept_map.keys()) if self.dept_map else ["No Departments Found"]
        self.cmb_update_dept = ctk.CTkComboBox(form_frame, values=dept_options, width=200, state="disabled")
        self.cmb_update_dept.grid(row=5, column=1, padx=10, pady=10)

        self.btn_commit_update = ctk.CTkButton(form_frame, text="Update Staff Details", state="disabled", fg_color="green", hover_color="#226422", command=self.commit_update_action)
        self.btn_commit_update.grid(row=6, column=0, pady=20, padx=5)

        self.btn_commit_delete = ctk.CTkButton(form_frame, text="Terminate Employee", state="disabled", fg_color="red", hover_color="#8b1e1e", command=self.commit_delete_action)
        self.btn_commit_delete.grid(row=6, column=1, pady=20, padx=5)

    def fetch_staff_for_update(self):
        """Lookup employee metrics by core unique key index fields."""
        search_id = self.ent_manage_search_id.get().strip()
        if not search_id:
            messagebox.showwarning("Input Required", "Please specify an Employee ID.")
            return

        # Refresh department cache lists first to handle dynamic modifications
        self.load_department_mapping()

        records, _ = self.db_manager.get_staff_by_id(search_id)
        if not records:
            messagebox.showerror("Not Found", f"No employee record found for ID '{search_id}'.")
            return

        emp = records[0] # employee_id, first_name, last_name, role, department_id

        # Enable modify components
        for entry in [self.ent_update_fname, self.ent_update_lname, self.ent_update_role]:
            entry.configure(state="normal")
            entry.delete(0, tk.END)

        self.cmb_update_dept.configure(state="readonly")

        # Map details into form fields securely
        self.ent_update_fname.insert(0, str(emp[1]))
        self.ent_update_lname.insert(0, str(emp[2]))
        self.ent_update_role.insert(0, str(emp[3]))

        # Reverse resolve the department name to set dropdown selection visual index state
        current_dept_id = emp[4]
        for name, d_id in self.dept_map.items():
            if d_id == current_dept_id:
                self.cmb_update_dept.set(name)
                break

        self.btn_commit_update.configure(state="normal")
        self.btn_commit_delete.configure(state="normal")

    def commit_update_action(self):
        """Submit updated employee fields via update data flow channels."""
        search_id = self.ent_manage_search_id.get().strip()
        fname = self.ent_update_fname.get().strip()
        lname = self.ent_update_lname.get().strip()
        role = self.ent_update_role.get().strip()
        selected_dept = self.cmb_update_dept.get()

        if not all([fname, lname, role]):
            messagebox.showerror("Error", "Required fields cannot be empty.")
            return

        dept_id = self.dept_map.get(selected_dept)

        success = self.db_manager.update_staff_info(search_id, fname, lname, role, dept_id)
        if success:
            messagebox.showinfo("Success", "Employee record completely modified successfully.")
            self.load_staff_data()
        else:
            messagebox.showerror("Database Error", "Failed to commit staff corrections.")

    def commit_delete_action(self):
        """Drop specific operational index mappings on user confirmation."""
        search_id = self.ent_manage_search_id.get().strip()
        
        confirm = messagebox.askyesno("Confirm Termination", f"Remove employee ID {search_id} from operational registries? This action is irreversible.")
        if not confirm:
            return

        success = self.db_manager.delete_staff(search_id)
        if success:
            messagebox.showinfo("Dropped", "Employee registration successfully dropped from system parameters.")
            
            # Reset active view input states completely
            for entry in [self.ent_update_fname, self.ent_update_lname, self.ent_update_role]:
                entry.delete(0, tk.END)
                entry.configure(state="disabled")
            
            self.cmb_update_dept.configure(state="disabled")
            self.ent_manage_search_id.delete(0, tk.END)
            self.btn_commit_update.configure(state="disabled")
            self.btn_commit_delete.configure(state="disabled")
            self.load_staff_data()
        else:
            messagebox.showerror("Database Constraint Error", "Cannot delete employee. Check for dependent appointments or record connections.")