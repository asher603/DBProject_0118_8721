import customtkinter as ctk
from tkinter import messagebox

class EntityDetailPopup(ctk.CTkToplevel):
    def __init__(self, parent, pk_value, cfg, db_manager, on_modified_callback):
        super().__init__(parent)
        self.db_manager = db_manager
        self.cfg = cfg
        self.pk_value = pk_value
        self.on_modified_callback = on_modified_callback

        self.title(f"Manage Record Instance Details — {cfg['table']}")
        self.geometry("500x600")
        self.transient(parent)
        self.grab_set() # Forces modal view control focus

        # Main Header Title Label
        ctk.CTkLabel(self, text=f"Reviewing {cfg['table']} [Key ID: {pk_value}]", font=("Arial", 16, "bold")).pack(pady=15)

        # Container Frame Setup
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=440, height=400)
        self.scroll_frame.pack(pady=10, fill="both", expand=True, padx=20)

        self.input_widgets = {}
        self.fetch_and_populate_record_fields()

        # Action Buttons Layout Frame Setup
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.pack(fill="x", pady=20, padx=20)

        # Close/Back Navigation arrow alternate behavior
        self.btn_back = ctk.CTkButton(self.actions_frame, text="← Return Back", command=self.destroy, width=110, fg_color="gray")
        self.btn_back.pack(side="left", padx=5)

        if self.cfg["write"]:
            self.btn_update = ctk.CTkButton(self.actions_frame, text="Apply Updates", command=self.execute_update_action, width=140, fg_color="blue")
            self.btn_update.pack(side="right", padx=5)

        self.btn_delete = ctk.CTkButton(self.actions_frame, text="Delete Permanently", command=self.execute_delete_action, width=140, fg_color="red")
        self.btn_delete.pack(side="right", padx=5)

    def fetch_and_populate_record_fields(self):
        # Always read fresh values from Database directly using standard atomic primary key selectors
        query = f"SELECT * FROM {self.cfg['table']} WHERE {self.cfg['pk']} = %s"
        record = self.db_manager.fetch_one(query, (self.pk_value,))

        if not record:
            messagebox.showerror("Error", "Unable to locate targeted record instance on server storage.")
            self.destroy()
            return

        for col, label in zip(self.cfg["cols"], self.cfg["labels"]):
            ctk.CTkLabel(self.scroll_frame, text=f"{label}:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(8, 2))
            
            entry = ctk.CTkEntry(self.scroll_frame, width=380)
            entry.insert(0, str(record.get(col.lower(), "")))
            
            # Primary Key elements are blocked out explicitly from arbitrary edits
            if col.lower() == self.cfg["pk"].lower() or not self.cfg["write"]:
                entry.configure(state="disabled")

            entry.pack(anchor="w", padx=20, pady=2)
            self.input_widgets[col] = entry

    def execute_update_action(self):
        update_clauses = []
        values = []

        for col, widget in self.input_widgets.items():
            if col.lower() == self.cfg["pk"].lower():
                continue
            update_clauses.append(f"{col} = %s")
            values.append(widget.get())

        values.append(self.pk_value) # For WHERE clause restriction filter
        sql = f"UPDATE {self.cfg['table']} SET {', '.join(update_clauses)} WHERE {self.cfg['pk']} = %s"

        try:
            self.db_manager.execute_non_query(sql, tuple(values))
            messagebox.showinfo("Success", "Record attributes modified successfully inside system storage!")
            self.on_modified_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("DML Execution Violation Exception", str(e))

    def execute_delete_action(self):
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you completely certain you want to purge this record from {self.cfg['table']}?")
        if not confirm:
            return

        sql = f"DELETE FROM {self.cfg['table']} WHERE {self.cfg['pk']} = %s"
        try:
            self.db_manager.execute_non_query(sql, (self.pk_value,))
            messagebox.showinfo("Purged", "Record completely wiped out from hospital directories.")
            self.on_modified_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Foreign Key Cascade Restrict Constraint Triggered", f"Purge rejected! This record is actively linked or referenced elsewhere.\n\nDetails: {str(e)}")