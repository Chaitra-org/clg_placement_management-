"""
Login & Registration GUI
Provides dedicated login pages for Admin and Student,
plus self-registration for new students.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from models.user import User
from storage.data_manager import DataManager
from gui.style import (
    CARD_BG, PAGE_BG, HEADER_BG, TEXT_PRIMARY, TEXT_MUTED,
    FONT_TITLE, FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD,
    ACCENT_BLUE, ACCENT_GREEN, ACCENT_PURPLE, ACCENT_RED
)


class LoginView(ttk.Frame):
    """Integrated Login and Registration View."""

    DEPARTMENTS = [
        "Computer Science",
        "Information Technology",
        "Data Science",
        "Electronics",
        "Electrical",
        "Mechanical",
        "Civil"
    ]

    def __init__(self, parent, data_manager: DataManager, on_login_success=None):
        super().__init__(parent, style="Page.TFrame")
        self.dm = data_manager
        self.on_login_success = on_login_success

        self._build_ui()

    def _build_ui(self):
        """Construct the login page layout."""
        # Center container
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = tk.Frame(self, bg=PAGE_BG)
        container.grid(row=0, column=0)

        # Login Card
        card = tk.LabelFrame(
            container,
            text="",
            bg=CARD_BG,
            relief="solid",
            bd=1,
            padx=28,
            pady=24
        )
        card.pack(pady=20)

        # Portal Title
        tk.Label(
            card,
            text="🎓 Campus Placement Portal",
            font=FONT_TITLE,
            fg=HEADER_BG,
            bg=CARD_BG
        ).pack(pady=(0, 2))

        tk.Label(
            card,
            text="Sign in to your account or register as a new student",
            font=FONT_SUBHEADING,
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(pady=(0, 16))

        # Tab bar for: Admin Login | Student Login | Student Registration
        self.notebook = ttk.Notebook(card)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: Admin Login
        admin_tab = tk.Frame(self.notebook, bg=CARD_BG, padx=16, pady=16)
        self.notebook.add(admin_tab, text="  👨‍💼 Admin Login  ")
        self._build_admin_login(admin_tab)

        # Tab 2: Student Login
        student_tab = tk.Frame(self.notebook, bg=CARD_BG, padx=16, pady=16)
        self.notebook.add(student_tab, text="  🎓 Student Login  ")
        self._build_student_login(student_tab)

        # Tab 3: Student Registration
        register_tab = tk.Frame(self.notebook, bg=CARD_BG, padx=16, pady=16)
        self.notebook.add(register_tab, text="  📝 Student Registration  ")
        self._build_student_register(register_tab)

        # Bottom Quick Credential Hint Box
        hint_box = tk.Frame(card, bg="#F1F5F9", padx=12, pady=8, relief="flat")
        hint_box.pack(fill="x", pady=(18, 0))

        tk.Label(
            hint_box,
            text="💡 Quick Test Credentials:",
            font=FONT_BODY_BOLD,
            fg=TEXT_PRIMARY,
            bg="#F1F5F9"
        ).pack(anchor="w")

        tk.Label(
            hint_box,
            text="• Admin: username 'admin' | password 'admin123'\n• Student: Roll No 'CS101' | password 'student123'",
            font=("Segoe UI", 8),
            fg=TEXT_MUTED,
            bg="#F1F5F9",
            justify="left"
        ).pack(anchor="w", pady=(2, 0))

    # ----------------------------------------------------
    # Sub-View 1: Admin Login
    # ----------------------------------------------------
    def _build_admin_login(self, parent):
        tk.Label(parent, text="Administrator Username", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).pack(anchor="w", pady=(4, 2))
        self.entry_admin_user = ttk.Entry(parent, font=FONT_BODY, width=34)
        self.entry_admin_user.pack(fill="x", pady=(0, 12))
        self.entry_admin_user.insert(0, "admin")

        tk.Label(parent, text="Password", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).pack(anchor="w", pady=(4, 2))
        self.entry_admin_pass = ttk.Entry(parent, font=FONT_BODY, show="•", width=34)
        self.entry_admin_pass.pack(fill="x", pady=(0, 16))
        self.entry_admin_pass.insert(0, "admin123")
        self.entry_admin_pass.bind("<Return>", lambda e: self.handle_admin_login())

        btn_admin_login = tk.Button(
            parent,
            text="🔐 Login as Admin",
            font=FONT_BODY_BOLD,
            bg=ACCENT_BLUE,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=7,
            command=self.handle_admin_login
        )
        btn_admin_login.pack(fill="x", pady=(4, 6))

    # ----------------------------------------------------
    # Sub-View 2: Student Login
    # ----------------------------------------------------
    def _build_student_login(self, parent):
        tk.Label(parent, text="Student Roll Number", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).pack(anchor="w", pady=(4, 2))
        self.entry_student_user = ttk.Entry(parent, font=FONT_BODY, width=34)
        self.entry_student_user.pack(fill="x", pady=(0, 12))
        self.entry_student_user.insert(0, "CS101")

        tk.Label(parent, text="Password", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).pack(anchor="w", pady=(4, 2))
        self.entry_student_pass = ttk.Entry(parent, font=FONT_BODY, show="•", width=34)
        self.entry_student_pass.pack(fill="x", pady=(0, 16))
        self.entry_student_pass.insert(0, "student123")
        self.entry_student_pass.bind("<Return>", lambda e: self.handle_student_login())

        btn_student_login = tk.Button(
            parent,
            text="🎓 Login as Student",
            font=FONT_BODY_BOLD,
            bg=ACCENT_GREEN,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=7,
            command=self.handle_student_login
        )
        btn_student_login.pack(fill="x", pady=(4, 6))

    # ----------------------------------------------------
    # Sub-View 3: Student Registration
    # ----------------------------------------------------
    def _build_student_register(self, parent):
        grid_frame = tk.Frame(parent, bg=CARD_BG)
        grid_frame.pack(fill="x")
        grid_frame.columnconfigure((0, 1), weight=1)

        # Roll Number & Full Name
        tk.Label(grid_frame, text="Roll Number *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=(0, 6), pady=(2, 2))
        tk.Label(grid_frame, text="Full Name *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=0, column=1, sticky="w", padx=(6, 0), pady=(2, 2))

        self.reg_roll = ttk.Entry(grid_frame, font=FONT_BODY)
        self.reg_roll.grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(0, 8))

        self.reg_name = ttk.Entry(grid_frame, font=FONT_BODY)
        self.reg_name.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(0, 8))

        # Department & CGPA
        tk.Label(grid_frame, text="Department *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=2, column=0, sticky="w", padx=(0, 6), pady=(2, 2))
        tk.Label(grid_frame, text="CGPA (0.00 - 10.00) *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=2, column=1, sticky="w", padx=(6, 0), pady=(2, 2))

        self.reg_dept = ttk.Combobox(grid_frame, values=self.DEPARTMENTS, state="readonly", font=FONT_BODY)
        self.reg_dept.set(self.DEPARTMENTS[0])
        self.reg_dept.grid(row=3, column=0, sticky="ew", padx=(0, 6), pady=(0, 8))

        self.reg_cgpa = ttk.Entry(grid_frame, font=FONT_BODY)
        self.reg_cgpa.grid(row=3, column=1, sticky="ew", padx=(6, 0), pady=(0, 8))

        # Skills
        tk.Label(grid_frame, text="Technical Skills (comma separated) *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=4, column=0, columnspan=2, sticky="w", pady=(2, 2))
        self.reg_skills = ttk.Entry(grid_frame, font=FONT_BODY)
        self.reg_skills.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 8))

        # Password & Confirm Password
        tk.Label(grid_frame, text="Password *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=6, column=0, sticky="w", padx=(0, 6), pady=(2, 2))
        tk.Label(grid_frame, text="Confirm Password *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=6, column=1, sticky="w", padx=(6, 0), pady=(2, 2))

        self.reg_pass = ttk.Entry(grid_frame, font=FONT_BODY, show="•")
        self.reg_pass.grid(row=7, column=0, sticky="ew", padx=(0, 6), pady=(0, 14))

        self.reg_confirm = ttk.Entry(grid_frame, font=FONT_BODY, show="•")
        self.reg_confirm.grid(row=7, column=1, sticky="ew", padx=(6, 0), pady=(0, 14))

        btn_register = tk.Button(
            parent,
            text="📝 Register & Create Account",
            font=FONT_BODY_BOLD,
            bg=ACCENT_PURPLE,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=7,
            command=self.handle_student_register
        )
        btn_register.pack(fill="x", pady=(2, 4))

    # ----------------------------------------------------
    # Authentication Handlers
    # ----------------------------------------------------
    def handle_admin_login(self):
        """Authenticate Admin user."""
        username = self.entry_admin_user.get().strip()
        password = self.entry_admin_pass.get().strip()

        try:
            user = self.dm.authenticate(username, password, expected_role=User.ROLE_ADMIN)
            if self.on_login_success:
                self.on_login_success(user)
        except ValueError as ve:
            messagebox.showerror("Login Failed", str(ve))
        except Exception as e:
            messagebox.showerror("System Error", f"Unexpected error during login: {e}")

    def handle_student_login(self):
        """Authenticate Student user."""
        roll = self.entry_student_user.get().strip()
        password = self.entry_student_pass.get().strip()

        try:
            user = self.dm.authenticate(roll, password, expected_role=User.ROLE_STUDENT)
            if self.on_login_success:
                self.on_login_success(user)
        except ValueError as ve:
            messagebox.showerror("Login Failed", str(ve))
        except Exception as e:
            messagebox.showerror("System Error", f"Unexpected error during login: {e}")

    def handle_student_register(self):
        """Handle new student registration."""
        roll = self.reg_roll.get().strip()
        name = self.reg_name.get().strip()
        dept = self.reg_dept.get().strip()
        cgpa_str = self.reg_cgpa.get().strip()
        skills = self.reg_skills.get().strip()
        password = self.reg_pass.get().strip()
        confirm = self.reg_confirm.get().strip()

        try:
            if not roll:
                raise ValueError("Roll Number is required.")
            if not name:
                raise ValueError("Full Name is required.")
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
                raise ValueError("Please provide at least one technical skill.")

            if len(password) < 4:
                raise ValueError("Password must be at least 4 characters long.")

            if password != confirm:
                raise ValueError("Passwords do not match. Please re-enter.")

            student, user = self.dm.register_student_account(
                roll_no=roll,
                name=name,
                dept=dept,
                cgpa=cgpa,
                skills=skills,
                password=password
            )

            messagebox.showinfo(
                "Registration Successful! 🎉",
                f"Welcome, {student.name}!\nYour account has been registered successfully.\n\nYou can now log in with Roll Number '{student.roll_no}'."
            )

            # Pre-fill student login and switch to Student Login tab
            self.entry_student_user.delete(0, tk.END)
            self.entry_student_user.insert(0, student.roll_no)
            self.entry_student_pass.delete(0, tk.END)
            self.entry_student_pass.insert(0, password)
            self.notebook.select(1)

        except ValueError as ve:
            messagebox.showerror("Registration Error", str(ve))
        except Exception as e:
            messagebox.showerror("System Error", f"Failed to register student: {e}")
