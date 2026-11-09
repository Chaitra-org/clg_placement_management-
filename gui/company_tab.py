"""
Module 2: Company & Eligibility GUI (Admin View)
Handles registering companies/jobs and checking student eligibility criteria.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from models.company import Company
from models.student import Student
from storage.data_manager import DataManager
from gui.style import (
    CARD_BG, PAGE_BG, TEXT_PRIMARY, TEXT_MUTED,
    FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD,
    ACCENT_BLUE, ACCENT_GREEN, ACCENT_RED, ACCENT_PURPLE
)


class CompanyTab(ttk.Frame):
    """Company & Eligibility Management Interface."""

    def __init__(self, parent, data_manager: DataManager, on_data_changed=None):
        super().__init__(parent, style="Page.TFrame")
        self.dm = data_manager
        self.on_data_changed = on_data_changed

        self._build_ui()
        self.load_companies()
        self.refresh_student_dropdown()

    def _build_ui(self):
        """Build the Company and Eligibility UI."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Top Section: Register Company & Companies Table
        top_frame = tk.Frame(self, bg=PAGE_BG)
        top_frame.grid(row=0, column=0, sticky="nsew", padx=12, pady=(12, 6))
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=2)
        top_frame.rowconfigure(0, weight=1)

        # Left Card: Company Form
        form_card = tk.LabelFrame(
            top_frame,
            text=" 🏢 Post New Job Opening ",
            font=FONT_HEADING,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            padx=14,
            pady=12,
            relief="solid",
            bd=1
        )
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        form_card.columnconfigure(0, weight=1)

        row = 0
        tk.Label(form_card, text="Company ID *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=row, column=0, sticky="w", pady=(2, 2))
        self.entry_comp_id = ttk.Entry(form_card, font=FONT_BODY)
        self.entry_comp_id.grid(row=row+1, column=0, sticky="ew", pady=(0, 6))

        row += 2
        tk.Label(form_card, text="Company Name *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=row, column=0, sticky="w", pady=(2, 2))
        self.entry_comp_name = ttk.Entry(form_card, font=FONT_BODY)
        self.entry_comp_name.grid(row=row+1, column=0, sticky="ew", pady=(0, 6))

        row += 2
        tk.Label(form_card, text="Job Role *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=row, column=0, sticky="w", pady=(2, 2))
        self.entry_comp_role = ttk.Entry(form_card, font=FONT_BODY)
        self.entry_comp_role.grid(row=row+1, column=0, sticky="ew", pady=(0, 6))

        row += 2
        metric_frame = tk.Frame(form_card, bg=CARD_BG)
        metric_frame.grid(row=row, column=0, sticky="ew", pady=(2, 6))
        metric_frame.columnconfigure((0, 1), weight=1)

        tk.Label(metric_frame, text="Min CGPA *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=0, column=0, sticky="w")
        tk.Label(metric_frame, text="Package (LPA)", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=0, column=1, sticky="w")

        self.entry_min_cgpa = ttk.Entry(metric_frame, font=FONT_BODY)
        self.entry_min_cgpa.grid(row=1, column=0, sticky="ew", padx=(0, 4))

        self.entry_package = ttk.Entry(metric_frame, font=FONT_BODY)
        self.entry_package.grid(row=1, column=1, sticky="ew", padx=(4, 0))

        row += 1
        tk.Label(form_card, text="Required Skills (comma separated) *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=row, column=0, sticky="w", pady=(2, 2))
        self.entry_comp_skills = ttk.Entry(form_card, font=FONT_BODY)
        self.entry_comp_skills.grid(row=row+1, column=0, sticky="ew", pady=(0, 8))

        row += 2
        btn_frame = tk.Frame(form_card, bg=CARD_BG)
        btn_frame.grid(row=row, column=0, sticky="ew", pady=(4, 0))
        btn_frame.columnconfigure((0, 1), weight=1)

        self.btn_add_company = tk.Button(
            btn_frame,
            text="➕ Add Job Opening",
            font=FONT_BODY_BOLD,
            bg=ACCENT_GREEN,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=5,
            command=self.add_company
        )
        self.btn_add_company.grid(row=0, column=0, sticky="ew", padx=(0, 4))

        self.btn_clear_comp = tk.Button(
            btn_frame,
            text="🔄 Clear",
            font=FONT_BODY,
            bg="#E2E8F0",
            fg=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=5,
            command=self.clear_form
        )
        self.btn_clear_comp.grid(row=0, column=1, sticky="ew", padx=(4, 0))

        # Right Card: Companies Table
        table_card = tk.LabelFrame(
            top_frame,
            text=" 📋 Available Job Openings & Criteria ",
            font=FONT_HEADING,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            padx=12,
            pady=12,
            relief="solid",
            bd=1
        )
        table_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        table_card.columnconfigure(0, weight=1)
        table_card.rowconfigure(0, weight=1)

        cols = ("cid", "name", "role", "min_cgpa", "skills", "package")
        self.tree_comp = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse")

        self.tree_comp.heading("cid", text="ID")
        self.tree_comp.heading("name", text="Company")
        self.tree_comp.heading("role", text="Role")
        self.tree_comp.heading("min_cgpa", text="Min CGPA")
        self.tree_comp.heading("skills", text="Required Skills")
        self.tree_comp.heading("package", text="LPA")

        self.tree_comp.column("cid", width=65, anchor="center")
        self.tree_comp.column("name", width=120, anchor="w")
        self.tree_comp.column("role", width=140, anchor="w")
        self.tree_comp.column("min_cgpa", width=70, anchor="center")
        self.tree_comp.column("skills", width=180, anchor="w")
        self.tree_comp.column("package", width=60, anchor="center")

        scroll_comp_y = ttk.Scrollbar(table_card, orient="vertical", command=self.tree_comp.yview)
        self.tree_comp.configure(yscrollcommand=scroll_comp_y.set)

        self.tree_comp.grid(row=0, column=0, sticky="nsew")
        scroll_comp_y.grid(row=0, column=1, sticky="ns")

        self.tree_comp.bind("<<TreeviewSelect>>", self.on_company_selected)

        # Bottom Section: Eligibility Checker
        bottom_card = tk.LabelFrame(
            self,
            text=" 🎯 Eligibility Checker & Skill Matching ",
            font=FONT_HEADING,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            padx=14,
            pady=12,
            relief="solid",
            bd=1
        )
        bottom_card.grid(row=1, column=0, sticky="nsew", padx=12, pady=(6, 12))
        bottom_card.columnconfigure(0, weight=1)
        bottom_card.rowconfigure(1, weight=1)

        ctrl_frame = tk.Frame(bottom_card, bg=CARD_BG)
        ctrl_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        tk.Label(ctrl_frame, text="Check Eligible Students for Company:", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 6))

        self.combo_elig_comp = ttk.Combobox(ctrl_frame, state="readonly", width=26)
        self.combo_elig_comp.pack(side="left", padx=(0, 8))

        btn_check_comp = tk.Button(
            ctrl_frame,
            text="🔎 Find Students",
            font=FONT_BODY_BOLD,
            bg=ACCENT_BLUE,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=3,
            command=self.check_students_for_selected_company
        )
        btn_check_comp.pack(side="left", padx=(0, 16))

        ttk.Separator(ctrl_frame, orient="vertical").pack(side="left", fill="y", padx=10)

        tk.Label(ctrl_frame, text="Or Check Companies for Student:", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 6))

        self.combo_elig_student = ttk.Combobox(ctrl_frame, state="readonly", width=26)
        self.combo_elig_student.pack(side="left", padx=(0, 8))

        btn_check_st = tk.Button(
            ctrl_frame,
            text="🔎 Find Jobs",
            font=FONT_BODY_BOLD,
            bg=ACCENT_PURPLE,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=3,
            command=self.check_companies_for_selected_student
        )
        btn_check_st.pack(side="left")

        elig_table_frame = tk.Frame(bottom_card, bg=CARD_BG)
        elig_table_frame.grid(row=1, column=0, sticky="nsew")
        elig_table_frame.columnconfigure(0, weight=1)
        elig_table_frame.rowconfigure(0, weight=1)

        elig_cols = ("col1", "col2", "col3", "col4", "status", "skills", "reason")
        self.tree_elig = ttk.Treeview(elig_table_frame, columns=elig_cols, show="headings", selectmode="browse")

        self.tree_elig.heading("col1", text="Identifier")
        self.tree_elig.heading("col2", text="Name / Role")
        self.tree_elig.heading("col3", text="Department / Min CGPA")
        self.tree_elig.heading("col4", text="CGPA / Package")
        self.tree_elig.heading("status", text="Eligible?")
        self.tree_elig.heading("skills", text="Matched Skills")
        self.tree_elig.heading("reason", text="Analysis / Remarks")

        self.tree_elig.column("col1", width=85, anchor="center")
        self.tree_elig.column("col2", width=140, anchor="w")
        self.tree_elig.column("col3", width=140, anchor="w")
        self.tree_elig.column("col4", width=85, anchor="center")
        self.tree_elig.column("status", width=75, anchor="center")
        self.tree_elig.column("skills", width=160, anchor="w")
        self.tree_elig.column("reason", width=260, anchor="w")

        self.tree_elig.tag_configure("eligible", foreground=ACCENT_GREEN, background="#ECFDF5")
        self.tree_elig.tag_configure("ineligible", foreground=ACCENT_RED, background="#FEF2F2")

        scroll_elig_y = ttk.Scrollbar(elig_table_frame, orient="vertical", command=self.tree_elig.yview)
        self.tree_elig.configure(yscrollcommand=scroll_elig_y.set)

        self.tree_elig.grid(row=0, column=0, sticky="nsew")
        scroll_elig_y.grid(row=0, column=1, sticky="ns")

        self.lbl_elig_summary = tk.Label(
            bottom_card,
            text="Select a company or student above and click Find to analyze eligibility.",
            font=FONT_BODY,
            bg=CARD_BG,
            fg=TEXT_MUTED
        )
        self.lbl_elig_summary.grid(row=2, column=0, sticky="w", pady=(6, 0))

    def load_companies(self):
        """Populate the companies Treeview and company combobox."""
        for item in self.tree_comp.get_children():
            self.tree_comp.delete(item)

        df = self.dm.get_all_companies_df()
        comp_dropdown_values = []

        if not df.empty:
            for _, row in df.iterrows():
                cid = row.get("Company ID", "")
                name = row.get("Company Name", "")
                role = row.get("Role", "")
                min_cgpa = f"{float(row.get('Min CGPA', 0.0)):.2f}"
                skills = row.get("Required Skills", "")
                pkg = f"{float(row.get('Package (LPA)', 0.0)):.1f} LPA"

                self.tree_comp.insert("", "end", values=(cid, name, role, min_cgpa, skills, pkg))
                comp_dropdown_values.append(f"{cid} - {name} ({role})")

        self.combo_elig_comp["values"] = comp_dropdown_values
        if comp_dropdown_values:
            self.combo_elig_comp.set(comp_dropdown_values[0])

    def refresh_student_dropdown(self):
        """Refresh student selector in eligibility checker."""
        students_df = self.dm.get_all_students_df()
        st_values = []
        if not students_df.empty:
            for _, row in students_df.iterrows():
                st_values.append(f"{row['Roll No']} - {row['Name']}")

        self.combo_elig_student["values"] = st_values
        if st_values:
            self.combo_elig_student.set(st_values[0])

    def on_company_selected(self, event):
        """When a row is selected in the company table, pre-select in dropdown for quick check."""
        selected = self.tree_comp.selection()
        if not selected:
            return
        values = self.tree_comp.item(selected[0], "values")
        if values:
            cid, name, role = values[0], values[1], values[2]
            for val in self.combo_elig_comp["values"]:
                if cid in val:
                    self.combo_elig_comp.set(val)
                    break

    def clear_form(self):
        """Clear form entries."""
        self.entry_comp_id.delete(0, tk.END)
        self.entry_comp_name.delete(0, tk.END)
        self.entry_comp_role.delete(0, tk.END)
        self.entry_min_cgpa.delete(0, tk.END)
        self.entry_comp_skills.delete(0, tk.END)
        self.entry_package.delete(0, tk.END)

    def add_company(self):
        """Validate and add a new company job vacancy."""
        cid = self.entry_comp_id.get().strip().upper()
        name = self.entry_comp_name.get().strip()
        role = self.entry_comp_role.get().strip()
        min_cgpa_str = self.entry_min_cgpa.get().strip()
        skills = self.entry_comp_skills.get().strip()
        pkg_str = self.entry_package.get().strip() or "0.0"

        try:
            if not cid:
                raise ValueError("Company ID is required (e.g. CMP06).")
            if not name:
                raise ValueError("Company Name is required.")
            if not role:
                raise ValueError("Job Role is required.")
            if not min_cgpa_str:
                raise ValueError("Minimum CGPA is required.")

            try:
                min_cgpa = float(min_cgpa_str)
            except ValueError:
                raise ValueError("Minimum CGPA must be a valid number.")

            try:
                pkg = float(pkg_str)
            except ValueError:
                raise ValueError("Package (LPA) must be a numeric value.")

            company = Company(
                company_id=cid,
                name=name,
                role=role,
                min_cgpa=min_cgpa,
                required_skills=skills,
                package_lpa=pkg
            )
            company.validate()

            self.dm.add_company(company)
            messagebox.showinfo("Success", f"Job opening at '{name}' for '{role}' added successfully!")
            self.clear_form()
            self.load_companies()

            if self.on_data_changed:
                self.on_data_changed()

        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register company: {e}")

    def check_students_for_selected_company(self):
        """Evaluate all students for the chosen company."""
        selected_text = self.combo_elig_comp.get()
        if not selected_text:
            messagebox.showwarning("Notice", "Please select a company first.")
            return

        cid = selected_text.split(" - ")[0].strip()
        company = self.dm.get_company_by_id(cid)
        if not company:
            messagebox.showerror("Error", f"Could not find company '{cid}'.")
            return

        self.tree_elig.heading("col1", text="Roll No")
        self.tree_elig.heading("col2", text="Student Name")
        self.tree_elig.heading("col3", text="Department")
        self.tree_elig.heading("col4", text="CGPA")

        for item in self.tree_elig.get_children():
            self.tree_elig.delete(item)

        results = self.dm.get_eligible_students_for_company(company)
        eligible_count = 0

        for r in results:
            is_elig = r["Eligible"] == "Yes"
            if is_elig:
                eligible_count += 1
            tag = "eligible" if is_elig else "ineligible"

            self.tree_elig.insert(
                "",
                "end",
                values=(
                    r["Roll No"],
                    r["Name"],
                    r["Department"],
                    f"{r['CGPA']:.2f}",
                    r["Eligible"],
                    r["Matched Skills"],
                    r["Reason"]
                ),
                tags=(tag,)
            )

        total = len(results)
        pct = (eligible_count / total * 100) if total > 0 else 0
        self.lbl_elig_summary.config(
            text=f"Company: {company.name} ({company.role}) | Min CGPA: {company.min_cgpa} | "
                 f"Eligible Candidates: {eligible_count} of {total} ({pct:.1f}%)"
        )

    def check_companies_for_selected_student(self):
        """Evaluate all companies for the chosen student."""
        selected_text = self.combo_elig_student.get()
        if not selected_text:
            messagebox.showwarning("Notice", "Please select a student first.")
            return

        roll_no = selected_text.split(" - ")[0].strip()
        student = self.dm.get_student_by_roll(roll_no)
        if not student:
            messagebox.showerror("Error", f"Could not find student '{roll_no}'.")
            return

        self.tree_elig.heading("col1", text="Company ID")
        self.tree_elig.heading("col2", text="Company Name")
        self.tree_elig.heading("col3", text="Job Role")
        self.tree_elig.heading("col4", text="Min CGPA")

        for item in self.tree_elig.get_children():
            self.tree_elig.delete(item)

        results = self.dm.get_eligible_companies_for_student(student)
        eligible_count = 0

        for r in results:
            is_elig = r["Eligible"] == "Yes"
            if is_elig:
                eligible_count += 1
            tag = "eligible" if is_elig else "ineligible"

            self.tree_elig.insert(
                "",
                "end",
                values=(
                    r["Company ID"],
                    r["Company Name"],
                    r["Role"],
                    f"{r['Min CGPA']:.2f}",
                    r["Eligible"],
                    r["Matched Skills"],
                    r["Status"]
                ),
                tags=(tag,)
            )

        total = len(results)
        self.lbl_elig_summary.config(
            text=f"Student: {student.name} ({student.roll_no}) | CGPA: {student.cgpa} | "
                 f"Qualifies for {eligible_count} out of {total} job openings."
        )
