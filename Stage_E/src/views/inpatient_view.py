import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from datetime import date

class InpatientView(ctk.CTkFrame):
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_admissions = self.tabview.add("Inpatient Admissions")
        self.tab_rooms = self.tabview.add("Rooms Management")
        self.tab_beds = self.tabview.add("Beds Management")

        # Caching dictionaries for cleaner UI names mapping to raw IDs
        self.patient_map = {}
        self.bed_map = {}
        self.dept_map = {}
        self.room_map = {}

        self.load_all_mappings()
        self.setup_admissions_subtabs()
        self.setup_rooms_subtabs()
        self.setup_beds_subtabs()

    def load_all_mappings(self):
        # Patients
        p_recs, _ = self.db_manager.get_all_patients()
        self.patient_map = {f"{r[1]} {r[2]} (ID: {r[0]})": r[0] for r in p_recs} if p_recs else {}
        # Beds
        b_recs, _ = self.db_manager.get_all_beds()
        self.bed_map = {f"Bed No. {r[1]} (In Room: {r[2]})": r[0] for r in b_recs} if b_recs else {}
        # Departments
        d_recs, _ = self.db_manager.get_all_departments()
        self.dept_map = {str(r[1]): r[0] for r in d_recs} if d_recs else {}
        # Rooms
        r_recs, _ = self.db_manager.get_all_rooms()
        self.room_map = {f"Room {r[1]} ({r[2]})": r[0] for r in r_recs} if r_recs else {}

    # -------------------------------------------------------------------------
    # ADMISSIONS TAB
    # -------------------------------------------------------------------------
    def setup_admissions_subtabs(self):
        inner_tabs = ctk.CTkTabview(self.tab_admissions)
        inner_tabs.pack(fill="both", expand=True)
        
        t_view = inner_tabs.add("View Admissions")
        t_add = inner_tabs.add("New Admission")
        t_manage = inner_tabs.add("Update/Delete")

        # View
        t_view.grid_columnconfigure(0, weight=1)
        t_view.grid_rowconfigure(0, weight=1)
        cols = ("id", "patient", "bed", "adm_date", "dis_date")
        self.tree_adm = ttk.Treeview(t_view, columns=cols, show="headings")
        for c, t in zip(cols, ["Admission ID", "Patient Name", "Bed Number", "Admission Date", "Discharge Date"]):
            self.tree_adm.heading(c, text=t); self.tree_adm.column(c, anchor="center")
        self.tree_adm.grid(row=0, column=0, sticky="nsew")
        
        # Add Form
        f_add = ctk.CTkFrame(t_add, fg_color="transparent")
        f_add.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f_add, text="Select Patient:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.cmb_adm_p = ctk.CTkComboBox(f_add, values=list(self.patient_map.keys()), width=220)
        self.cmb_adm_p.grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(f_add, text="Assign Bed:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.cmb_adm_b = ctk.CTkComboBox(f_add, values=list(self.bed_map.keys()), width=220)
        self.cmb_adm_b.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(f_add, text="Admission Date:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.ent_adm_date = ctk.CTkEntry(f_add, width=220); self.ent_adm_date.insert(0, str(date.today()))
        self.ent_adm_date.grid(row=2, column=1, padx=10, pady=5)
        ctk.CTkButton(f_add, text="Register Admission", command=self.add_admission_action).grid(row=3, column=0, columnspan=2, pady=15)

        # Manage Form
        f_mng = ctk.CTkFrame(t_manage, fg_color="transparent")
        f_mng.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f_mng, text="Enter Admission ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.ent_mng_adm_id = ctk.CTkEntry(f_mng, width=150)
        self.ent_mng_adm_id.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(f_mng, text="Fetch", width=70, command=self.fetch_admission_action).grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkLabel(f_mng, text="Patient:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.cmb_mng_adm_p = ctk.CTkComboBox(f_mng, values=list(self.patient_map.keys()), state="disabled", width=200)
        self.cmb_mng_adm_p.grid(row=1, column=1, columnspan=2, pady=5)

        ctk.CTkLabel(f_mng, text="Bed:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.cmb_mng_adm_b = ctk.CTkComboBox(f_mng, values=list(self.bed_map.keys()), state="disabled", width=200)
        self.cmb_mng_adm_b.grid(row=2, column=1, columnspan=2, pady=5)

        ctk.CTkLabel(f_mng, text="Adm Date:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.ent_mng_adm_d1 = ctk.CTkEntry(f_mng, state="disabled", width=200)
        self.ent_mng_adm_d1.grid(row=3, column=1, columnspan=2, pady=5)

        ctk.CTkLabel(f_mng, text="Discharge Date:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.ent_mng_adm_d2 = ctk.CTkEntry(f_mng, state="disabled", width=200)
        self.ent_mng_adm_d2.grid(row=4, column=1, columnspan=2, pady=5)

        self.btn_adm_upd = ctk.CTkButton(f_mng, text="Update", state="disabled", fg_color="green", command=self.update_admission_action)
        self.btn_adm_upd.grid(row=5, column=0, pady=15)
        self.btn_adm_del = ctk.CTkButton(f_mng, text="Delete", state="disabled", fg_color="red", command=self.delete_admission_action)
        self.btn_adm_del.grid(row=5, column=1, pady=15)

        self.load_admissions_grid()

    def load_admissions_grid(self):
        for r in self.tree_adm.get_children(): self.tree_adm.delete(r)
        records, _ = self.db_manager.get_detailed_admissions()
        if records:
            for rec in records:
                row = list(rec)
                row[3], row[4] = str(row[3]), str(row[4]) if row[4] else "Active Stay"
                self.tree_adm.insert("", tk.END, values=row)

    def add_admission_action(self):
        p_id = self.patient_map.get(self.cmb_adm_p.get())
        b_id = self.bed_map.get(self.cmb_adm_b.get())
        if p_id and b_id and self.db_manager.add_new_admission(self.ent_adm_date.get(), p_id, b_id):
            messagebox.showinfo("Success", "Inpatient admission logged successfully.")
            self.load_admissions_grid()

    def fetch_admission_action(self):
        recs, _ = self.db_manager.get_admission_by_id(self.ent_mng_adm_id.get().strip())
        if not recs:
            messagebox.showerror("Error", "Admission ID record not found."); return
        rec = recs[0]
        for w in [self.cmb_mng_adm_p, self.cmb_mng_adm_b, self.ent_mng_adm_d1, self.ent_mng_adm_d2]: w.configure(state="normal")
        self.ent_mng_adm_d1.delete(0, tk.END); self.ent_mng_adm_d1.insert(0, str(rec[1]))
        self.ent_mng_adm_d2.delete(0, tk.END); self.ent_mng_adm_d2.insert(0, str(rec[2]) if rec[2] else "")
        
        for k, v in self.patient_map.items(): 
            if v == rec[3]: self.cmb_mng_adm_p.set(k); break
        for k, v in self.bed_map.items(): 
            if v == rec[4]: self.cmb_mng_adm_b.set(k); break
            
        self.btn_adm_upd.configure(state="normal"); self.btn_adm_del.configure(state="normal")

    def update_admission_action(self):
        p_id = self.patient_map.get(self.cmb_mng_adm_p.get())
        b_id = self.bed_map.get(self.cmb_mng_adm_b.get())
        if self.db_manager.update_admission_info(self.ent_mng_adm_id.get().strip(), self.ent_mng_adm_d1.get(), self.ent_mng_adm_d2.get(), p_id, b_id):
            messagebox.showinfo("Success", "Admission data updated."); self.load_admissions_grid()

    def delete_admission_action(self):
        if messagebox.askyesno("Confirm", "Delete this record permanently?"):
            if self.db_manager.delete_admission(self.ent_mng_adm_id.get().strip()):
                messagebox.showinfo("Deleted", "Record removed successfully."); self.load_admissions_grid()

    # -------------------------------------------------------------------------
    # ROOMS TAB
    # -------------------------------------------------------------------------
    def setup_rooms_subtabs(self):
        inner_tabs = ctk.CTkTabview(self.tab_rooms)
        inner_tabs.pack(fill="both", expand=True)
        t_view = inner_tabs.add("View Rooms")
        t_add = inner_tabs.add("Add Room")
        t_manage = inner_tabs.add("Update/Delete")

        # View
        t_view.grid_columnconfigure(0, weight=1); t_view.grid_rowconfigure(0, weight=1)
        self.tree_rooms = ttk.Treeview(t_view, columns=("id", "num", "type", "dept"), show="headings")
        for c, t in zip(["id", "num", "type", "dept"], ["Room ID", "Room Number", "Room Type", "Department"]):
            self.tree_rooms.heading(c, text=t); self.tree_rooms.column(c, anchor="center")
        self.tree_rooms.grid(row=0, column=0, sticky="nsew")

        # Add
        f_add = ctk.CTkFrame(t_add, fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")
        f_add_fr = ctk.CTkFrame(t_add, fg_color="transparent"); f_add_fr.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f_add_fr, text="Room Number:").grid(row=0, column=0, padx=10, pady=5)
        self.ent_r_num = ctk.CTkEntry(f_add_fr, width=200); self.ent_r_num.grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(f_add_fr, text="Room Type:").grid(row=1, column=0, padx=10, pady=5)
        self.ent_r_type = ctk.CTkEntry(f_add_fr, width=200); self.ent_r_type.grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkLabel(f_add_fr, text="Department:").grid(row=2, column=0, padx=10, pady=5)
        self.cmb_r_dept = ctk.CTkComboBox(f_add_fr, values=list(self.dept_map.keys()), width=200); self.cmb_r_dept.grid(row=2, column=1, padx=10, pady=5)
        ctk.CTkButton(f_add_fr, text="Save Room", command=self.add_room_action).grid(row=3, column=0, columnspan=2, pady=15)

        # Manage Form
        f_mng = ctk.CTkFrame(t_manage, fg_color="transparent"); f_mng.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f_mng, text="Room ID:").grid(row=0, column=0, padx=10, pady=5)
        self.ent_mng_room_id = ctk.CTkEntry(f_mng, width=120); self.ent_mng_room_id.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(f_mng, text="Fetch", width=70, command=self.fetch_room_action).grid(row=0, column=2, padx=5, pady=5)
        
        ctk.CTkLabel(f_mng, text="Room Number:").grid(row=1, column=0, padx=10, pady=5)
        self.ent_mng_r_num = ctk.CTkEntry(f_mng, state="disabled", width=200); self.ent_mng_r_num.grid(row=1, column=1, columnspan=2, pady=5)
        ctk.CTkLabel(f_mng, text="Room Type:").grid(row=2, column=0, padx=10, pady=5)
        self.ent_mng_r_type = ctk.CTkEntry(f_mng, state="disabled", width=200); self.ent_mng_r_type.grid(row=2, column=1, columnspan=2, pady=5)
        ctk.CTkLabel(f_mng, text="Department:").grid(row=3, column=0, padx=10, pady=5)
        self.cmb_mng_r_dept = ctk.CTkComboBox(f_mng, values=list(self.dept_map.keys()), state="disabled", width=200); self.cmb_mng_r_dept.grid(row=3, column=1, columnspan=2, pady=5)

        self.btn_r_upd = ctk.CTkButton(f_mng, text="Update", state="disabled", fg_color="green", command=self.update_room_action); self.btn_r_upd.grid(row=4, column=0, pady=15)
        self.btn_r_del = ctk.CTkButton(f_mng, text="Delete", state="disabled", fg_color="red", command=self.delete_room_action); self.btn_r_del.grid(row=4, column=1, pady=15)

        self.load_rooms_grid()

    def load_rooms_grid(self):
        for r in self.tree_rooms.get_children(): self.tree_rooms.delete(r)
        recs, _ = self.db_manager.get_all_rooms()
        if recs:
            for rec in recs: self.tree_rooms.insert("", tk.END, values=rec)

    def add_room_action(self):
        d_id = self.dept_map.get(self.cmb_r_dept.get())
        if d_id and self.db_manager.add_new_room(self.ent_r_num.get(), self.ent_r_type.get(), d_id):
            messagebox.showinfo("Success", "Room added successfully."); self.load_rooms_grid(); self.load_all_mappings()

    def fetch_room_action(self):
        recs, _ = self.db_manager.get_room_by_id(self.ent_mng_room_id.get().strip())
        if not recs: messagebox.showerror("Error", "Not found."); return
        rec = recs[0]
        for w in [self.ent_mng_r_num, self.ent_mng_r_type, self.cmb_mng_r_dept]: w.configure(state="normal")
        self.ent_mng_r_num.delete(0, tk.END); self.ent_mng_r_num.insert(0, str(rec[1]))
        self.ent_mng_r_type.delete(0, tk.END); self.ent_mng_r_type.insert(0, str(rec[2]))
        for k, v in self.dept_map.items():
            if v == rec[3]: self.cmb_mng_r_dept.set(k); break
        self.btn_r_upd.configure(state="normal"); self.btn_r_del.configure(state="normal")

    def update_room_action(self):
        d_id = self.dept_map.get(self.cmb_mng_r_dept.get())
        if self.db_manager.update_room_info(self.ent_mng_room_id.get().strip(), self.ent_mng_r_num.get(), self.ent_mng_r_type.get(), d_id):
            messagebox.showinfo("Success", "Room updated."); self.load_rooms_grid(); self.load_all_mappings()

    def delete_room_action(self):
        if self.db_manager.delete_room(self.ent_mng_room_id.get().strip()):
            messagebox.showinfo("Deleted", "Room removed."); self.load_rooms_grid(); self.load_all_mappings()

    # -------------------------------------------------------------------------
    # BEDS TAB
    # -------------------------------------------------------------------------
    def setup_beds_subtabs(self):
        inner_tabs = ctk.CTkTabview(self.tab_beds)
        inner_tabs.pack(fill="both", expand=True)
        t_view = inner_tabs.add("View Beds")
        t_add = inner_tabs.add("Add Bed")
        t_manage = inner_tabs.add("Update/Delete")

        # View
        t_view.grid_columnconfigure(0, weight=1); t_view.grid_rowconfigure(0, weight=1)
        self.tree_beds = ttk.Treeview(t_view, columns=("id", "num", "room"), show="headings")
        for c, t in zip(["id", "num", "room"], ["Bed ID", "Bed Number", "Located in Room"]):
            self.tree_beds.heading(c, text=t); self.tree_beds.column(c, anchor="center")
        self.tree_beds.grid(row=0, column=0, sticky="nsew")

        # Add
        f_add_fr = ctk.CTkFrame(t_add, fg_color="transparent"); f_add_fr.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f_add_fr, text="Bed Number:").grid(row=0, column=0, padx=10, pady=5)
        self.ent_b_num = ctk.CTkEntry(f_add_fr, width=200); self.ent_b_num.grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(f_add_fr, text="Assign to Room:").grid(row=1, column=0, padx=10, pady=5)
        self.cmb_b_room = ctk.CTkComboBox(f_add_fr, values=list(self.room_map.keys()), width=200); self.cmb_b_room.grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkButton(f_add_fr, text="Save Bed", command=self.add_bed_action).grid(row=2, column=0, columnspan=2, pady=15)

        # Manage Form
        f_mng = ctk.CTkFrame(t_manage, fg_color="transparent"); f_mng.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f_mng, text="Bed ID:").grid(row=0, column=0, padx=10, pady=5)
        self.ent_mng_bed_id = ctk.CTkEntry(f_mng, width=120); self.ent_mng_bed_id.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(f_mng, text="Fetch", width=70, command=self.fetch_bed_action).grid(row=0, column=2, padx=5, pady=5)
        
        ctk.CTkLabel(f_mng, text="Bed Number:").grid(row=1, column=0, padx=10, pady=5)
        self.ent_mng_b_num = ctk.CTkEntry(f_mng, state="disabled", width=200); self.ent_mng_b_num.grid(row=1, column=1, columnspan=2, pady=5)
        ctk.CTkLabel(f_mng, text="Room Assigned:").grid(row=2, column=0, padx=10, pady=5)
        self.cmb_mng_b_room = ctk.CTkComboBox(f_mng, values=list(self.room_map.keys()), state="disabled", width=200); self.cmb_mng_b_room.grid(row=2, column=1, columnspan=2, pady=5)

        self.btn_b_upd = ctk.CTkButton(f_mng, text="Update", state="disabled", fg_color="green", command=self.update_bed_action); self.btn_b_upd.grid(row=3, column=0, pady=15)
        self.btn_b_del = ctk.CTkButton(f_mng, text="Delete", state="disabled", fg_color="red", command=self.delete_bed_action); self.btn_b_del.grid(row=3, column=1, pady=15)

        self.load_beds_grid()

    def load_beds_grid(self):
        for r in self.tree_beds.get_children(): self.tree_beds.delete(r)
        recs, _ = self.db_manager.get_all_beds()
        if recs:
            for rec in recs: self.tree_beds.insert("", tk.END, values=rec)

    def add_bed_action(self):
        r_id = self.room_map.get(self.cmb_b_room.get())
        if r_id and self.db_manager.add_new_bed(self.ent_b_num.get(), r_id):
            messagebox.showinfo("Success", "Bed added."); self.load_beds_grid(); self.load_all_mappings()

    def fetch_bed_action(self):
        recs, _ = self.db_manager.get_bed_by_id(self.ent_mng_bed_id.get().strip())
        if not recs: messagebox.showerror("Error", "Not found."); return
        rec = recs[0]
        for w in [self.ent_mng_b_num, self.cmb_mng_b_room]: w.configure(state="normal")
        self.ent_mng_b_num.delete(0, tk.END); self.ent_b_num.insert(0, str(rec[1]))
        for k, v in self.room_map.items():
            if v == rec[2]: self.cmb_mng_b_room.set(k); break
        self.btn_b_upd.configure(state="normal"); self.btn_b_del.configure(state="normal")

    def update_bed_action(self):
        r_id = self.room_map.get(self.cmb_mng_b_room.get())
        if self.db_manager.update_bed_info(self.ent_mng_bed_id.get().strip(), self.ent_mng_b_num.get(), r_id):
            messagebox.showinfo("Success", "Bed updated."); self.load_beds_grid(); self.load_all_mappings()

    def delete_bed_action(self):
        if self.db_manager.delete_bed(self.ent_mng_bed_id.get().strip()):
            messagebox.showinfo("Deleted", "Bed removed."); self.load_beds_grid(); self.load_all_mappings()