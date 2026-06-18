import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from datetime import date

class BillingView(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_view_all = self.tabview.add("Invoices Registry")
        self.tab_add_invoice = self.tabview.add("Create New Invoice")
        self.tab_manage_invoice = self.tabview.add("Update / Delete Invoice")

        self.patient_map = {}
        self.load_patient_mapping()
        self.setup_view_all_tab()
        self.setup_add_tab()
        self.setup_manage_tab()

    def load_patient_mapping(self):
        records, _ = self.db_manager.get_all_patients()
        self.patient_map = {f"{r[1]} {r[2]} (ID: {r[0]})": r[0] for r in records} if records else {}

    def setup_view_all_tab(self):
        self.tab_view_all.grid_columnconfigure(0, weight=1)
        self.tab_view_all.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.tab_view_all, fg_color="transparent")
        search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(search_frame, text="Search By:").pack(side="left")
        self.cmb_filter_type = ctk.CTkComboBox(search_frame, values=["Patient Name", "Invoice ID"], width=120, state="readonly", command=lambda e: self.load_invoices_data())
        self.cmb_filter_type.set("Patient Name")
        self.cmb_filter_type.pack(side="left", padx=5)

        self.ent_search = ctk.CTkEntry(search_frame, placeholder_text="Type search value...", width=180)
        self.ent_search.pack(side="left", padx=5)
        self.ent_search.bind("<KeyRelease>", lambda e: self.load_invoices_data())

        table_frame = ctk.CTkFrame(self.tab_view_all, fg_color="transparent")
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("invoice_id", "patient_name", "amount", "billing_date")
        self.tree_invoice = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns: self.tree_invoice.heading(col, text=col.replace("_", " ").title())
        for col in columns: self.tree_invoice.column(col, anchor="center", width=150)
        self.tree_invoice.grid(row=0, column=0, sticky="nsew")

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree_invoice.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_invoice.configure(yscrollcommand=scrollbar.set)
        
        self.load_invoices_data()

    def load_invoices_data(self):
        for row in self.tree_invoice.get_children(): self.tree_invoice.delete(row)
        term, f_type = self.ent_search.get().strip(), self.cmb_filter_type.get()
        records, _ = self.db_manager.get_detailed_invoices(search_term=term if term else None, filter_type=f_type)
        if records:
            for rec in records:
                f_rec = list(rec); f_rec[3] = str(f_rec[3])
                self.tree_invoice.insert("", tk.END, values=f_rec)

    def setup_add_tab(self):
        form_frame = ctk.CTkFrame(self.tab_add_invoice, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(form_frame, text="Generate Financial Billing Invoice", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)

        ctk.CTkLabel(form_frame, text="Select Patient:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.cmb_add_patient = ctk.CTkComboBox(form_frame, values=list(self.patient_map.keys()), width=240, state="readonly")
        self.cmb_add_patient.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Amount ($):").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_amount = ctk.CTkEntry(form_frame, width=240)
        self.ent_add_amount.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Billing Date:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_date = ctk.CTkEntry(form_frame, width=240); self.ent_add_date.insert(0, str(date.today()))
        self.ent_add_date.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkButton(form_frame, text="Issue Invoice", command=self.create_invoice_action).grid(row=4, column=0, columnspan=2, pady=25)

    def create_invoice_action(self):
        p_id = self.patient_map.get(self.cmb_add_patient.get())
        if self.db_manager.add_new_invoice(float(self.ent_add_amount.get()), self.ent_add_date.get(), p_id):
            messagebox.showinfo("Issued", "Success.")
            self.ent_add_amount.delete(0, tk.END); self.load_invoices_data()

    def setup_manage_tab(self):
        form_frame = ctk.CTkFrame(self.tab_manage_invoice, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="Invoice ID:").grid(row=0, column=0, padx=10, pady=10)
        self.ent_manage_search_id = ctk.CTkEntry(form_frame, width=200)
        self.ent_manage_search_id.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(form_frame, text="Fetch", width=100, command=self.fetch_invoice_for_update).grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Patient:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.cmb_update_patient = ctk.CTkComboBox(form_frame, values=list(self.patient_map.keys()), width=200, state="disabled")
        self.cmb_update_patient.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Amount ($):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_amount = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_amount.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Date:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_date = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_date.grid(row=4, column=1, padx=10, pady=10)

        self.btn_commit_update = ctk.CTkButton(form_frame, text="Update", state="disabled", fg_color="green", command=self.commit_update_action)
        self.btn_commit_update.grid(row=5, column=0, pady=20)
        self.btn_commit_delete = ctk.CTkButton(form_frame, text="Void", state="disabled", fg_color="red", command=self.commit_delete_action)
        self.btn_commit_delete.grid(row=5, column=1, pady=20)

    def fetch_invoice_for_update(self):
        records, _ = self.db_manager.get_invoice_by_id(self.ent_manage_search_id.get().strip())
        if records:
            inv = records[0]
            self.cmb_update_patient.configure(state="readonly")
            for e in [self.ent_update_amount, self.ent_update_date]: e.configure(state="normal"); e.delete(0, tk.END)
            self.ent_update_amount.insert(0, str(inv[1])); self.ent_update_date.insert(0, str(inv[2]))
            for name, p_id in self.patient_map.items():
                if p_id == inv[3]: self.cmb_update_patient.set(name); break
            self.btn_commit_update.configure(state="normal"); self.btn_commit_delete.configure(state="normal")

    def commit_update_action(self):
        p_id = self.patient_map.get(self.cmb_update_patient.get())
        if self.db_manager.update_invoice_info(self.ent_manage_search_id.get().strip(), float(self.ent_update_amount.get()), self.ent_update_date.get(), p_id):
            messagebox.showinfo("Success", "Updated."); self.load_invoices_data()

    def commit_delete_action(self):
        if self.db_manager.delete_invoice(self.ent_manage_search_id.get().strip()):
            messagebox.showinfo("Voided", "Dropped."); self.load_invoices_data()