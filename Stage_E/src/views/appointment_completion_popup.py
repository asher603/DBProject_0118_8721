import customtkinter as ctk
from tkinter import messagebox

class AppointmentCompletionPopup(ctk.CTkToplevel):
    def __init__(self, parent, appt_id, patient_id, patient_name, db_manager, on_done_callback):
        super().__init__(parent)
        self.db_manager = db_manager
        self.appt_id = appt_id
        self.patient_id = patient_id
        self.on_done_callback = on_done_callback

        self.title("Execute Appointment Closing Procedures Workflow")
        self.geometry("460x580")
        self.transient(parent)
        self.grab_set()

        # Responsive high-contrast textual labels aligned with system dark/light theme
        ctk.CTkLabel(self, text=f"Logging Operational Closing for:\n{patient_name}", font=("Arial", 15, "bold")).pack(pady=15)

        ctk.CTkLabel(self, text="Billing Ledger Base Fee Total Amount ($):").pack(anchor="w", padx=45, pady=(5, 0))
        
        # Clean placeholder entry box for custom invoice input
        self.entry_cost = ctk.CTkEntry(self, width=370, placeholder_text="e.g. 150.00")
        self.entry_cost.pack(pady=5)

        ctk.CTkLabel(self, text="Official Medical Diagnosis Summary:").pack(anchor="w", padx=45, pady=(5, 0))
        self.txt_diag = ctk.CTkTextbox(self, width=370, height=90)
        self.txt_diag.pack(pady=5)

        ctk.CTkFrame(self, height=2, width=380, fg_color="gray").pack(pady=15)

        # Checkbox to toggle prescription visibility
        self.check_var = ctk.StringVar(value="off")
        self.chk_include = ctk.CTkCheckBox(self, text="Include Prescription Medication Formula", 
                                            variable=self.check_var, onvalue="on", offvalue="off", command=self.toggle_inputs)
        self.chk_include.pack(anchor="w", padx=45, pady=5)

        # 1. FIX: Create a dedicated container frame for prescription fields (NOT packed initially)
        self.prescription_frame = ctk.CTkFrame(self, fg_color="transparent")

        # 2. FIX: Pack all prescription sub-widgets inside the new container frame instead of 'self'
        ctk.CTkLabel(self.prescription_frame, text="Select Catalogs Drug Item:").pack(anchor="w", padx=45, pady=(5, 0))
        self.med_data = self.fetch_medications_list()
        self.combo_med = ctk.CTkComboBox(self.prescription_frame, values=list(self.med_data.keys()), state="readonly", width=370)
        self.combo_med.pack(pady=5)

        ctk.CTkLabel(self.prescription_frame, text="Specific Dosage Directions:").pack(anchor="w", padx=45, pady=(5, 0))
        self.entry_dose = ctk.CTkEntry(self.prescription_frame, width=370, placeholder_text="e.g. 1 pill every 8 hours")
        self.entry_dose.pack(pady=5)

        # Submit button at the very bottom
        self.btn_submit = ctk.CTkButton(self, text="Confirm Visit & Complete Transaction", command=self.commit_procedure, fg_color="green", font=("Arial", 14, "bold"), height=35)
        self.btn_submit.pack(pady=25)

    def fetch_medications_list(self):
        rows = self.db_manager.fetch_all("SELECT Medication_ID, Medication_Name FROM MEDICATIONS ORDER BY Medication_Name")
        return {r["medication_name"]: r["medication_id"] for r in rows}

    def toggle_inputs(self):
        # 3. FIX: Show/Hide the entire container frame dynamically and repack the submit button to stay at the bottom
        if self.check_var.get() == "on":
            self.prescription_frame.pack(fill="x", before=self.btn_submit)
        else:
            self.prescription_frame.pack_forget()

    def commit_procedure(self):
        cost = self.entry_cost.get().strip()
        diag = self.txt_diag.get("1.0", "end-1c").strip()
        
        med_id = None
        dosage = None

        if not cost:
            messagebox.showerror("Validation Failed", "Billing amount ledger cost cannot be left blank.")
            return

        if not diag:
            messagebox.showerror("Validation Failed", "Medical diagnosis write-up cannot be submitted blank.")
            return

        if self.check_var.get() == "on":
            selected_med = self.combo_med.get()
            med_id = self.med_data.get(selected_med)
            dosage = self.entry_dose.get().strip()
            
            if not med_id or not dosage:
                messagebox.showerror("Prescription Error", "You checked the prescription box. You must pick a drug item and provide exact dosage instructions.")
                return

        try:
            success = self.db_manager.call_complete_appointment_procedure(self.appt_id, self.patient_id, cost, diag, med_id, dosage)
            if success:
                messagebox.showinfo("Success", "Procedure execution committed! Visit logged, invoice generated, and prescription generated successfully.")
                self.on_done_callback()
                self.destroy()
            else:
                messagebox.showerror("Database Transaction Aborted", "Procedure returned failure execution status code on database node.")
        except Exception as e:
            messagebox.showerror("Database Transaction Aborted", str(e))