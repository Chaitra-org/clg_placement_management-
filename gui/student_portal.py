"""
Student Portal GUI
Personalized dashboard for logged-in students to view profile,
discover eligible job openings, apply directly, and track application status.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from models.user import User
from models.student import Student
from storage.data_manager import DataManager
from gui.style import (
    CARD_BG, PAGE_BG, TEXT_PRIMARY, TEXT_MUTED,
    FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD,
    ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMBER, ACCENT_RED, ACCENT_PURPLE
)


class StudentPortal(ttk.Frame):
    """Personalized Student Portal."""

    def __init__(self, parent, user: User, data_manager: DataManager, on_logout=None):
        super().__init__(parent, style="Page.TFrame")
        self.user = user
        self.dm = data_manager
        self.on_logout = on_logout

        self.student = self.dm.get_student_by_roll(self.user.roll_no)

        self._build_ui()
        self.refresh_all()

    def _build_ui(self):
        """Construct the Student Portal interface."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ----------------------------------------------------
        # Top Profile Banner Card
        # ----------------------------------------------------
        profile_card = tk.LabelFrame(
            self,
            text=" 👤 Student Profile Overview ",
            font=FONT_HEADING,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            padx=16,
            pady=12,
            relief="solid",
            bd=1
        )
        profile_card.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 6))
        profile_card.columnconfigure((0, 1, 2, 3), weight=1)

        st_name = self.student.name if self.student else self.user.username.upper()
        st_roll = self.student.roll_no if self.student else self.user.roll_no
        st_dept = self.student.department if self.student else "N/A"
        st_cgpa = f"{self.student.cgpa:.2f}" if self.student else "N/A"
        st_skills = self.student.skills if self.student else "None"

        # Column 0: Name & Roll
        col0 = tk.Frame(profile_card, bg=CARD_BG)
        col0.grid(row=0, column=0, sticky="w")
        tk.Label(col0, text=st_name, font=(FONT_HEADING[0], 13, "bold"), fg=ACCENT_BLUE, bg=CARD_BG).pack(anchor="w")
        tk.Label(col0, text=f"Roll No: {st_roll}", font=FONT_BODY_BOLD, fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")

        # Column 1: Dept & CGPA
        col1 = tk.Frame(profile_card, bg=CARD_BG)
        col1.grid(row=0, column=1, sticky="w")
        tk.Label(col1, text=f"Dept: {st_dept}", font=FONT_BODY, fg=TEXT_PRIMARY, bg=CARD_BG).pack(anchor="w")
        tk.Label(col1, text=f"Academic CGPA: {st_cgpa}", font=FONT_BODY_BOLD, fg=ACCENT_GREEN, bg=CARD_BG).pack(anchor="w")

        # Column 2: Skills
        col2 = tk.Frame(profile_card, bg=CARD_BG)
        col2.grid(row=0, column=2, sticky="ew", padx=10)
        tk.Label(col2, text="Registered Skills:", font=FONT_BODY_BOLD, fg=TEXT_MUTED, bg=CARD_BG).pack(anchor="w")
        self.lbl_skills_display = tk.Label(col2, text=st_skills, font=FONT_BODY, fg=TEXT_PRIMARY, bg=CARD_BG, wraplength=320, justify="left")
        self.lbl_skills_display.pack(anchor="w")

        # Column 3: Edit Skills Button
        col3 = tk.Frame(profile_card, bg=CARD_BG)
        col3.grid(row=0, column=3, sticky="e")
        btn_edit_skills = tk.Button(
            col3,
            text="✏️ Update Skills",
            font=FONT_BODY,
            bg="#E2E8F0",
            fg=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self.open_update_skills_dialog
        )
        btn_edit_skills.pack(anchor="e")

        # ----------------------------------------------------
        # Notebook: 2 Tabs (Eligible Jobs & My Applications)
        # ----------------------------------------------------
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=14, pady=(6, 12))

        # Tab 1: Available & Eligible Jobs
        tab_jobs = ttk.Frame(self.notebook, style="Page.TFrame")
        self.notebook.add(tab_jobs, text="  💼 Job Openings & Eligibility  ")
        self._build_jobs_tab(tab_jobs)

        # Tab 2: My Applications & Status
        tab_my_apps = ttk.Frame(self.notebook, style="Page.TFrame")
        self.notebook.add(tab_my_apps, text="  📑 My Application Statuses  ")
        self._build_my_apps_tab(tab_my_apps)

    def _build_jobs_tab(self, parent):
        """Construct the Job Openings and Apply tab."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        # Filter and Action header
        header_bar = tk.Frame(parent, bg=PAGE_BG)
        header_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))

        tk.Label(
            header_bar,
            text="Companies match based on your CGPA and technical skills.",
            font=FONT_BODY,
            fg=TEXT_MUTED,
            bg=PAGE_BG
        ).pack(side="left")

        btn_apply = tk.Button(
            header_bar,
            text="🚀 Apply for Selected Job",
            font=FONT_BODY_BOLD,
            bg=ACCENT_BLUE,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=5,
            command=self.apply_to_selected_job
        )
        btn_apply.pack(side="right")

        btn_refresh_jobs = tk.Button(
            header_bar,
            text="↺ Refresh Openings",
            font=FONT_BODY,
            bg="#E2E8F0",
            fg=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=4,
            command=self.load_jobs
        )
        btn_refresh_jobs.pack(side="right", padx=(0, 8))

        # Table frame
        tbl_frame = tk.Frame(parent, bg=CARD_BG, relief="solid", bd=1)
        tbl_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tbl_frame.columnconfigure(0, weight=1)
        tbl_frame.rowconfigure(0, weight=1)

        cols = ("cid", "comp", "role", "min_cgpa", "pkg", "eligible", "matched_skills", "status")
        self.tree_jobs = ttk.Treeview(tbl_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_jobs.heading("cid", text="Job ID")
        self.tree_jobs.heading("comp", text="Company")
        self.tree_jobs.heading("role", text="Role")
        self.tree_jobs.heading("min_cgpa", text="Min CGPA")
        self.tree_jobs.heading("pkg", text="Package")
        self.tree_jobs.heading("eligible", text="Eligible?")
        self.tree_jobs.heading("matched_skills", text="Matching Skills")
        self.tree_jobs.heading("status", text="Application Status")

        self.tree_jobs.column("cid", width=70, anchor="center")
        self.tree_jobs.column("comp", width=140, anchor="w")
        self.tree_jobs.column("role", width=150, anchor="w")
        self.tree_jobs.column("min_cgpa", width=75, anchor="center")
        self.tree_jobs.column("pkg", width=80, anchor="center")
        self.tree_jobs.column("eligible", width=80, anchor="center")
        self.tree_jobs.column("matched_skills", width=180, anchor="w")
        self.tree_jobs.column("status", width=120, anchor="center")

        self.tree_jobs.tag_configure("Eligible", foreground=ACCENT_GREEN, background="#ECFDF5")
        self.tree_jobs.tag_configure("Ineligible", foreground=ACCENT_RED, background="#FEF2F2")

        scroll_y = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree_jobs.yview)
        scroll_x = ttk.Scrollbar(tbl_frame, orient="horizontal", command=self.tree_jobs.xview)
        self.tree_jobs.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree_jobs.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

    def _build_my_apps_tab(self, parent):
        """Construct the My Applications tracking tab."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        # Header bar
        header_bar = tk.Frame(parent, bg=PAGE_BG)
        header_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))

        self.lbl_app_count = tk.Label(header_bar, text="You have submitted 0 applications.", font=FONT_BODY_BOLD, fg=TEXT_PRIMARY, bg=PAGE_BG)
        self.lbl_app_count.pack(side="left")

        btn_withdraw = tk.Button(
            header_bar,
            text="❌ Withdraw Application",
            font=FONT_BODY,
            bg=ACCENT_RED,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self.withdraw_application
        )
        btn_withdraw.pack(side="right")

        btn_refresh = tk.Button(
            header_bar,
            text="↺ Refresh Status",
            font=FONT_BODY,
            bg="#E2E8F0",
            fg=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=4,
            command=self.load_my_applications
        )
        btn_refresh.pack(side="right", padx=(0, 8))

        # Table frame
        tbl_frame = tk.Frame(parent, bg=CARD_BG, relief="solid", bd=1)
        tbl_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tbl_frame.columnconfigure(0, weight=1)
        tbl_frame.rowconfigure(0, weight=1)

        cols = ("appid", "company", "role", "applied_date", "status")
        self.tree_my_apps = ttk.Treeview(tbl_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_my_apps.heading("appid", text="Application ID")
        self.tree_my_apps.heading("company", text="Company")
        self.tree_my_apps.heading("role", text="Role Applied")
        self.tree_my_apps.heading("applied_date", text="Date Applied")
        self.tree_my_apps.heading("status", text="Recruitment Status")

        self.tree_my_apps.column("appid", width=100, anchor="center")
        self.tree_my_apps.column("company", width=180, anchor="w")
        self.tree_my_apps.column("role", width=200, anchor="w")
        self.tree_my_apps.column("applied_date", width=110, anchor="center")
        self.tree_my_apps.column("status", width=130, anchor="center")

        self.tree_my_apps.tag_configure("Selected", foreground=ACCENT_GREEN, background="#ECFDF5")
        self.tree_my_apps.tag_configure("Shortlisted", foreground=ACCENT_AMBER, background="#FFFBEB")
        self.tree_my_apps.tag_configure("Rejected", foreground=ACCENT_RED, background="#FEF2F2")
        self.tree_my_apps.tag_configure("Applied", foreground=ACCENT_BLUE, background="#EFF6FF")

        scroll_y = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree_my_apps.yview)
        scroll_x = ttk.Scrollbar(tbl_frame, orient="horizontal", command=self.tree_my_apps.xview)
        self.tree_my_apps.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree_my_apps.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

    # ----------------------------------------------------
    # Operations
    # ----------------------------------------------------

    def refresh_all(self):
        """Reload student profile, available jobs, and application status."""
        self.student = self.dm.get_student_by_roll(self.user.roll_no)
        if self.student:
            self.lbl_skills_display.config(text=self.student.skills)
        self.load_jobs()
        self.load_my_applications()

    def load_jobs(self):
        """Evaluate company openings against student profile."""
        for item in self.tree_jobs.get_children():
            self.tree_jobs.delete(item)

        if not self.student:
            return

        companies_df = self.dm.get_all_companies_df()
        my_apps = self.dm.get_student_applications(self.student.roll_no)

        # Map existing application statuses
        existing_apps_map = {}
        if not my_apps.empty:
            for _, r in my_apps.iterrows():
                key = (str(r["Company Name"]).lower(), str(r["Role"]).lower())
                existing_apps_map[key] = str(r["Status"])

        for _, r in companies_df.iterrows():
            comp_name = r["Company Name"]
            role = r["Role"]
            min_cgpa = float(r["Min CGPA"])
            pkg = f"{float(r['Package (LPA)']):.1f} LPA"

            # Check eligibility
            from models.company import Company
            comp_obj = Company.from_dict(r.to_dict())
            is_elig, reason, matched = comp_obj.is_student_eligible(self.student)

            elig_label = "Eligible" if is_elig else "Ineligible"
            tag = "Eligible" if is_elig else "Ineligible"

            # Check if student already applied
            app_key = (comp_name.lower(), role.lower())
            if app_key in existing_apps_map:
                status_txt = f"Applied ({existing_apps_map[app_key]})"
            else:
                status_txt = "Not Applied"

            matched_txt = ", ".join(matched) if matched else "None"

            self.tree_jobs.insert(
                "",
                "end",
                values=(
                    r["Company ID"],
                    comp_name,
                    role,
                    f"{min_cgpa:.2f}",
                    pkg,
                    elig_label,
                    matched_txt,
                    status_txt
                ),
                tags=(tag,)
            )

    def load_my_applications(self):
        """Load current student's applications."""
        for item in self.tree_my_apps.get_children():
            self.tree_my_apps.delete(item)

        if not self.student:
            return

        df = self.dm.get_student_applications(self.student.roll_no)
        count = len(df)
        self.lbl_app_count.config(text=f"You have submitted {count} job application(s).")

        if not df.empty:
            for _, r in df.iterrows():
                status = str(r["Status"])
                self.tree_my_apps.insert(
                    "",
                    "end",
                    values=(
                        r["Application ID"],
                        r["Company Name"],
                        r["Role"],
                        r["Applied Date"],
                        status
                    ),
                    tags=(status,)
                )

    def apply_to_selected_job(self):
        """Submit application for the selected job."""
        selected = self.tree_jobs.selection()
        if not selected:
            messagebox.showwarning("Notice", "Please select a job opening from the table to apply.")
            return

        vals = self.tree_jobs.item(selected[0], "values")
        cid, comp_name, role, min_cgpa, pkg, elig_label, matched, current_status = vals

        if "Applied" in current_status:
            messagebox.showinfo("Already Applied", f"You have already applied for '{role}' at {comp_name}.")
            return

        if elig_label == "Ineligible":
            proceed = messagebox.askyesno(
                "Eligibility Warning",
                f"Your profile currently does not meet the minimum criteria for this job ({comp_name} - {role}).\n\nDo you still want to apply?",
                icon="warning"
            )
            if not proceed:
                return

        try:
            app = self.dm.apply_student(self.student.roll_no, comp_name, role)
            messagebox.showinfo(
                "Application Successful! 🎉",
                f"You have successfully applied to {comp_name} for the role of '{role}'!\nApplication ID: {app.app_id}"
            )
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit application: {e}")

    def withdraw_application(self):
        """Withdraw an application if still in 'Applied' status."""
        selected = self.tree_my_apps.selection()
        if not selected:
            messagebox.showwarning("Notice", "Please select an application to withdraw.")
            return

        vals = self.tree_my_apps.item(selected[0], "values")
        app_id, comp, role, date, status = vals

        if status.lower() != "applied":
            messagebox.showwarning(
                "Cannot Withdraw",
                f"This application is already marked as '{status}'. Only applications in 'Applied' status can be withdrawn."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Withdrawal",
            f"Are you sure you want to withdraw your application to {comp} for '{role}'?",
            icon="question"
        )
        if not confirm:
            return

        try:
            self.dm.delete_application(app_id)
            messagebox.showinfo("Withdrawn", "Application withdrawn successfully.")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to withdraw application: {e}")

    def open_update_skills_dialog(self):
        """Open a pop-up dialog allowing the student to update technical skills."""
        if not self.student:
            return

        dialog = tk.Toplevel(self)
        dialog.title("Update Skills")
        dialog.geometry("420x220")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text="Update Your Technical Skills", font=FONT_HEADING, fg=TEXT_PRIMARY).pack(pady=(16, 6))
        tk.Label(dialog, text="Enter comma-separated skills (e.g. Python, SQL, React, AWS):", font=FONT_BODY, fg=TEXT_MUTED).pack(pady=(0, 8))

        entry_skills = ttk.Entry(dialog, font=FONT_BODY, width=44)
        entry_skills.pack(pady=4)
        entry_skills.insert(0, self.student.skills)

        def save_skills():
            new_skills = entry_skills.get().strip()
            if not new_skills:
                messagebox.showwarning("Notice", "Skills cannot be empty.", parent=dialog)
                return

            try:
                updated_student = Student(
                    roll_no=self.student.roll_no,
                    name=self.student.name,
                    department=self.student.department,
                    cgpa=self.student.cgpa,
                    skills=new_skills
                )
                self.dm.update_student(self.student.roll_no, updated_student)
                messagebox.showinfo("Saved", "Skills updated successfully!", parent=dialog)
                dialog.destroy()
                self.refresh_all()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update skills: {e}", parent=dialog)

        btn_save = tk.Button(
            dialog,
            text="💾 Save Skills",
            font=FONT_BODY_BOLD,
            bg=ACCENT_BLUE,
            fg="#FFFFFF",
            relief="flat",
            padx=12,
            pady=4,
            command=save_skills
        )
        btn_save.pack(pady=(14, 0))
