"""
College Placement Management System
Main Application Entry Point with Authentication & Role-Based Views

Technologies used:
- Core Python & File Handling (CSV persistent storage)
- Object-Oriented Programming (OOP)
- Pandas (Data querying, aggregation & DataFrames)
- NumPy (Numerical computations & statistical calculations)
- Matplotlib (Interactive graphical charts)
- Tkinter & ttk (Modern Desktop GUI)
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from models.user import User
from storage.data_manager import DataManager
from gui.style import (
    apply_theme, HEADER_BG, HEADER_FG, PAGE_BG,
    TEXT_PRIMARY, TEXT_MUTED, FONT_TITLE, FONT_SUBTITLE, FONT_BODY, FONT_BODY_BOLD,
    ACCENT_RED
)
from gui.login_window import LoginView
from gui.student_tab import StudentTab
from gui.company_tab import CompanyTab
from gui.placement_tab import PlacementTab
from gui.student_portal import StudentPortal


class PlacementApp:
    """Main Application Controller managing Authentication and Role Dashboards."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("College Placement Management System")
        self.root.geometry("1180x760")
        self.root.minsize(1020, 680)
        self.root.configure(bg=PAGE_BG)

        self._center_window(1180, 760)

        data_path = os.path.join(BASE_DIR, "data")
        self.data_manager = DataManager(data_dir=data_path)

        self.current_user: User = None

        apply_theme(self.root)
        self._build_header()

        self.view_container = tk.Frame(self.root, bg=PAGE_BG)
        self.view_container.pack(side="top", fill="both", expand=True)

        self._build_status_bar()
        self.show_login_view()

    def _center_window(self, width: int, height: int):
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = max(0, (screen_width // 2) - (width // 2))
        y = max(0, (screen_height // 2) - (height // 2) - 20)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _build_header(self):
        self.header_frame = tk.Frame(self.root, bg=HEADER_BG, padx=20, pady=10)
        self.header_frame.pack(side="top", fill="x")

        title_box = tk.Frame(self.header_frame, bg=HEADER_BG)
        title_box.pack(side="left")

        lbl_title = tk.Label(
            title_box,
            text="🎓 College Placement Management System",
            font=FONT_TITLE,
            bg=HEADER_BG,
            fg=HEADER_FG
        )
        lbl_title.pack(anchor="w")

        self.lbl_subtitle = tk.Label(
            title_box,
            text="Desktop Suite: Student Records • Company Eligibility • Applications • Placement Analytics",
            font=FONT_SUBTITLE,
            bg=HEADER_BG,
            fg="#93C5FD"
        )
        self.lbl_subtitle.pack(anchor="w", pady=(2, 0))

        self.user_control_box = tk.Frame(self.header_frame, bg=HEADER_BG)
        self.user_control_box.pack(side="right", anchor="e")

        self.lbl_user_badge = tk.Label(
            self.user_control_box,
            text="",
            font=("Segoe UI", 9, "bold"),
            bg="#1E40AF",
            fg="#FFFFFF",
            padx=10,
            pady=4
        )

        self.btn_logout = tk.Button(
            self.user_control_box,
            text="🚪 Logout",
            font=FONT_BODY_BOLD,
            bg=ACCENT_RED,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=3,
            command=self.logout
        )

    def _build_status_bar(self):
        status_bar = tk.Frame(self.root, bg="#E2E8F0", padx=14, pady=4)
        status_bar.pack(side="bottom", fill="x")

        self.lbl_status = tk.Label(
            status_bar,
            text="🟢 System Ready | Persistent Storage: data/*.csv",
            font=("Segoe UI", 8),
            bg="#E2E8F0",
            fg=TEXT_PRIMARY
        )
        self.lbl_status.pack(side="left")

        current_date = datetime.now().strftime("%B %d, %Y")
        lbl_date = tk.Label(
            status_bar,
            text=f"Session: {current_date} | v1.0.0",
            font=("Segoe UI", 8),
            bg="#E2E8F0",
            fg=TEXT_MUTED
        )
        lbl_date.pack(side="right")

    def _clear_view_container(self):
        for widget in self.view_container.winfo_children():
            widget.destroy()

    def show_login_view(self):
        self._clear_view_container()
        self.current_user = None

        self.lbl_user_badge.pack_forget()
        self.btn_logout.pack_forget()

        self.lbl_subtitle.config(text="Please sign in to continue or register for a student account.")
        self.lbl_status.config(text="🔒 Authentication Required | Please log in.")

        login_view = LoginView(
            self.view_container,
            data_manager=self.data_manager,
            on_login_success=self.on_login_success
        )
        login_view.pack(fill="both", expand=True)

    def on_login_success(self, user: User):
        self.current_user = user

        if user.is_admin():
            badge_text = "👨‍💼 Administrator (admin)"
        else:
            student = self.data_manager.get_student_by_roll(user.roll_no)
            st_name = student.name if student else user.username.upper()
            badge_text = f"🎓 Student: {st_name} ({user.roll_no})"

        self.lbl_user_badge.config(text=badge_text)
        self.lbl_user_badge.pack(side="left", padx=(0, 10))
        self.btn_logout.pack(side="left")

        if user.is_admin():
            self.show_admin_dashboard()
        else:
            self.show_student_portal()

    def show_admin_dashboard(self):
        self._clear_view_container()
        self.lbl_subtitle.config(text="Administrator Control Panel • Student Records • Companies • Placement Analytics")

        self.notebook = ttk.Notebook(self.view_container)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(8, 4))

        self.tab_students = StudentTab(
            self.notebook,
            data_manager=self.data_manager,
            on_data_changed=self.on_global_data_changed
        )
        self.notebook.add(self.tab_students, text="  🎓 Student Management  ")

        self.tab_companies = CompanyTab(
            self.notebook,
            data_manager=self.data_manager,
            on_data_changed=self.on_global_data_changed
        )
        self.notebook.add(self.tab_companies, text="  🏢 Company & Eligibility  ")

        self.tab_placement = PlacementTab(
            self.notebook,
            data_manager=self.data_manager,
            on_data_changed=self.on_global_data_changed
        )
        self.notebook.add(self.tab_placement, text="  📊 Applications & Placement  ")

        self.notebook.bind("<<NotebookTabChanged>>", self.on_admin_tab_switched)
        self.lbl_status.config(text=f"🟢 Admin Session Active | User: {self.current_user.username}")

    def show_student_portal(self):
        self._clear_view_container()
        self.lbl_subtitle.config(text="Student Career Portal • Explore Job Vacancies • Track Application Status")

        portal = StudentPortal(
            self.view_container,
            user=self.current_user,
            data_manager=self.data_manager,
            on_logout=self.logout
        )
        portal.pack(fill="both", expand=True)
        self.lbl_status.config(text=f"🟢 Student Session Active | Roll No: {self.current_user.roll_no}")

    def logout(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?", icon="question")
        if confirm:
            self.show_login_view()

    def on_global_data_changed(self):
        try:
            if hasattr(self, "tab_companies"):
                self.tab_companies.load_companies()
                self.tab_companies.refresh_student_dropdown()
            if hasattr(self, "tab_placement"):
                self.tab_placement.refresh_all()

            st_count = len(self.data_manager.get_all_students_df())
            comp_count = len(self.data_manager.get_all_companies_df())
            app_count = len(self.data_manager.get_all_applications_df())
            self.lbl_status.config(
                text=f"🟢 Data Synced | Students: {st_count} | Companies: {comp_count} | Applications: {app_count}"
            )
        except Exception as e:
            print(f"Sync error: {e}")

    def on_admin_tab_switched(self, event):
        current_tab_index = self.notebook.index("current")
        if current_tab_index == 1:
            self.tab_companies.refresh_student_dropdown()
        elif current_tab_index == 2:
            self.tab_placement.refresh_all()


def main():
    try:
        root = tk.Tk()
        app = PlacementApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Fatal error while launching application: {e}")
        messagebox.showerror("System Error", f"Failed to start College Placement System:\n{e}")


if __name__ == "__main__":
    main()
