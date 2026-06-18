import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class StaffDeptsView(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_view_all = self.tabview.add("Staff Directory")
        self.tab_add_staff = self.tabview.add("Add New Staff")
        self.tab_manage_staff = self.tabview.add("Update / Delete Staff")

        self.dept_map = {}
        self.load_department_mapping()
        self.setup_view_all_tab()
        self.setup_add_tab()
        self.setup_manage_tab()

    def load_department_mapping(self):
        records, _ = self.db_manager.get_all_departments()
        self.dept_map = {name: d_id for d_id, name in records} if records else {}

    def setup_view_all_tab(self):
        self.tab_view_all.grid_columnconfigure(0, weight=1)
        self.tab_view_all.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.tab_view_all, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(search_frame, text="Search By:").pack(side="left", padx=5)
        self.cmb_filter_type = ctk.CTkComboBox(search_frame, values=["Name", "Role"], width=90, state="readonly", command=lambda e: self.load_staff_data())
        self.cmb_filter_type.set("Name")
        self.cmb_filter_type.pack(side="left", padx=5)

        self.ent_search = ctk.CTkEntry(search_frame, placeholder_text="Type keyword...", width=200)
        self.ent_search.pack(side="left", padx=10)
        self.ent_search.bind("<KeyRelease>", lambda event: self.load_staff_data())

        ctk.CTkButton(search_frame, text="Clear", width=70, command=lambda: [self.ent_search.delete(0, tk.END), self.load_staff_data()]).pack(side="right", padx=5)

        table_frame = ctk.CTkFrame(self.tab_view_all, fg_color="transparent")
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("id", "first_name", "last_name", "role", "department")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="Employee ID"); self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name"); self.tree.heading("role", text="Role"); self.tree.heading("department", text="Department")

        for col in columns: self.tree.column(col, anchor="center", width=140)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.load_staff_data()

    def load_staff_data(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        term, f_type = self.ent_search.get().strip(), self.cmb_filter_type.get()
        records, _ = self.db_manager.get_staff_with_departments(search_term=term if term else None, filter_type=f_type)
        if records:
            for rec in records: self.tree.insert("", tk.END, values=rec)

    def setup_add_tab(self):
        form_frame = ctk.CTkFrame(self.tab_add_staff, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        fields = ["First Name:", "Last Name:", "Role:"]
        self.add_entries = []
        for i, text in enumerate(fields):
            ctk.CTkLabel(form_frame, text=text).grid(row=i, column=0, padx=10, pady=10, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=200)
            entry.grid(row=i, column=1, padx=10, pady=10)
            self.add_entries.append(entry)

        ctk.CTkLabel(form_frame, text="Department:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.cmb_add_dept = ctk.CTkComboBox(form_frame, values=list(self.dept_map.keys()), width=200, state="readonly")
        self.cmb_add_dept.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkButton(form_frame, text="Hire Employee", command=self.add_staff_action).grid(row=4, column=0, columnspan=2, pady=20)

    def add_staff_action(self):
        vals = [e.get().strip() for e in self.add_entries]
        dept = self.cmb_add_dept.get()
        if self.db_manager.add_new_staff(vals[0], vals[1], vals[2], self.dept_map.get(dept)):
            messagebox.showinfo("Success", "Staff hired successfully."); self.load_staff_data()

    def setup_manage_tab(self):
        form_frame = ctk.CTkFrame(self.tab_manage_staff, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="Enter Employee ID:").grid(row=0, column=0, padx=10, pady=10)
        self.ent_manage_search_id = ctk.CTkEntry(form_frame, width=200)
        self.ent_manage_search_id.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(form_frame, text="Fetch", width=100, command=self.fetch_staff_for_update).grid(row=0, column=2, padx=10, pady=10)

        lbl_line = ctk.CTkLabel(form_frame, text="_______________________________________________________")
        lbl_line.grid(row=1, column=0, columnspan=3, pady=10)

        labels = ["First Name:", "Last Name:", "Role:"]
        self.update_entries = []
        for i, text in enumerate(labels):
            ctk.CTkLabel(form_frame, text=text).grid(row=i+2, column=0, padx=10, pady=10, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=200, state="disabled")
            entry.grid(row=i+2, column=1, padx=10, pady=10)
            self.update_entries.append(entry)

        ctk.CTkLabel(form_frame, text="Department:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.cmb_update_dept = ctk.CTkComboBox(form_frame, values=list(self.dept_map.keys()), width=200, state="disabled")
        self.cmb_update_dept.grid(row=5, column=1, padx=10, pady=10)

        self.btn_commit_update = ctk.CTkButton(form_frame, text="Update", state="disabled", fg_color="green", command=self.commit_update_action)
        self.btn_commit_update.grid(row=6, column=0, pady=20)
        self.btn_commit_delete = ctk.CTkButton(form_frame, text="Terminate", state="disabled", fg_color="red", command=self.commit_delete_action)
        self.btn_commit_delete.grid(row=6, column=1, pady=20)

    def fetch_staff_for_update(self):
        records, _ = self.db_manager.get_staff_by_id(self.ent_manage_search_id.get().strip())
        if not records: return
        emp = records[0]
        for entry in self.update_entries: entry.configure(state="normal"); entry.delete(0, tk.END)
        self.cmb_update_dept.configure(state="readonly")
        self.update_entries[0].insert(0, str(emp[1]))
        self.update_entries[1].insert(0, str(emp[2]))
        self.update_entries[2].insert(0, str(emp[3]))
        for name, d_id in self.dept_map.items():
            if d_id == emp[4]: self.cmb_update_dept.set(name); break
        self.btn_commit_update.configure(state="normal"); self.btn_commit_delete.configure(state="normal")

    def commit_update_action(self):
        vals = [e.get().strip() for e in self.update_entries]
        dept = self.cmb_update_dept.get()
        if self.db_manager.update_staff_info(self.ent_manage_search_id.get().strip(), vals[0], vals[1], vals[2], self.dept_map.get(dept)):
            messagebox.showinfo("Success", "Updated."); self.load_staff_data()

    def commit_delete_action(self):
        if self.db_manager.delete_staff(self.ent_manage_search_id.get().strip()):
            messagebox.showinfo("Success", "Fired."); self.load_staff_data()