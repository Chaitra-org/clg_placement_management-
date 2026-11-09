"""
Module 3: Applications & Placement GUI (Admin View)
Handles applying students to companies, tracking application statuses,
and presenting statistical placement analytics and Matplotlib charts.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from storage.data_manager import DataManager
from models.application import Application
from gui.style import (
    CARD_BG, PAGE_BG, TEXT_PRIMARY, TEXT_MUTED,
    FONT_HEADING, FONT_SUBHEADING, FONT_BODY, FONT_BODY_BOLD,
    ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMBER, ACCENT_RED, ACCENT_PURPLE
)


class PlacementTab(ttk.Frame):
    """Applications & Placement Analytics Interface."""

    def __init__(self, parent, data_manager: DataManager, on_data_changed=None):
        super().__init__(parent, style="Page.TFrame")
        self.dm = data_manager
        self.on_data_changed = on_data_changed

        self.selected_app_id = None
        self.canvas = None

        self._build_ui()
        self.refresh_all()

    def _build_ui(self):
        """Construct the Applications and Placement Analytics UI."""
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)

        left_container = tk.Frame(self, bg=PAGE_BG)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=12)
        left_container.columnconfigure(0, weight=1)
        left_container.rowconfigure(1, weight=1)

        apply_card = tk.LabelFrame(
            left_container,
            text=" 📝 Apply Student for Job Opening ",
            font=FONT_HEADING,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            padx=14,
            pady=12,
            relief="solid",
            bd=1
        )
        apply_card.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        apply_card.columnconfigure((0, 1), weight=1)

        tk.Label(apply_card, text="Select Student *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=(0, 6))
        tk.Label(apply_card, text="Select Company & Role *", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).grid(row=0, column=1, sticky="w", padx=(6, 0))

        self.combo_student = ttk.Combobox(apply_card, state="readonly", font=FONT_BODY)
        self.combo_student.grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=(2, 8))

        self.combo_company = ttk.Combobox(apply_card, state="readonly", font=FONT_BODY)
        self.combo_company.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(2, 8))

        btn_apply = tk.Button(
            apply_card,
            text="🚀 Submit Application",
            font=FONT_BODY_BOLD,
            bg=ACCENT_BLUE,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5,
            command=self.submit_application
        )
        btn_apply.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(4, 2))

        apps_card = tk.LabelFrame(
            left_container,
            text=" 📋 Job Applications Tracker ",
            font=FONT_HEADING,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            padx=12,
            pady=12,
            relief="solid",
            bd=1
        )
        apps_card.grid(row=1, column=0, sticky="nsew")
        apps_card.columnconfigure(0, weight=1)
        apps_card.rowconfigure(1, weight=1)

        filter_bar = tk.Frame(apps_card, bg=CARD_BG)
        filter_bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        tk.Label(filter_bar, text="Filter Status:", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 6))
        self.combo_status_filter = ttk.Combobox(
            filter_bar,
            values=["All", "Applied", "Shortlisted", "Selected", "Rejected"],
            state="readonly",
            width=14
        )
        self.combo_status_filter.set("All")
        self.combo_status_filter.pack(side="left", padx=(0, 10))
        self.combo_status_filter.bind("<<ComboboxSelected>>", lambda e: self.load_applications())

        btn_refresh_apps = tk.Button(
            filter_bar,
            text="↺ Refresh",
            font=FONT_BODY,
            bg="#E2E8F0",
            fg=TEXT_PRIMARY,
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=2,
            command=self.load_applications
        )
        btn_refresh_apps.pack(side="left")

        app_table_frame = tk.Frame(apps_card, bg=CARD_BG)
        app_table_frame.grid(row=1, column=0, sticky="nsew")
        app_table_frame.columnconfigure(0, weight=1)
        app_table_frame.rowconfigure(0, weight=1)

        cols = ("appid", "roll", "name", "company", "role", "status", "date")
        self.tree_apps = ttk.Treeview(app_table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_apps.heading("appid", text="App ID")
        self.tree_apps.heading("roll", text="Roll No")
        self.tree_apps.heading("name", text="Student")
        self.tree_apps.heading("company", text="Company")
        self.tree_apps.heading("role", text="Role")
        self.tree_apps.heading("status", text="Status")
        self.tree_apps.heading("date", text="Date")

        self.tree_apps.column("appid", width=75, anchor="center")
        self.tree_apps.column("roll", width=65, anchor="center")
        self.tree_apps.column("name", width=110, anchor="w")
        self.tree_apps.column("company", width=105, anchor="w")
        self.tree_apps.column("role", width=120, anchor="w")
        self.tree_apps.column("status", width=85, anchor="center")
        self.tree_apps.column("date", width=80, anchor="center")

        self.tree_apps.tag_configure("Selected", foreground=ACCENT_GREEN, background="#ECFDF5")
        self.tree_apps.tag_configure("Shortlisted", foreground=ACCENT_AMBER, background="#FFFBEB")
        self.tree_apps.tag_configure("Rejected", foreground=ACCENT_RED, background="#FEF2F2")
        self.tree_apps.tag_configure("Applied", foreground=ACCENT_BLUE, background="#EFF6FF")

        scroll_app_y = ttk.Scrollbar(app_table_frame, orient="vertical", command=self.tree_apps.yview)
        scroll_app_x = ttk.Scrollbar(app_table_frame, orient="horizontal", command=self.tree_apps.xview)
        self.tree_apps.configure(yscrollcommand=scroll_app_y.set, xscrollcommand=scroll_app_x.set)

        self.tree_apps.grid(row=0, column=0, sticky="nsew")
        scroll_app_y.grid(row=0, column=1, sticky="ns")
        scroll_app_x.grid(row=1, column=0, sticky="ew")

        self.tree_apps.bind("<<TreeviewSelect>>", self.on_app_selected)

        status_update_frame = tk.Frame(apps_card, bg="#F1F5F9", padx=10, pady=8, relief="flat")
        status_update_frame.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        tk.Label(status_update_frame, text="Update Status for Selected:", font=FONT_BODY_BOLD, bg="#F1F5F9", fg=TEXT_PRIMARY).pack(side="left", padx=(0, 6))

        self.combo_new_status = ttk.Combobox(
            status_update_frame,
            values=["Applied", "Shortlisted", "Selected", "Rejected"],
            state="readonly",
            width=12
        )
        self.combo_new_status.set("Selected")
        self.combo_new_status.pack(side="left", padx=(0, 8))

        btn_update_status = tk.Button(
            status_update_frame,
            text="✔ Update Status",
            font=FONT_BODY_BOLD,
            bg=ACCENT_GREEN,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=3,
            command=self.update_application_status
        )
        btn_update_status.pack(side="left", padx=(0, 6))

        btn_delete_app = tk.Button(
            status_update_frame,
            text="🗑 Remove",
            font=FONT_BODY,
            bg=ACCENT_RED,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=3,
            command=self.delete_application
        )
        btn_delete_app.pack(side="left")

        right_card = tk.LabelFrame(
            self,
            text=" 📊 Placement Analytics & Visualizations ",
            font=FONT_HEADING,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            padx=14,
            pady=12,
            relief="solid",
            bd=1
        )
        right_card.grid(row=0, column=1, sticky="nsew", padx=(6, 12), pady=12)
        right_card.columnconfigure(0, weight=1)
        right_card.rowconfigure(2, weight=1)

        kpi_frame = tk.Frame(right_card, bg=CARD_BG)
        kpi_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        kpi_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.kpi_total = self._create_kpi_box(kpi_frame, 0, "Total Students", "0", ACCENT_BLUE)
        self.kpi_placed = self._create_kpi_box(kpi_frame, 1, "Placed Students", "0", ACCENT_GREEN)
        self.kpi_rate = self._create_kpi_box(kpi_frame, 2, "Placement Rate", "0%", ACCENT_PURPLE)
        self.kpi_cgpa = self._create_kpi_box(kpi_frame, 3, "Avg CGPA (Placed)", "0.0", ACCENT_AMBER)

        chart_ctrl = tk.Frame(right_card, bg=CARD_BG)
        chart_ctrl.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        tk.Label(chart_ctrl, text="Select Chart View:", font=FONT_BODY_BOLD, bg=CARD_BG, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 6))

        self.CHART_OPTIONS = [
            "Application Status Distribution (Donut)",
            "Department-wise Placement (Bar)",
            "Student CGPA Distribution (NumPy Stats)",
            "Top Hiring Companies (Bar)"
        ]
        self.combo_chart = ttk.Combobox(
            chart_ctrl,
            values=self.CHART_OPTIONS,
            state="readonly",
            width=36,
            font=FONT_BODY
        )
        self.combo_chart.set(self.CHART_OPTIONS[0])
        self.combo_chart.pack(side="left", padx=(0, 8))
        self.combo_chart.bind("<<ComboboxSelected>>", lambda e: self.render_chart())

        btn_render = tk.Button(
            chart_ctrl,
            text="📊 Plot",
            font=FONT_BODY_BOLD,
            bg=ACCENT_BLUE,
            fg="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=2,
            command=self.render_chart
        )
        btn_render.pack(side="left")

        self.chart_container = tk.Frame(right_card, bg="#FFFFFF", relief="solid", bd=1)
        self.chart_container.grid(row=2, column=0, sticky="nsew")
        self.chart_container.columnconfigure(0, weight=1)
        self.chart_container.rowconfigure(0, weight=1)

    def _create_kpi_box(self, parent, col, title, initial_val, color):
        box = tk.Frame(parent, bg="#F8FAFC", relief="solid", bd=1, padx=6, pady=8)
        box.grid(row=0, column=col, sticky="ew", padx=3)

        lbl_val = tk.Label(box, text=initial_val, font=(FONT_HEADING[0], 14, "bold"), fg=color, bg="#F8FAFC")
        lbl_val.pack()

        lbl_title = tk.Label(box, text=title, font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#F8FAFC")
        lbl_title.pack()

        return lbl_val

    def refresh_all(self):
        self.refresh_dropdowns()
        self.load_applications()
        self.refresh_statistics()

    def refresh_dropdowns(self):
        st_df = self.dm.get_all_students_df()
        st_items = []
        if not st_df.empty:
            for _, r in st_df.iterrows():
                st_items.append(f"{r['Roll No']} - {r['Name']} ({r['Department']})")
        self.combo_student["values"] = st_items
        if st_items:
            self.combo_student.set(st_items[0])
        else:
            self.combo_student.set("")

        comp_df = self.dm.get_all_companies_df()
        comp_items = []
        if not comp_df.empty:
            for _, r in comp_df.iterrows():
                comp_items.append(f"{r['Company Name']} | {r['Role']}")
        self.combo_company["values"] = comp_items
        if comp_items:
            self.combo_company.set(comp_items[0])
        else:
            self.combo_company.set("")

    def load_applications(self):
        for item in self.tree_apps.get_children():
            self.tree_apps.delete(item)

        df = self.dm.get_all_applications_df()
        filter_status = self.combo_status_filter.get()

        if not df.empty and filter_status != "All":
            df = df[df["Status"].str.lower() == filter_status.lower()]

        if not df.empty:
            for _, r in df.iterrows():
                status = str(r.get("Status", "Applied"))
                self.tree_apps.insert(
                    "",
                    "end",
                    values=(
                        r.get("Application ID", ""),
                        r.get("Roll No", ""),
                        r.get("Student Name", ""),
                        r.get("Company Name", ""),
                        r.get("Role", ""),
                        status,
                        r.get("Applied Date", "")
                    ),
                    tags=(status,)
                )

    def on_app_selected(self, event):
        selected = self.tree_apps.selection()
        if not selected:
            return
        vals = self.tree_apps.item(selected[0], "values")
        if vals:
            self.selected_app_id = vals[0]
            current_status = vals[5]
            if current_status in self.combo_new_status["values"]:
                self.combo_new_status.set(current_status)

    def submit_application(self):
        st_val = self.combo_student.get()
        comp_val = self.combo_company.get()

        if not st_val:
            messagebox.showwarning("Notice", "Please select a student.")
            return
        if not comp_val:
            messagebox.showwarning("Notice", "Please select a company & role.")
            return

        roll_no = st_val.split(" - ")[0].strip()
        parts = comp_val.split(" | ")
        company_name = parts[0].strip()
        role = parts[1].strip() if len(parts) > 1 else ""

        try:
            student = self.dm.get_student_by_roll(roll_no)
            comp_df = self.dm.get_all_companies_df()
            matching_comp = comp_df[
                (comp_df["Company Name"].str.lower() == company_name.lower()) &
                (comp_df["Role"].str.lower() == role.lower())
            ]
            if not matching_comp.empty:
                comp_obj = self.dm.get_company_by_id(matching_comp.iloc[0]["Company ID"])
                if comp_obj and student:
                    is_elig, reason, _ = comp_obj.is_student_eligible(student)
                    if not is_elig:
                        proceed = messagebox.askyesno(
                            "Eligibility Advisory",
                            f"Student {student.name} may not meet criteria:\n\n{reason}\n\nDo you still want to proceed with application?",
                            icon="question"
                        )
                        if not proceed:
                            return

            app = self.dm.apply_student(roll_no, company_name, role)
            messagebox.showinfo("Success", f"Application submitted successfully! (ID: {app.app_id})")

            self.load_applications()
            self.refresh_statistics()

            if self.on_data_changed:
                self.on_data_changed()

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit application: {e}")

    def update_application_status(self):
        if not self.selected_app_id:
            messagebox.showwarning("Notice", "Please select an application from the table first.")
            return

        new_status = self.combo_new_status.get()
        try:
            self.dm.update_application_status(self.selected_app_id, new_status)
            messagebox.showinfo("Success", f"Application '{self.selected_app_id}' updated to '{new_status}'.")
            self.load_applications()
            self.refresh_statistics()

            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {e}")

    def delete_application(self):
        if not self.selected_app_id:
            messagebox.showwarning("Notice", "Please select an application to remove.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete application '{self.selected_app_id}'?",
            icon="warning"
        )
        if not confirm:
            return

        try:
            self.dm.delete_application(self.selected_app_id)
            messagebox.showinfo("Deleted", f"Application '{self.selected_app_id}' removed.")
            self.selected_app_id = None
            self.load_applications()
            self.refresh_statistics()

            if self.on_data_changed:
                self.on_data_changed()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete application: {e}")

    def refresh_statistics(self):
        stats = self.dm.get_placement_statistics()

        self.kpi_total.config(text=str(stats["total_students"]))
        self.kpi_placed.config(text=str(stats["placed_students_count"]))
        self.kpi_rate.config(text=f"{stats['placement_rate']:.1f}%")
        self.kpi_cgpa.config(text=f"{stats['avg_cgpa_placed']:.2f}")

        self.render_chart(stats)

    def render_chart(self, stats: dict = None):
        if stats is None:
            stats = self.dm.get_placement_statistics()

        chart_choice = self.combo_chart.get()

        fig = Figure(figsize=(5.2, 3.8), dpi=100)
        fig.patch.set_facecolor("#FFFFFF")
        ax = fig.add_subplot(111)

        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        if chart_choice == "Application Status Distribution (Donut)":
            self._plot_status_donut(ax, stats)
        elif chart_choice == "Department-wise Placement (Bar)":
            self._plot_dept_placement(ax, stats)
        elif chart_choice == "Student CGPA Distribution (NumPy Stats)":
            self._plot_cgpa_distribution(ax, stats)
        elif chart_choice == "Top Hiring Companies (Bar)":
            self._plot_top_companies(ax, stats)
        else:
            self._plot_status_donut(ax, stats)

        fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def _plot_status_donut(self, ax, stats):
        status_counts = stats.get("status_counts", {})
        labels = [k for k, v in status_counts.items() if v > 0]
        values = [v for k, v in status_counts.items() if v > 0]

        if not values or sum(values) == 0:
            ax.text(0.5, 0.5, "No application data available to display.", ha="center", va="center", color=TEXT_MUTED)
            ax.axis("off")
            return

        colors_map = {
            "Selected": "#10B981",
            "Shortlisted": "#F59E0B",
            "Applied": "#3B82F6",
            "Rejected": "#EF4444"
        }
        colors = [colors_map.get(lbl, "#94A3B8") for lbl in labels]

        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,
            wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
            textprops=dict(color=TEXT_PRIMARY, fontsize=9)
        )
        for at in autotexts:
            at.set_color("#FFFFFF")
            at.set_weight("bold")
            at.set_fontsize(8)

        ax.set_title("Application Status Breakdown", fontsize=11, fontweight="bold", pad=12, color=TEXT_PRIMARY)

    def _plot_dept_placement(self, ax, stats):
        dept_df = stats.get("department_stats", pd.DataFrame())
        if dept_df.empty:
            ax.text(0.5, 0.5, "No department data available.", ha="center", va="center", color=TEXT_MUTED)
            ax.axis("off")
            return

        depts = dept_df["Department"].tolist()
        total_students = dept_df["Total Students"].tolist()
        placed_students = dept_df["Placed Students"].tolist()

        x = np.arange(len(depts))
        width = 0.35

        ax.bar(x - width/2, total_students, width, label="Total Students", color="#93C5FD", edgecolor="#2563EB")
        ax.bar(x + width/2, placed_students, width, label="Placed Students", color="#34D399", edgecolor="#059669")

        ax.set_ylabel("Number of Students", fontsize=9, fontweight="bold")
        ax.set_title("Department-wise Students vs Placed", fontsize=11, fontweight="bold", pad=12)
        ax.set_xticks(x)
        short_depts = [d.replace("Computer Science", "CSE").replace("Information Technology", "IT").replace("Data Science", "DS").replace("Electronics", "ECE").replace("Mechanical", "MECH") for d in depts]
        ax.set_xticklabels(short_depts, rotation=15, ha="right", fontsize=8)
        ax.legend(fontsize=8)
        ax.grid(axis="y", linestyle="--", alpha=0.5)

    def _plot_cgpa_distribution(self, ax, stats):
        st_df = self.dm.get_all_students_df()
        if st_df.empty or "CGPA" not in st_df.columns:
            ax.text(0.5, 0.5, "No student CGPA data available.", ha="center", va="center", color=TEXT_MUTED)
            ax.axis("off")
            return

        cgpas = np.array(st_df["CGPA"].dropna().values, dtype=float)
        if len(cgpas) == 0:
            ax.text(0.5, 0.5, "No CGPA records found.", ha="center", va="center", color=TEXT_MUTED)
            ax.axis("off")
            return

        mean_cgpa = np.mean(cgpas)
        median_cgpa = np.median(cgpas)

        bins = np.linspace(6.0, 10.0, 9)
        n, bins_out, patches = ax.hist(cgpas, bins=bins, color="#818CF8", edgecolor="#4F46E5", alpha=0.85)

        ax.axvline(mean_cgpa, color="#DC2626", linestyle="--", linewidth=1.5, label=f"Mean: {mean_cgpa:.2f}")
        ax.axvline(median_cgpa, color="#059669", linestyle=":", linewidth=1.5, label=f"Median: {median_cgpa:.2f}")

        ax.set_xlabel("CGPA", fontsize=9, fontweight="bold")
        ax.set_ylabel("Student Count", fontsize=9, fontweight="bold")
        ax.set_title(f"CGPA Distribution (N={len(cgpas)})", fontsize=11, fontweight="bold", pad=12)
        ax.legend(fontsize=8)
        ax.grid(axis="y", linestyle="--", alpha=0.5)

    def _plot_top_companies(self, ax, stats):
        top_comp = stats.get("top_companies", {})
        if not top_comp:
            ax.text(0.5, 0.5, "No placement selections recorded yet.", ha="center", va="center", color=TEXT_MUTED)
            ax.axis("off")
            return

        comps = list(top_comp.keys())
        counts = list(top_comp.values())

        y_pos = np.arange(len(comps))
        ax.barh(y_pos, counts, color="#60A5FA", edgecolor="#1D4ED8", height=0.5)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(comps, fontsize=8)
        ax.invert_yaxis()
        ax.set_xlabel("Selected Students Count", fontsize=9, fontweight="bold")
        ax.set_title("Top Recruiting Companies", fontsize=11, fontweight="bold", pad=12)
        ax.grid(axis="x", linestyle="--", alpha=0.5)
