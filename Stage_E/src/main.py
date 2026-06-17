import customtkinter as ctk
# Later we will import our views here, for example:
# from views.patients_view import PatientsView
from database import DatabaseManager

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
        
        # Initialize database connection (passed to views later)
        self.db_manager = DatabaseManager()

        # Configure main grid layout: 1 row, 2 columns (sidebar and main content area)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ---------------------------------------------------------
        # SIDEBAR FRAME (Navigation Menu)
        # ---------------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(9, weight=1) # Push theme selector to the bottom

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
        # MAIN CONTENT FRAME (Where the screens will appear)
        # ---------------------------------------------------------
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Load the default screen upon startup
        self.show_patients()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Changes the UI theme between Dark, Light, and System default."""
        ctk.set_appearance_mode(new_appearance_mode)

    def clear_main_frame(self):
        """Destroys all widgets currently loaded in the main frame to make room for a new view."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------
    # NAVIGATION METHODS
    # ---------------------------------------------------------

    def show_patients(self):
        self.clear_main_frame()
        # Placeholder for Patients View
        lbl = ctk.CTkLabel(self.main_frame, text="Patient Management View\n(Coming Soon)", font=ctk.CTkFont(size=24))
        lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        # Future implementation:
        # view = PatientsView(self.main_frame, self.db_manager)
        # view.pack(fill="both", expand=True)

    def show_staff(self):
        self.clear_main_frame()
        lbl = ctk.CTkLabel(self.main_frame, text="Staff & Departments View\n(Coming Soon)", font=ctk.CTkFont(size=24))
        lbl.place(relx=0.5, rely=0.5, anchor="center")

    def show_appointments(self):
        self.clear_main_frame()
        lbl = ctk.CTkLabel(self.main_frame, text="Appointments & Visits View\n(Coming Soon)", font=ctk.CTkFont(size=24))
        lbl.place(relx=0.5, rely=0.5, anchor="center")

    def show_pharmacy(self):
        self.clear_main_frame()
        lbl = ctk.CTkLabel(self.main_frame, text="Pharmacy View\n(Coming Soon)", font=ctk.CTkFont(size=24))
        lbl.place(relx=0.5, rely=0.5, anchor="center")

    def show_billing(self):
        self.clear_main_frame()
        lbl = ctk.CTkLabel(self.main_frame, text="Billing & Invoices View\n(Coming Soon)", font=ctk.CTkFont(size=24))
        lbl.place(relx=0.5, rely=0.5, anchor="center")

    def show_reports(self):
        self.clear_main_frame()
        lbl = ctk.CTkLabel(self.main_frame, text="Reports & Advanced Operations\n(Queries & Procedures)", font=ctk.CTkFont(size=24))
        lbl.place(relx=0.5, rely=0.5, anchor="center")

if __name__ == "__main__":
    # Initialize and run the application
    app = HospitalApp()
    app.mainloop()