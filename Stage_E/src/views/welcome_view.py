import customtkinter as ctk

class WelcomeView(ctk.CTkFrame):
    """
    Initial Welcome Gate Screen (Login/Enter Screen) managed as a standalone view component.
    """
    def __init__(self, master, on_enter_command):
        super().__init__(master)
        self.on_enter_command = on_enter_command

        # Center alignment structure for the welcome gate
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.lbl_gate_title = ctk.CTkLabel(
            self, 
            text="Hospital Management System", 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.lbl_gate_title.grid(row=0, column=0, pady=(60, 10))

        self.lbl_gate_subtitle = ctk.CTkLabel(
            self, 
            text="Production Database Client Application", 
            font=ctk.CTkFont(size=16, slant="italic")
        )
        self.lbl_gate_subtitle.grid(row=1, column=0, pady=10)

        self.btn_enter_system = ctk.CTkButton(
            self, 
            text="Enter System", 
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200, 
            height=45,
            command=self.on_enter_command
        )
        self.btn_enter_system.grid(row=2, column=0, pady=(10, 80))