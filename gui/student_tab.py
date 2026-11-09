"""
Module 1: Student Management GUI (Admin View)
Handles adding, viewing, searching, updating, and deleting student records.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

from models.student import Student
from storage.data_manager import DataManager
from gui.style import (
    CARD_BG, PAGE_BG, TEXT_PRIMARY, TEXT_MUTED,
    FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD,
    ACCENT_BLUE, ACCENT_GREEN, ACCENT_RED
)


class StudentTab(ttk.Frame):
    """Student Management Module Interface."""

    DEPARTMENTS = [
        "Computer Science",
        "Information Technology",
        "Data Science",
        "Electronics",
        "Electrical",
        "Mechanical",
        "Civil"
    ]

    def __init__(self, parent, data_manager: DataManager, on_data_changed=None):
        super().__init__(parent, style="Page.TFrame")
        self.dm = data_manager
        self.on_data_changed = on_data_changed

        self.selected_roll_no = None

        self._build_ui()
        self.load_students()

    def _build_ui(self):
        """Construct the student management interface."""
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        # Left Panel: Student Input Form
        left_card = tk.LabelFrame(
            self,
            text=" 📝 Student Details Form ",
            font=FONT_HEADING,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            padx=16,
            pady=16,
            relief="solid",
            bd=1
        )
        left_card.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)

        row = 0
        tk.Label(left_card, text="Roll Number *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=row, column=0, sticky="w", pady=(4, 2))
        self.entry_roll = ttk.Entry(left_card, font=FONT_BODY)
        self.entry_roll.grid(row=row+1, column=0, sticky="ew", pady=(0, 10))

        row += 2
        tk.Label(left_card, text="Full Name *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=row, column=0, sticky="w", pady=(4, 2))
        self.entry_name = ttk.Entry(left_card, font=FONT_BODY)
        self.entry_name.grid(row=row+1, column=0, sticky="ew", pady=(0, 10))

        row += 2
        tk.Label(left_card, text="Department *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=row, column=0, sticky="w", pady=(4, 2))
        self.combo_dept = ttk.Combobox(left_card, values=self.DEPARTMENTS, state="readonly", font=FONT_BODY)
        self.combo_dept.set(self.DEPARTMENTS[0])
        self.combo_dept.grid(row=row+1, column=0, sticky="ew", pady=(0, 10))

        row += 2
        tk.Label(left_card, text="CGPA (0.00 - 10.00) *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=row, column=0, sticky="w", pady=(4, 2))
        self.entry_cgpa = ttk.Entry(left_card, font=FONT_BODY)
        self.entry_cgpa.grid(row=row+1, column=0, sticky="ew", pady=(0, 10))

        row += 2
        tk.Label(left_card, text="Skills (comma separated) *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=row, column=0, sticky="w", pady=(4, 2))
        self.entry_skills = ttk.Entry(left_card, font=FONT_BODY)
        self.entry_skills.grid(row=row+1, column=0, sticky="ew", pady=(0, 6))

        tk.Label(
            left_card,
            text="e.g. Python, SQL, Machine Learning",
            font=("Segoe UI", 8, "italic"),
            bg=CARD_BG,
            fg=TEXT_MUTED
        ).grid(row=row+2, column=0, sticky="w", pady=(0, 16))

        left_card.columnconfigure(0, weight=1)

        btn_frame = tk.Frame(left_card, bg=CARD_BG)
        btn_frame.grid(row=row+3, column=0, sticky="ew", pady=(10, 0))
        btn_frame.columnconfigure((0, 1), weight=1)

        self.btn_add = tk.Button(
            btn_frame,
            text="➕ Add Student",
            font=FONT_BODY_BOLD,
            bg=ACCENT_GREEN,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.add_student
        )
        self.btn_add.grid(row=0, column=0, sticky="ew", padx=(0, 4), pady=4)

        self.btn_update = tk.Button(
            btn_frame,
            text="✏️ Update",
            font=FONT_BODY_BOLD,
            bg=ACCENT_BLUE,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.update_student
        )
        self.btn_update.grid(row=0, column=1, sticky="ew", padx=(4, 0), pady=4)

        self.btn_delete = tk.Button(
            btn_frame,
            text="🗑️ Delete",
            font=FONT_BODY_BOLD,
            bg=ACCENT_RED,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.delete_student
        )
        self.btn_delete.grid(row=1, column=0, sticky="ew", padx=(0, 4), pady=4)

        self.btn_clear = tk.Button(
            btn_frame,
            text="🔄 Clear Form",
            font=FONT_BODY,
            bg="#E2E8F0",
            fg=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.clear_form
        )
        self.btn_clear.grid(row=1, column=1, sticky="ew", padx=(4, 0), pady=4)

        tk.Label(
            left_card,
            text="💡 Tip: Double-click a student in the table\nto load details for editing.",
            font=("Segoe UI", 8),
            bg="#F1F5F9",
            fg=TEXT_MUTED,
            padx=8,
            pady=6,
            relief="flat"
        ).grid(row=row+4, column=0, sticky="ew", pady=(18, 0))

        # Right Panel: Search Bar and Student Table
        right_card = tk.LabelFrame(
            self,
            text=" 🎓 Student Records Database ",
            font=FONT_HEADING,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            padx=14,
            pady=14,
            relief="solid",
            bd=1
        )
        right_card.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        right_card.rowconfigure(1, weight=1)
        right_card.columnconfigure(0, weight=1)

        search_frame = tk.Frame(right_card, bg=CARD_BG)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        tk.Label(search_frame, text="Search:", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 6))

        self.entry_search = ttk.Entry(search_frame, font=FONT_BODY, width=22)
        self.entry_search.pack(side="left", padx=(0, 10))
        self.entry_search.bind("<Return>", lambda event: self.search_students())

        tk.Label(search_frame, text="Dept:", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 6))

        self.combo_filter_dept = ttk.Combobox(search_frame, values=["All"] + self.DEPARTMENTS, state="readonly", width=16)
        self.combo_filter_dept.set("All")
        self.combo_filter_dept.pack(side="left", padx=(0, 10))
        self.combo_filter_dept.bind("<<ComboboxSelected>>", lambda event: self.search_students())

        btn_search = tk.Button(
            search_frame,
            text="🔍 Filter",
            font=FONT_BODY,
            bg=ACCENT_BLUE,
            fg="#FFFFFF",
            relief="flat",
            padx=8,
            pady=2,
            cursor="hand2",
            command=self.search_students
        )
        btn_search.pack(side="left", padx=(0, 6))

        btn_reset = tk.Button(
            search_frame,
            text="↺ Reset",
            font=FONT_BODY,
            bg="#E2E8F0",
            fg=TEXT_PRIMARY,
            relief="flat",
            padx=8,
            pady=2,
            cursor="hand2",
            command=self.reset_search
        )
        btn_reset.pack(side="left")

        table_frame = tk.Frame(right_card, bg=CARD_BG)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ("roll_no", "name", "dept", "cgpa", "skills")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("roll_no", text="Roll No")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("dept", text="Department")
        self.tree.heading("cgpa", text="CGPA")
        self.tree.heading("skills", text="Skills")

        self.tree.column("roll_no", width=85, anchor="center")
        self.tree.column("name", width=140, anchor="w")
        self.tree.column("dept", width=140, anchor="w")
        self.tree.column("cgpa", width=65, anchor="center")
        self.tree.column("skills", width=220, anchor="w")

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.tree.bind("<Double-1>", self.on_row_double_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.lbl_record_count = tk.Label(
            right_card,
            text="Showing 0 students",
            font=FONT_BODY,
            bg=CARD_BG,
            fg=TEXT_MUTED
        )
        self.lbl_record_count.grid(row=2, column=0, sticky="w", pady=(8, 0))

    def load_students(self, df: pd.DataFrame = None):
        """Populate the Treeview table with student data."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        if df is None:
            df = self.dm.get_all_students_df()

        if not df.empty:
            for _, row in df.iterrows():
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row.get("Roll No", ""),
                        row.get("Name", ""),
                        row.get("Department", ""),
                        f"{float(row.get('CGPA', 0.0)):.2f}",
                        row.get("Skills", "")
                    )
                )

        total_all = len(self.dm.get_all_students_df())
        current_count = len(df)
        self.lbl_record_count.config(
            text=f"Showing: {current_count} of {total_all} student records"
        )

    def search_students(self):
        """Filter table based on search query and department dropdown."""
        query = self.entry_search.get().strip()
        dept = self.combo_filter_dept.get()
        filtered_df = self.dm.search_students(query=query, department=dept)
        self.load_students(filtered_df)

    def reset_search(self):
        """Clear search filters and show all records."""
        self.entry_search.delete(0, tk.END)
        self.combo_filter_dept.set("All")
        self.load_students()

    def on_row_select(self, event):
        """Save selected roll number when a row is clicked."""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            if values:
                self.selected_roll_no = values[0]

    def on_row_double_click(self, event):
        """Load double-clicked student data into the form for editing."""
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        if not values:
            return

        roll_no, name, dept, cgpa, skills = values
        self.selected_roll_no = roll_no

        self.entry_roll.delete(0, tk.END)
        self.entry_roll.insert(0, roll_no)

        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, name)

        if dept in self.DEPARTMENTS:
            self.combo_dept.set(dept)

        self.entry_cgpa.delete(0, tk.END)
        self.entry_cgpa.insert(0, cgpa)

        self.entry_skills.delete(0, tk.END)
        self.entry_skills.insert(0, skills)

    def clear_form(self):
        """Reset form fields and clear selection."""
        self.selected_roll_no = None
        self.entry_roll.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.combo_dept.set(self.DEPARTMENTS[0])
        self.entry_cgpa.delete(0, tk.END)
        self.entry_skills.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def _get_form_student(self) -> Student:
        """Construct and validate a Student object from form fields."""
        roll = self.entry_roll.get().strip()
        name = self.entry_name.get().strip()
        dept = self.combo_dept.get().strip()
        cgpa_str = self.entry_cgpa.get().strip()
        skills = self.entry_skills.get().strip()

        if not roll:
            raise ValueError("Roll Number is required.")
        if not name:
            raise ValueError("Student Name is required.")
        if not dept:
            raise ValueError("Department is required.")
        if not cgpa_str:
            raise ValueError("CGPA is required.")

        try:
            cgpa = float(cgpa_str)
        except ValueError:
            raise ValueError("CGPA must be a valid number (e.g. 8.50).")

        if not (0.0 <= cgpa <= 10.0):
            raise ValueError(f"CGPA must be between 0.00 and 10.00 (entered: {cgpa}).")

        if not skills:
            raise ValueError("At least one skill is required.")

        student = Student(roll_no=roll, name=name, department=dept, cgpa=cgpa, skills=skills)
        student.validate()
        return student

    def add_student(self):
        """Add a new student record with error handling."""
        try:
            student = self._get_form_student()
            self.dm.add_student(student)
            messagebox.showinfo("Success", f"Student '{student.name}' ({student.roll_no}) added successfully!")
            self.clear_form()
            self.load_students()
            if self.on_data_changed:
                self.on_data_changed()
        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {e}")

    def update_student(self):
        """Update an existing student's record."""
        target_roll = self.selected_roll_no
        if not target_roll:
            target_roll = self.entry_roll.get().strip()
            if not target_roll:
                messagebox.showwarning("Selection Required", "Please select a student from the table or enter Roll Number to update.")
                return

        try:
            student = self._get_form_student()
            self.dm.update_student(target_roll, student)
            messagebox.showinfo("Success", f"Student '{student.roll_no}' updated successfully!")
            self.clear_form()
            self.load_students()
            if self.on_data_changed:
                self.on_data_changed()
        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {e}")

    def delete_student(self):
        """Delete selected student record after confirmation."""
        roll = self.selected_roll_no
        if not roll:
            roll = self.entry_roll.get().strip()
            if not roll:
                messagebox.showwarning("Selection Required", "Please select a student from the table to delete.")
                return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete student with Roll Number '{roll}'?\n\nThis will also remove their job applications and login account.",
            icon="warning"
        )
        if not confirm:
            return

        try:
            self.dm.delete_student(roll)
            messagebox.showinfo("Deleted", f"Student '{roll}' has been removed.")
            self.clear_form()
            self.load_students()
            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {e}")
