import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class PatientsView(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.tab_view_all = self.tabview.add("View All Patients")
        self.tab_add_patient = self.tabview.add("Register New Patient")
        self.tab_manage_patient = self.tabview.add("Update / Delete Patient")

        self.setup_view_all_tab()
        self.setup_add_tab()
        self.setup_manage_tab()

    def setup_view_all_tab(self):
        self.tab_view_all.grid_columnconfigure(0, weight=1)
        self.tab_view_all.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.tab_view_all, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(search_frame, text="Search By:").pack(side="left", padx=5)
        self.cmb_filter_type = ctk.CTkComboBox(search_frame, values=["Name", "ID"], width=90, state="readonly", command=lambda e: self.load_patients_data())
        self.cmb_filter_type.set("Name")
        self.cmb_filter_type.pack(side="left", padx=5)

        self.ent_search = ctk.CTkEntry(search_frame, placeholder_text="Type search term...", width=200)
        self.ent_search.pack(side="left", padx=10)
        self.ent_search.bind("<KeyRelease>", lambda event: self.load_patients_data())

        ctk.CTkButton(search_frame, text="Clear", width=70, command=lambda: [self.ent_search.delete(0, tk.END), self.load_patients_data()]).pack(side="right", padx=5)

        table_frame = ctk.CTkFrame(self.tab_view_all, fg_color="transparent")
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("id", "first_name", "last_name", "dob", "phone", "address")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="Patient ID"); self.tree.heading("first_name", text="First Name"); self.tree.heading("last_name", text="Last Name")
        self.tree.heading("dob", text="Date of Birth"); self.tree.heading("phone", text="Phone"); self.tree.heading("address", text="Address")

        for c in columns: self.tree.column(c, anchor="center", width=100 if c != "address" else 220)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.load_patients_data()

    def load_patients_data(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        term, f_type = self.ent_search.get().strip(), self.cmb_filter_type.get()
        records, _ = self.db_manager.get_all_patients(search_term=term if term else None, filter_type=f_type)
        if records:
            for rec in records:
                formatted_rec = list(rec)
                if formatted_rec[3]: formatted_rec[3] = str(formatted_rec[3])
                self.tree.insert("", tk.END, values=formatted_rec)

    def setup_add_tab(self):
        form_frame = ctk.CTkFrame(self.tab_add_patient, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(form_frame, text="Register New Patient Profile", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        fields = ["First Name:", "Last Name:", "Date of Birth (YYYY-MM-DD):", "Phone Number:", "Address:"]
        self.add_entries = []
        for i, text in enumerate(fields):
            ctk.CTkLabel(form_frame, text=text).grid(row=i+1, column=0, padx=10, pady=8, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=200)
            entry.grid(row=i+1, column=1, padx=10, pady=8)
            self.add_entries.append(entry)

        ctk.CTkButton(form_frame, text="Register Patient", command=self.register_patient_action).grid(row=6, column=0, columnspan=2, pady=20)

    def register_patient_action(self):
        vals = [e.get().strip() for e in self.add_entries]
        if not all(vals[:3]):
            messagebox.showerror("Error", "First Name, Last Name, and DOB are required.")
            return
        if self.db_manager.add_new_patient(*vals):
            messagebox.showinfo("Success", "Patient registered successfully.")
            for e in self.add_entries: e.delete(0, tk.END)
            self.load_patients_data()

    def setup_manage_tab(self):
        form_frame = ctk.CTkFrame(self.tab_manage_patient, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="Enter Patient ID to Fetch:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_manage_search_id = ctk.CTkEntry(form_frame, width=200)
        self.ent_manage_search_id.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(form_frame, text="Fetch Record", width=100, command=self.fetch_patient_for_update).grid(row=0, column=2, padx=10, pady=10)

        lbl_line = ctk.CTkLabel(form_frame, text="_______________________________________________________")
        lbl_line.grid(row=1, column=0, columnspan=3, pady=10)

        labels = ["First Name:", "Last Name:", "Phone Number:", "Address:"]
        self.update_entries = []
        for i, text in enumerate(labels):
            ctk.CTkLabel(form_frame, text=text).grid(row=i+2, column=0, padx=10, pady=10, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=200, state="disabled")
            entry.grid(row=i+2, column=1, padx=10, pady=10)
            self.update_entries.append(entry)

        self.btn_commit_update = ctk.CTkButton(form_frame, text="Update Details", state="disabled", fg_color="green", command=self.commit_update_action)
        self.btn_commit_update.grid(row=6, column=0, pady=20, padx=5)
        self.btn_commit_delete = ctk.CTkButton(form_frame, text="Delete Record", state="disabled", fg_color="red", command=self.commit_delete_action)
        self.btn_commit_delete.grid(row=6, column=1, pady=20, padx=5)

    def fetch_patient_for_update(self):
        search_id = self.ent_manage_search_id.get().strip()
        records, _ = self.db_manager.get_patient_by_id(search_id)
        if not records:
            messagebox.showerror("Not Found", "No match found.")
            return
        patient = records[0]
        for entry in self.update_entries: entry.configure(state="normal"); entry.delete(0, tk.END)
        self.update_entries[0].insert(0, str(patient[1]))
        self.update_entries[1].insert(0, str(patient[2]))
        self.update_entries[2].insert(0, str(patient[4]) if patient[4] else "")
        self.update_entries[3].insert(0, str(patient[5]) if patient[5] else "")
        self.btn_commit_update.configure(state="normal"); self.btn_commit_delete.configure(state="normal")

    def commit_update_action(self):
        vals = [e.get().strip() for e in self.update_entries]
        if self.db_manager.update_patient_info(self.ent_manage_search_id.get().strip(), *vals):
            messagebox.showinfo("Success", "Profile updated."); self.load_patients_data()

    def commit_delete_action(self):
        if messagebox.askyesno("Confirm", "Are you sure?"):
            if self.db_manager.delete_patient(self.ent_manage_search_id.get().strip()):
                messagebox.showinfo("Deleted", "Record dropped."); self.load_patients_data()