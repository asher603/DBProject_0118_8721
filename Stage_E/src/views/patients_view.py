import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class PatientsView(ctk.CTkFrame):
    """
    A view class that provides a full CRUD interface for managing the PATIENTS table.
    Adheres strictly to the pure auto-increment policy (IDs are generated automatically by the DB).
    """
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        # Configure frame layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create Tabview for better UX organization
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Define tabs
        self.tab_view_all = self.tabview.add("View All Patients")
        self.tab_add_patient = self.tabview.add("Register New Patient")
        self.tab_manage_patient = self.tabview.add("Update / Delete Patient")

        # Initialize UI components inside each tab
        self.setup_view_all_tab()
        self.setup_add_tab()
        self.setup_manage_tab()

    # -------------------------------------------------------------------------
    # TAB 1: VIEW ALL PATIENTS
    # -------------------------------------------------------------------------
    def setup_view_all_tab(self):
        self.tab_view_all.grid_columnconfigure(0, weight=1)
        self.tab_view_all.grid_rowconfigure(1, weight=1)

        # Header Title
        title = ctk.CTkLabel(self.tab_view_all, text="Registered Patients Directory", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Refresh Button
        refresh_btn = ctk.CTkButton(self.tab_view_all, text="Refresh Directory", command=self.load_patients_data)
        refresh_btn.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        # Setup Styled Tkinter Treeview for Data Presentation
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#2a2d2e", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#1f538d", foreground="white", relief="flat")

        # Define columns based on database structural attributes
        columns = ("id", "first_name", "last_name", "dob", "phone", "address")
        self.tree = ttk.Treeview(self.tab_view_all, columns=columns, show="headings")
        
        self.tree.heading("id", text="Patient ID")
        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("dob", text="Date of Birth")
        self.tree.heading("phone", text="Phone Number")
        self.tree.heading("address", text="Address")

        self.tree.column("id", width=100, anchor="center")
        self.tree.column("first_name", width=120, anchor="center")
        self.tree.column("last_name", width=120, anchor="center")
        self.tree.column("dob", width=110, anchor="center")
        self.tree.column("phone", width=120, anchor="center")
        self.tree.column("address", width=200, anchor="w")

        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Load data on view activation
        self.load_patients_data()

    def load_patients_data(self):
        """Fetch records from DB and populate the Treeview table."""
        # Clear existing data in Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        records, _ = self.db_manager.get_all_patients()
        if records:
            for rec in records:
                # Format Date of Birth safely to string if it exists
                formatted_rec = list(rec)
                if formatted_rec[3]:
                    formatted_rec[3] = str(formatted_rec[3])
                self.tree.insert("", tk.END, values=formatted_rec)

    # -------------------------------------------------------------------------
    # TAB 2: REGISTER NEW PATIENT (CREATE - PURE AUTO-INCREMENT)
    # -------------------------------------------------------------------------
    def setup_add_tab(self):
        # Create form fields inside a centered sub-frame
        form_frame = ctk.CTkFrame(self.tab_add_patient, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="Register New Patient Profile", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # ID field removed to enforce database sequence generation policy
        ctk.CTkLabel(form_frame, text="First Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_fname = ctk.CTkEntry(form_frame, width=200)
        self.ent_add_fname.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Last Name:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_lname = ctk.CTkEntry(form_frame, width=200)
        self.ent_add_lname.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Date of Birth (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_dob = ctk.CTkEntry(form_frame, width=200, placeholder_text="e.g. 1995-08-24")
        self.ent_add_dob.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Phone Number:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_phone = ctk.CTkEntry(form_frame, width=200)
        self.ent_add_phone.grid(row=4, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Address:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.ent_add_address = ctk.CTkEntry(form_frame, width=200)
        self.ent_add_address.grid(row=5, column=1, padx=10, pady=10)

        save_btn = ctk.CTkButton(form_frame, text="Register Patient", command=self.register_patient_action)
        save_btn.grid(row=6, column=0, columnspan=2, pady=20)

    def register_patient_action(self):
        """Extract user inputs and issue a secure INSERT operation via DatabaseManager."""
        fname = self.ent_add_fname.get().strip()
        lname = self.ent_add_lname.get().strip()
        dob = self.ent_add_dob.get().strip()
        phone = self.ent_add_phone.get().strip()
        address = self.ent_add_address.get().strip()

        if not all([fname, lname, dob]):
            messagebox.showerror("Validation Error", "First Name, Last Name, and Date of Birth are mandatory fields.")
            return

        success = self.db_manager.add_new_patient(fname, lname, dob, phone, address)
        if success:
            messagebox.showinfo("Success", f"Patient {fname} {lname} successfully registered.")
            # Clear input fields
            for entry in [self.ent_add_fname, self.ent_add_lname, self.ent_add_dob, self.ent_add_phone, self.ent_add_address]:
                entry.delete(0, tk.END)
            self.load_patients_data()
        else:
            messagebox.showerror("Database Error", "Failed to register patient. Verify database connection or date formatting.")

    # -------------------------------------------------------------------------
    # TAB 3: UPDATE / DELETE PATIENT
    # -------------------------------------------------------------------------
    def setup_manage_tab(self):
        form_frame = ctk.CTkFrame(self.tab_manage_patient, fg_color="transparent")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Step 1: Input key and lookup from database
        ctk.CTkLabel(form_frame, text="Enter Patient ID to Fetch:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_manage_search_id = ctk.CTkEntry(form_frame, width=200, placeholder_text="Numeric Auto-ID")
        self.ent_manage_search_id.grid(row=0, column=1, padx=10, pady=10)

        fetch_btn = ctk.CTkButton(form_frame, text="Fetch Record", width=100, command=self.fetch_patient_for_update)
        fetch_btn.grid(row=0, column=2, padx=10, pady=10)

        # Separator line
        lbl_line = ctk.CTkLabel(form_frame, text="_______________________________________________________", fg_color="transparent")
        lbl_line.grid(row=1, column=0, columnspan=3, pady=10)

        # Step 2: Editable Form Fields (Initially Disabled until a valid record is fetched)
        ctk.CTkLabel(form_frame, text="First Name:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_fname = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_fname.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Last Name:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_lname = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_lname.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Phone Number:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_phone = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_phone.grid(row=4, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="Address:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.ent_update_address = ctk.CTkEntry(form_frame, width=200, state="disabled")
        self.ent_update_address.grid(row=5, column=1, padx=10, pady=10)

        # Modification Control Buttons
        self.btn_commit_update = ctk.CTkButton(form_frame, text="Update Details", state="disabled", fg_color="green", hover_color="#226422", command=self.commit_update_action)
        self.btn_commit_update.grid(row=6, column=0, pady=20, padx=5)

        self.btn_commit_delete = ctk.CTkButton(form_frame, text="Delete Patient Record", state="disabled", fg_color="red", hover_color="#8b1e1e", command=self.commit_delete_action)
        self.btn_commit_delete.grid(row=6, column=1, pady=20, padx=5)

    def fetch_patient_for_update(self):
        """Lookup specific patient data by ID to populate edit fields according to phase criteria."""
        search_id = self.ent_manage_search_id.get().strip()
        if not search_id:
            messagebox.showwarning("Input Required", "Please provide a valid Patient ID first.")
            return

        records, _ = self.db_manager.get_patient_by_id(search_id)
        if not records:
            messagebox.showerror("Not Found", f"No registered patient matching ID '{search_id}' found.")
            return

        patient = records[0] # Retrieve the single tuple match

        # Unlock fields to modify content dynamically
        for entry in [self.ent_update_fname, self.ent_update_lname, self.ent_update_phone, self.ent_update_address]:
            entry.configure(state="normal")
            entry.delete(0, tk.END)

        # Populating existing system metrics into input spaces
        self.ent_update_fname.insert(0, str(patient[1]))
        self.ent_update_lname.insert(0, str(patient[2]))
        self.ent_update_phone.insert(0, str(patient[4]) if patient[4] else "")
        self.ent_update_address.insert(0, str(patient[5]) if patient[5] else "")

        # Enable action execution buttons
        self.btn_commit_update.configure(state="normal")
        self.btn_commit_delete.configure(state="normal")

    def commit_update_action(self):
        """Submit the modified field values to database via write pipeline."""
        search_id = self.ent_manage_search_id.get().strip()
        fname = self.ent_update_fname.get().strip()
        lname = self.ent_update_lname.get().strip()
        phone = self.ent_update_phone.get().strip()
        address = self.ent_update_address.get().strip()

        if not all([fname, lname]):
            messagebox.showerror("Error", "Names fields cannot be empty.")
            return

        success = self.db_manager.update_patient_info(search_id, fname, lname, phone, address)
        if success:
            messagebox.showinfo("Success", "Patient profile details updated successfully.")
            self.load_patients_data()
        else:
            messagebox.showerror("Database Error", "Failed to apply profile changes.")

    def commit_delete_action(self):
        """Perform system removal of patient profile record safely."""
        search_id = self.ent_manage_search_id.get().strip()
        
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you absolutely sure you want to remove patient ID {search_id} from the database? This action is irreversible.")
        if not confirm:
            return

        success = self.db_manager.delete_patient(search_id)
        if success:
            messagebox.showinfo("Deleted", "Patient record completely dropped from indices.")
            
            # Reset view control elements to clear form space entirely
            for entry in [self.ent_update_fname, self.ent_update_lname, self.ent_update_phone, self.ent_update_address]:
                entry.delete(0, tk.END)
                entry.configure(state="disabled")
            
            self.ent_manage_search_id.delete(0, tk.END)
            self.btn_commit_update.configure(state="disabled")
            self.btn_commit_delete.configure(state="disabled")
            self.load_patients_data()
        else:
            messagebox.showerror("Database Constraint Error", "Cannot remove patient. Check for existing related appointments or admissions records.")