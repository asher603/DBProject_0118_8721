import os
import sys
# Path safeguard: Ensures 'src' subdirectories are always visible to the Python interpreter
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from database import DatabaseManager
from views.main_menu_view import MainMenuView
from views.generic_crud_view import GenericCrudView
from views.special_operations_view import SpecialOperationsView

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class HospitalApp(ctk.CTk):
    """
    Main Application window wrapper bootstrap. Handles linear clean state switches 
    directly starting from the Main Menu Hub -> Concrete Sub-Workspaces.
    """
    def __init__(self):
        super().__init__()

        self.title("Hospital Management Enterprise System")
        self.geometry("1200x800")
        
        # Initialize database link
        self.db_manager = DatabaseManager()

        # Core frame container where sub-views get mounted/unmounted dynamically
        self.view_container = ctk.CTkFrame(self, fg_color="transparent")
        self.view_container.pack(fill="both", expand=True)

        # NEW: Trigger the Main Menu Hub directly upon application launch
        self.show_main_menu_hub()

    def clear_workspace(self):
        for widget in self.view_container.winfo_children():
            widget.destroy()

    def show_main_menu_hub(self):
        self.clear_workspace()
        view = MainMenuView(
            self.view_container, 
            on_crud_click=self.show_crud_workspace, 
            on_special_click=self.show_special_workspace
        )
        view.pack(fill="both", expand=True)

    def show_crud_workspace(self):
        self.clear_workspace()
        view = GenericCrudView(self.view_container, self.db_manager, on_back_click=self.show_main_menu_hub)
        view.pack(fill="both", expand=True)

    def show_special_workspace(self):
        self.clear_workspace()
        view = SpecialOperationsView(self.view_container, self.db_manager, on_back_click=self.show_main_menu_hub)
        view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()