import customtkinter as ctk

class MainMenuView(ctk.CTkFrame):
    """
    The Core Selection Screen. Contains ONLY 2 clear, prominent buttons
    directing the user to either the Dynamic CRUD system or Special Reports.
    """
    def __init__(self, parent, on_crud_click, on_special_click):
        super().__init__(parent, fg_color="transparent")
        
        # Center layout card container
        self.menu_card = ctk.CTkFrame(self, width=600, height=420, corner_radius=20)
        self.menu_card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.menu_card, text="Hospital Control Panel", font=("Arial", 24, "bold"), text_color="#1f538d").pack(pady=(45, 10))
        ctk.CTkLabel(self.menu_card, text="Please select a workspace routing option below:", font=("Arial", 13), text_color="gray").pack(pady=(0, 40))

        # Button 1: Entity Management (CRUD)
        self.btn_crud = ctk.CTkButton(
            self.menu_card, 
            text="📂 Entity Management & CRUD", 
            font=("Arial", 15, "bold"),
            width=380,
            height=60,
            corner_radius=10,
            command=on_crud_click
        )
        self.btn_crud.pack(pady=15)

        # Button 2: Special Actions & Reports
        self.btn_special = ctk.CTkButton(
            self.menu_card, 
            text="⚡ Special Actions & Reports", 
            font=("Arial", 15, "bold"),
            fg_color="purple", 
            hover_color="#5D207A",
            width=380,
            height=60,
            corner_radius=10,
            command=on_special_click
        )
        self.btn_special.pack(pady=15)