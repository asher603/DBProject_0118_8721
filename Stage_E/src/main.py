import customtkinter as ctk
from database import DatabaseManager
from views.patients_view import PatientsView
from views.staff_depts_view import StaffDeptsView
from views.outpatient_view import OutpatientView
from views.pharmacy_view import PharmacyView
from views.billing_view import BillingView
from views.reports_view import ReportsView

# Set the initial appearance mode and color theme
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class HospitalApp(ctk.CTk):
    """
    Main Application Window for the Hospital Management System.
    Handles the UI layout, sidebar navigation, and loading different views.
    """
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Hospital Management System")
        self.geometry("1100x700")
        
        # Initialize database connection
        self.db_manager = DatabaseManager()

        # Configure main grid layout: 1 row, 2 columns
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ---------------------------------------------------------
        # SIDEBAR FRAME (Navigation Menu)
        # ---------------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1)

        # Main Logo / Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Hospital System", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Navigation Buttons
        self.btn_patients = ctk.CTkButton(self.sidebar_frame, text="Patient Management", command=self.show_patients)
        self.btn_patients.grid(row=1, column=0, padx=20, pady=10)

        self.btn_staff = ctk.CTkButton(self.sidebar_frame, text="Staff & Departments", command=self.show_staff)
        self.btn_staff.grid(row=2, column=0, padx=20, pady=10)

        self.btn_appointments = ctk.CTkButton(self.sidebar_frame, text="Appointments & Visits", command=self.show_appointments)
        self.btn_appointments.grid(row=3, column=0, padx=20, pady=10)

        self.btn_pharmacy = ctk.CTkButton(self.sidebar_frame, text="Pharmacy", command=self.show_pharmacy)
        self.btn_pharmacy.grid(row=4, column=0, padx=20, pady=10)

        self.btn_billing = ctk.CTkButton(self.sidebar_frame, text="Billing & Invoices", command=self.show_billing)
        self.btn_billing.grid(row=5, column=0, padx=20, pady=10)

        self.btn_reports = ctk.CTkButton(self.sidebar_frame, text="Reports & Operations", command=self.show_reports)
        self.btn_reports.grid(row=6, column=0, padx=20, pady=10)

        # Appearance Mode Selector (Dark/Light Mode)
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=11, column=0, padx=20, pady=(10, 20))

        # ---------------------------------------------------------
        # MAIN CONTENT FRAME
        # ---------------------------------------------------------
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Load the default screen upon startup
        self.show_patients()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------
    # NAVIGATION METHODS (Loading actual views)
    # ---------------------------------------------------------
    def show_patients(self):
        self.clear_main_frame()
        view = PatientsView(self.main_frame, self.db_manager)
        view.pack(fill="both", expand=True)

    def show_staff(self):
        self.clear_main_frame()
        view = StaffDeptsView(self.main_frame, self.db_manager)
        view.pack(fill="both", expand=True)

    def show_appointments(self):
        self.clear_main_frame()
        view = OutpatientView(self.main_frame, self.db_manager)
        view.pack(fill="both", expand=True)

    def show_pharmacy(self):
        self.clear_main_frame()
        view = PharmacyView(self.main_frame, self.db_manager)
        view.pack(fill="both", expand=True)

    def show_billing(self):
        self.clear_main_frame()
        view = BillingView(self.main_frame, self.db_manager)
        view.pack(fill="both", expand=True)

    def show_reports(self):
        self.clear_main_frame()
        view = ReportsView(self.main_frame, self.db_manager)
        view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()