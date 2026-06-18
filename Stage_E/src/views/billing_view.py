import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from datetime import date

class BillingView(ctk.CTkFrame):
    """
    A view class providing a uniform CRUD interface for managing the INVOICES table.
    Enforces the auto-increment generation policy and replaces numeric Patient IDs with full names.
    """
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        # Layout management tracking configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Tabview to split view, creation, and manipulation fields
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_view_all = self.tabview.add("Invoices Registry")
        self.tab_add_invoice = self.tabview.add("Create New Invoice")
        self.tab_manage_invoice = self.tabview.add("Update / Delete Invoice")

        # In-memory dictionary to map Patient Names to Patient IDs for UI drop-downs
        self.patient_map = {}
        self.load_patient_mapping()

        # Build view component structures
        self.setup_view_all_tab()
        self.setup_add_tab()
        self.setup_manage_tab()

    def load_patient_mapping(self):
        """Fetch all patients to construct a name-to-ID lookup dictionary for dropdown items."""
        records, _ = self.db_manager.get_all_patients()
        self.patient_map = {}
        if records:
            for rec in records:
                # rec: (Patient_ID, First_Name, Last_Name, ...)
                full_name = f"{rec[1]} {rec[2]} (ID: {rec[0]})"
                self.patient_map[full_name] = rec[0]

    # -------------------------------------------------------------------------
    # TAB 1: INVOICES REGISTRY (READ WITH JOIN)
    # -------------------------------------------------------------------------
    def setup_view_all_tab(self):
        self.tab_view_all.grid_columnconfigure(0, weight=1)
        self.tab_view_all.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(self.tab_view_all, text="Hospital Financial Invoices Log", font=ctk.CTkFont(size=16, weight="bold"))
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        refresh_btn = ctk.CTkButton(self.tab_view_all, text="Refresh Financials", width=130, command=self.load_invoices_data)
        refresh_btn.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        # Configured Treeview table layout
        columns = ("invoice_id", "patient_name", "amount", "billing_date")
        self.tree_invoice = ttk.Treeview(self.tab_view_all, columns=columns, show="headings")
        
        self.tree_invoice.heading("invoice_id", text="Invoice ID")
        self.tree_invoice.heading("patient_name", text="Patient Name")
        self.tree_invoice.heading("amount", text="Total Billed Amount ($)")
        self.tree_invoice.heading("billing_date", text="Billing Date")

        self.tree_invoice.column("invoice_id", width=120, anchor="center")
        self.tree_invoice.column("patient_name", width=250, anchor="center")
        self.tree_invoice.column("amount", width=180, anchor="center")
        self.tree_invoice.column("billing_date", width=180, anchor="center")

        self.tree_invoice.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.load_invoices_data()

    def load_invoices_data(self):
        """Fetch join database values to populate the core table treeview structure."""
        for row in self.tree_invoice.get_children():
            self.tree_invoice.delete(row)
        records, _ = self.db_manager.get_detailed_invoices()
        if records:
            for rec in records:
                formatted_rec = list(rec)
                if formatted_rec[3]:
                    formatted_rec[3] = str(formatted_rec[3]) # Parse dates safely
                self.tree_invoice.insert("", tk.END, values=formatted_rec)

    # -------------------------------------------------------------------------
    # TAB 2: CREATE NEW INVOICE (CREATE)
    # -------------------------------------------------------------------------
    def setup_add_tab(self):
        form_frame = ctk.CTkFrame(self.tab_add_invoice, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="Generate Financial Billing Invoice", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=15)

        ctk.CTkLabel(form_frame, text="Select Patient:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        patient_options = list(self.patient_map.keys()) if self.patient_map else ["No Registered Patients Found"]
        self.cmb_add_patient = ctk.CTkComboBox(form_frame, values=patient_options, width=240, state="readonly")
        self.cmb_add_patient.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Total Billed Amount ($):").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_amount = ctk.CTkEntry(form_frame, width=240, placeholder_text="e.g. 250.50")
        self.ent_add_amount.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Billing Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_date = ctk.CTkEntry(form_frame, width=240)
        self.ent_add_date.insert(0, str(date.today())) # Autofill with current operational date
        self.ent_add_date.grid(row=3, column=1, padx=10, pady=10)

        create_btn = ctk.CTkButton(form_frame, text="Authorize & Issue Invoice", command=self.create_invoice_action)
        create_btn.grid(row=4, column=0, columnspan=2, pady=25)

    def create_invoice_action(self):
        """Extract billing metrics and transmit write pipelines to data tables."""
        selected_patient = self.cmb_add_patient.get()
        amount = self.ent_add_amount.get().strip()
        bill_date = self.ent_add_date.get().strip()

        if not amount or selected_patient == "No Registered Patients Found" or not bill_date:
            messagebox.showerror("Validation Error", "All parameter values must be evaluated to issue billing rows.")
            return

        patient_id = self.patient_map.get(selected_patient)

        try:
            float_amount = float(amount)
        except ValueError:
            messagebox.showerror("Format Error", "Billed amount must evaluate as a numeric value.")
            return

        success = self.db_manager.add_new_invoice(float_amount, bill_date, patient_id)
        if success:
            messagebox.showinfo("Success", "Financial billing invoice successfully generated.")
            self.ent_add_amount.delete(0, tk.END)
            self.load_invoices_data()
        else:
            messagebox.showerror("Database Error", "Transaction failed. Verify connection status indicators.")

    # -------------------------------------------------------------------------
    # TAB 3: UPDATE / DELETE INVOICE
    # -------------------------------------------------------------------------
    def setup_manage_tab(self):
        form_frame = ctk.CTkFrame(self.tab_manage_invoice, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Step 1: Input target index and trigger lookup
        ctk.CTkLabel(form_frame, text="Enter Invoice ID to Fetch:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_manage_search_id = ctk.CTkEntry(form_frame, width=200)
        self.ent_manage_search_id.grid(row=0, column=1, padx=10, pady=10)

        fetch_btn = ctk.CTkButton(form_frame, text="Fetch Invoice", width=100, command=self.fetch_invoice_for_update)
        fetch_btn.grid(row=0, column=2, padx=10, pady=10)

        lbl_line = ctk.CTkLabel(form_frame, text="_______________________________________________________", fg_color="transparent")
        lbl_line.grid(row=1, column=0, columnspan=3, pady=10)

        # Step 2: Editable Form Layout (Initially Disabled)
        ctk.CTkLabel(form_frame, text="Assigned Patient:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        patient_options = list(self.patient_map.keys()) if self.patient_map else ["No Registered Patients Found"]
        self.cmb_update_patient = ctk.CTkComboBox(form_frame, values=patient_options, width=200, state="disabled")
        self.cmb_update_patient.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Billed Amount ($):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_amount = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_amount.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Billing Date:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_date = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_date.grid(row=4, column=1, padx=10, pady=10)

        # Execution controls
        self.btn_commit_update = ctk.CTkButton(form_frame, text="Update Invoice", state="disabled", fg_color="green", hover_color="#226422", command=self.commit_update_action)
        self.btn_commit_update.grid(row=5, column=0, pady=20, padx=5)

        self.btn_commit_delete = ctk.CTkButton(form_frame, text="Void / Drop Invoice", state="disabled", fg_color="red", hover_color="#8b1e1e", command=self.commit_delete_action)
        self.btn_commit_delete.grid(row=5, column=1, pady=20, padx=5)

    def fetch_invoice_for_update(self):
        """Lookup financial row constraints based on provided primary index keys."""
        search_id = self.ent_manage_search_id.get().strip()
        if not search_id:
            return

        self.load_patient_mapping() # Refresh mapping values dynamically
        records, _ = self.db_manager.get_invoice_by_id(search_id)
        if not records:
            messagebox.showerror("Not Found", f"No transaction registry matching Invoice ID '{search_id}' discovered.")
            return

        inv = records[0] # Invoice_ID, Total_Amount, Billing_Date, Patient_ID

        # Unlock components
        self.cmb_update_patient.configure(state="readonly")
        for entry in [self.ent_update_amount, self.ent_update_date]:
            entry.configure(state="normal")
            entry.delete(0, tk.END)

        # Map state metrics into visual input frames
        self.ent_update_amount.insert(0, str(inv[1]))
        self.ent_update_date.insert(0, str(inv[2]))

        # Reverse map Patient ID to Combobox visual key string
        current_pid = inv[3]
        for name_str, p_id in self.patient_map.items():
            if p_id == current_pid:
                self.cmb_update_patient.set(name_str)
                break

        self.btn_commit_update.configure(state="normal")
        self.btn_commit_delete.configure(state="normal")

    def commit_update_action(self):
        """Submit refined field properties into update operation channels."""
        search_id = self.ent_manage_search_id.get().strip()
        selected_patient = self.cmb_update_patient.get()
        amount = self.ent_update_amount.get().strip()
        b_date = self.ent_update_date.get().strip()

        if not all([amount, b_date]):
            return

        patient_id = self.patient_map.get(selected_patient)
        try:
            float_amount = float(amount)
        except ValueError:
            return

        success = self.db_manager.update_invoice_info(search_id, float_amount, b_date, patient_id)
        if success:
            messagebox.showinfo("Success", "Financial ledger entries updated successfully.")
            self.load_invoices_data()
        else:
            messagebox.showerror("Database Error", "Failed to commit invoice changes.")

    def commit_delete_action(self):
        """Drop targeted financial record row index permanently."""
        search_id = self.ent_manage_search_id.get().strip()
        if not messagebox.askyesno("Confirm Voiding", f"Void and delete Invoice ID {search_id} from ledger tracking indices permanently?"):
            return

        success = self.db_manager.delete_invoice(search_id)
        if success:
            messagebox.showinfo("Dropped", "Invoice successfully purged from active indices.")
            
            # Wipe view properties
            for entry in [self.ent_update_amount, self.ent_update_date]:
                entry.delete(0, tk.END)
                entry.configure(state="disabled")
            self.cmb_update_patient.configure(state="disabled")
            self.ent_manage_search_id.delete(0, tk.END)
            self.btn_commit_update.configure(state="disabled")
            self.btn_commit_delete.configure(state="disabled")
            self.load_invoices_data()
        else:
            messagebox.showerror("Error", "Database rejected removal query constraints.")