"""
Data Manager Module
Handles persistent storage (CSV files), user authentication,
data querying with Pandas, and statistical computations with NumPy.
"""

import os
import csv
from datetime import datetime
import pandas as pd
import numpy as np

from models.student import Student
from models.company import Company
from models.application import Application
from models.user import User


class DataManager:
    """Manages reading, writing, updating, and analyzing placement data and user authentication."""

    STUDENT_COLUMNS = ["Roll No", "Name", "Department", "CGPA", "Skills"]
    COMPANY_COLUMNS = ["Company ID", "Company Name", "Role", "Min CGPA", "Required Skills", "Package (LPA)"]
    APPLICATION_COLUMNS = ["Application ID", "Roll No", "Student Name", "Company Name", "Role", "Status", "Applied Date"]
    USER_COLUMNS = ["Username", "Password_Hash", "Role", "Roll_No"]

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_dir = os.path.join(base_dir, "data")
        else:
            self.data_dir = data_dir

        self.students_file = os.path.join(self.data_dir, "students.csv")
        self.companies_file = os.path.join(self.data_dir, "companies.csv")
        self.applications_file = os.path.join(self.data_dir, "applications.csv")
        self.users_file = os.path.join(self.data_dir, "users.csv")

        self.initialize_storage()

    def initialize_storage(self):
        """Ensure data directory and CSV files exist with appropriate headers and seed data."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)

        # Initialize students.csv
        if not os.path.exists(self.students_file) or os.path.getsize(self.students_file) == 0:
            self._create_empty_csv(self.students_file, self.STUDENT_COLUMNS)
            self._seed_sample_students()

        # Initialize companies.csv
        if not os.path.exists(self.companies_file) or os.path.getsize(self.companies_file) == 0:
            self._create_empty_csv(self.companies_file, self.COMPANY_COLUMNS)
            self._seed_sample_companies()

        # Initialize applications.csv
        if not os.path.exists(self.applications_file) or os.path.getsize(self.applications_file) == 0:
            self._create_empty_csv(self.applications_file, self.APPLICATION_COLUMNS)
            self._seed_sample_applications()

        # Initialize users.csv
        if not os.path.exists(self.users_file) or os.path.getsize(self.users_file) == 0:
            self._create_empty_csv(self.users_file, self.USER_COLUMNS)
            self._seed_sample_users()

    def _create_empty_csv(self, file_path: str, columns: list):
        """Helper to create an empty CSV file with header using core Python file handling."""
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)

    def _seed_sample_students(self):
        """Populate initial realistic sample students."""
        sample_students = [
            Student("CS101", "Aarav Sharma", "Computer Science", 8.85, "Python, SQL, Machine Learning, Git"),
            Student("CS102", "Ananya Iyer", "Computer Science", 9.20, "Python, Java, Data Structures, Docker"),
            Student("IT201", "Rohan Mehta", "Information Technology", 7.90, "Web Development, React, JavaScript, SQL"),
            Student("IT202", "Pooja Verma", "Information Technology", 8.40, "Python, Cloud Computing, AWS, Linux"),
            Student("EC301", "Vikram Patel", "Electronics", 7.60, "Embedded Systems, C++, IoT, Python"),
            Student("EC302", "Sneha Rao", "Electronics", 8.10, "VLSI, MATLAB, C++, Python"),
            Student("ME401", "Karan Singh", "Mechanical", 7.20, "AutoCAD, SolidWorks, Python, Project Management"),
            Student("DS501", "Divya Nair", "Data Science", 9.40, "Python, Pandas, NumPy, Deep Learning, SQL"),
        ]
        df = pd.DataFrame([s.to_dict() for s in sample_students])
        df.to_csv(self.students_file, index=False)

    def _seed_sample_companies(self):
        """Populate initial realistic sample companies."""
        sample_companies = [
            Company("CMP01", "Google Cloud", "Software Development Engineer", 8.50, "Python, Data Structures, Git", 18.0),
            Company("CMP02", "Microsoft", "Data Analyst", 8.00, "Python, SQL, Pandas, Machine Learning", 14.5),
            Company("CMP03", "Infosys", "Systems Engineer", 7.00, "Python, Java, SQL", 6.5),
            Company("CMP04", "TCS Digital", "Full Stack Developer", 7.50, "JavaScript, React, SQL, Web Development", 7.5),
            Company("CMP05", "Qualcomm", "Embedded Software Engineer", 7.50, "C++, Embedded Systems, Linux", 12.0),
        ]
        df = pd.DataFrame([c.to_dict() for c in sample_companies])
        df.to_csv(self.companies_file, index=False)

    def _seed_sample_applications(self):
        """Populate initial realistic sample applications."""
        sample_apps = [
            Application("APP1001", "CS101", "Aarav Sharma", "Google Cloud", "Software Development Engineer", "Shortlisted", "2026-10-10"),
            Application("APP1002", "CS102", "Ananya Iyer", "Google Cloud", "Software Development Engineer", "Selected", "2026-10-11"),
            Application("APP1003", "DS501", "Divya Nair", "Microsoft", "Data Analyst", "Selected", "2026-10-12"),
            Application("APP1004", "IT201", "Rohan Mehta", "TCS Digital", "Full Stack Developer", "Selected", "2026-10-14"),
            Application("APP1005", "IT202", "Pooja Verma", "Microsoft", "Data Analyst", "Shortlisted", "2026-10-15"),
            Application("APP1006", "EC301", "Vikram Patel", "Qualcomm", "Embedded Software Engineer", "Applied", "2026-10-16"),
            Application("APP1007", "ME401", "Karan Singh", "Infosys", "Systems Engineer", "Rejected", "2026-10-17"),
        ]
        df = pd.DataFrame([a.to_dict() for a in sample_apps])
        df.to_csv(self.applications_file, index=False)

    def _seed_sample_users(self):
        """Populate initial users (Admin and pre-seeded students)."""
        users = [
            User("admin", User.hash_password("admin123"), User.ROLE_ADMIN, ""),
            User("cs101", User.hash_password("student123"), User.ROLE_STUDENT, "CS101"),
            User("cs102", User.hash_password("student123"), User.ROLE_STUDENT, "CS102"),
            User("it201", User.hash_password("student123"), User.ROLE_STUDENT, "IT201"),
            User("it202", User.hash_password("student123"), User.ROLE_STUDENT, "IT202"),
            User("ec301", User.hash_password("student123"), User.ROLE_STUDENT, "EC301"),
            User("ec302", User.hash_password("student123"), User.ROLE_STUDENT, "EC302"),
            User("me401", User.hash_password("student123"), User.ROLE_STUDENT, "ME401"),
            User("ds501", User.hash_password("student123"), User.ROLE_STUDENT, "DS501"),
        ]
        df = pd.DataFrame([u.to_dict() for u in users])
        df.to_csv(self.users_file, index=False)

    # =========================================================================
    # AUTHENTICATION & USER MANAGEMENT
    # =========================================================================

    def get_all_users_df(self) -> pd.DataFrame:
        """Load all registered users using Pandas."""
        try:
            df = pd.read_csv(self.users_file)
            if df.empty:
                return pd.DataFrame(columns=self.USER_COLUMNS)
            return df
        except Exception as e:
            print(f"Error loading users: {e}")
            return pd.DataFrame(columns=self.USER_COLUMNS)

    def authenticate(self, username_or_roll: str, plain_password: str, expected_role: str = None) -> User:
        """
        Authenticate a user by username or student roll number.
        """
        identifier = str(username_or_roll).strip().lower()
        if not identifier or not plain_password:
            raise ValueError("Please provide both username and password.")

        df = self.get_all_users_df()
        if df.empty:
            raise ValueError("No user accounts found in database.")

        matched_rows = df[
            (df["Username"].astype(str).str.lower() == identifier) |
            (df["Roll_No"].astype(str).str.lower() == identifier)
        ]

        if matched_rows.empty:
            raise ValueError("Account not found. Please check your credentials.")

        user_row = matched_rows.iloc[0]
        user = User.from_dict(user_row.to_dict())

        if not user.verify_password(plain_password):
            raise ValueError("Incorrect password. Please try again.")

        if expected_role and user.role != expected_role.lower():
            raise ValueError(f"Access denied: This portal is for {expected_role}s only.")

        return user

    def register_user(self, username: str, plain_password: str, role: str, roll_no: str = "") -> User:
        """Register a new user credential."""
        clean_user = username.strip().lower()
        if not clean_user:
            raise ValueError("Username cannot be empty.")
        if len(plain_password) < 4:
            raise ValueError("Password must be at least 4 characters long.")

        df = self.get_all_users_df()
        if not df.empty and clean_user in df["Username"].astype(str).str.lower().values:
            raise ValueError(f"Username '{username}' is already taken.")

        hashed = User.hash_password(plain_password)
        new_user = User(clean_user, hashed, role, roll_no)

        new_row = pd.DataFrame([new_user.to_dict()])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.users_file, index=False)
        return new_user

    def register_student_account(self, roll_no: str, name: str, dept: str, cgpa: float, skills: str, password: str) -> tuple[Student, User]:
        """
        Atomically register both a Student profile and a Student login account.
        """
        clean_roll = roll_no.strip().upper()

        st_df = self.get_all_students_df()
        if not st_df.empty and clean_roll in st_df["Roll No"].str.upper().values:
            raise ValueError(f"Student with Roll Number '{clean_roll}' already exists.")

        users_df = self.get_all_users_df()
        if not users_df.empty:
            if clean_roll.lower() in users_df["Username"].astype(str).str.lower().values:
                raise ValueError(f"Account for Roll Number '{clean_roll}' already exists.")

        student = Student(roll_no=clean_roll, name=name, department=dept, cgpa=cgpa, skills=skills)
        student.validate()

        # Create user credential first with the provided password
        user = self.register_user(
            username=clean_roll.lower(),
            plain_password=password,
            role=User.ROLE_STUDENT,
            roll_no=clean_roll
        )

        # Save student (create_default_user=False since user already registered)
        self.add_student(student, create_default_user=False)

        return student, user

    # =========================================================================
    # MODULE 1: STUDENT MANAGEMENT (CRUD & SEARCH)
    # =========================================================================

    def get_all_students_df(self) -> pd.DataFrame:
        """Load all students using Pandas."""
        try:
            df = pd.read_csv(self.students_file)
            if df.empty:
                return pd.DataFrame(columns=self.STUDENT_COLUMNS)
            df["CGPA"] = pd.to_numeric(df["CGPA"], errors="coerce").fillna(0.0)
            return df
        except Exception as e:
            print(f"Error loading students: {e}")
            return pd.DataFrame(columns=self.STUDENT_COLUMNS)

    def add_student(self, student: Student, create_default_user: bool = True) -> bool:
        """Add a new student after validating uniqueness of Roll Number."""
        student.validate()
        df = self.get_all_students_df()

        if not df.empty and student.roll_no in df["Roll No"].str.upper().values:
            raise ValueError(f"Student with Roll Number '{student.roll_no}' already exists.")

        new_row = pd.DataFrame([student.to_dict()])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.students_file, index=False)

        if create_default_user:
            try:
                users_df = self.get_all_users_df()
                if users_df.empty or student.roll_no.lower() not in users_df["Username"].astype(str).str.lower().values:
                    self.register_user(student.roll_no.lower(), "student123", User.ROLE_STUDENT, student.roll_no)
            except Exception:
                pass

        return True

    def update_student(self, original_roll_no: str, updated_student: Student) -> bool:
        """Update an existing student's record."""
        updated_student.validate()
        df = self.get_all_students_df()

        idx = df[df["Roll No"].str.upper() == original_roll_no.strip().upper()].index
        if len(idx) == 0:
            raise ValueError(f"Student with Roll Number '{original_roll_no}' not found.")

        if original_roll_no.strip().upper() != updated_student.roll_no:
            other_rolls = df.drop(idx)["Roll No"].str.upper().values
            if updated_student.roll_no in other_rolls:
                raise ValueError(f"New Roll Number '{updated_student.roll_no}' is already assigned to another student.")

        for col, val in updated_student.to_dict().items():
            df.loc[idx[0], col] = val

        df.to_csv(self.students_file, index=False)
        self._sync_student_name_in_applications(original_roll_no, updated_student.roll_no, updated_student.name)
        return True

    def _sync_student_name_in_applications(self, old_roll: str, new_roll: str, new_name: str):
        """Helper to sync student name and roll number in applications when updated."""
        try:
            app_df = self.get_all_applications_df()
            if not app_df.empty:
                matches = app_df["Roll No"].str.upper() == old_roll.strip().upper()
                if matches.any():
                    app_df.loc[matches, "Roll No"] = new_roll
                    app_df.loc[matches, "Student Name"] = new_name
                    app_df.to_csv(self.applications_file, index=False)
        except Exception as e:
            print(f"Error syncing student in applications: {e}")

    def delete_student(self, roll_no: str) -> bool:
        """Delete a student, cascade delete applications and user credentials."""
        df = self.get_all_students_df()
        clean_roll = roll_no.strip().upper()

        if clean_roll not in df["Roll No"].str.upper().values:
            raise ValueError(f"Student with Roll Number '{clean_roll}' not found.")

        df = df[df["Roll No"].str.upper() != clean_roll]
        df.to_csv(self.students_file, index=False)

        try:
            app_df = self.get_all_applications_df()
            if not app_df.empty:
                app_df = app_df[app_df["Roll No"].str.upper() != clean_roll]
                app_df.to_csv(self.applications_file, index=False)
        except Exception:
            pass

        try:
            user_df = self.get_all_users_df()
            if not user_df.empty:
                user_df = user_df[user_df["Roll_No"].astype(str).str.upper() != clean_roll]
                user_df.to_csv(self.users_file, index=False)
        except Exception:
            pass

        return True

    def search_students(self, query: str = "", department: str = "All") -> pd.DataFrame:
        """Filter students by search term (roll no, name, skills) and department."""
        df = self.get_all_students_df()
        if df.empty:
            return df

        if department and department != "All":
            df = df[df["Department"].str.lower() == department.lower()]

        if query and query.strip():
            q = query.strip().lower()
            mask = (
                df["Roll No"].str.lower().str.contains(q, na=False) |
                df["Name"].str.lower().str.contains(q, na=False) |
                df["Skills"].str.lower().str.contains(q, na=False)
            )
            df = df[mask]

        return df

    def get_student_by_roll(self, roll_no: str) -> Student:
        """Retrieve a specific Student object by roll number."""
        df = self.get_all_students_df()
        match = df[df["Roll No"].str.upper() == roll_no.strip().upper()]
        if match.empty:
            return None
        return Student.from_dict(match.iloc[0].to_dict())

    # =========================================================================
    # MODULE 2: COMPANY & ELIGIBILITY CHECKING
    # =========================================================================

    def get_all_companies_df(self) -> pd.DataFrame:
        """Load all companies using Pandas."""
        try:
            df = pd.read_csv(self.companies_file)
            if df.empty:
                return pd.DataFrame(columns=self.COMPANY_COLUMNS)
            df["Min CGPA"] = pd.to_numeric(df["Min CGPA"], errors="coerce").fillna(0.0)
            df["Package (LPA)"] = pd.to_numeric(df["Package (LPA)"], errors="coerce").fillna(0.0)
            return df
        except Exception as e:
            print(f"Error loading companies: {e}")
            return pd.DataFrame(columns=self.COMPANY_COLUMNS)

    def add_company(self, company: Company) -> bool:
        """Add a new company job opening."""
        company.validate()
        df = self.get_all_companies_df()

        if not df.empty and company.company_id in df["Company ID"].str.upper().values:
            raise ValueError(f"Company with ID '{company.company_id}' already exists.")

        new_row = pd.DataFrame([company.to_dict()])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.companies_file, index=False)
        return True

    def get_company_by_id(self, company_id: str) -> Company:
        """Retrieve a Company object by its ID."""
        df = self.get_all_companies_df()
        match = df[df["Company ID"].str.upper() == company_id.strip().upper()]
        if match.empty:
            return None
        return Company.from_dict(match.iloc[0].to_dict())

    def get_eligible_students_for_company(self, company: Company) -> list[dict]:
        """Check all students against a company's criteria."""
        students_df = self.get_all_students_df()
        results = []

        for _, row in students_df.iterrows():
            st = Student.from_dict(row.to_dict())
            is_eligible, reason, matched_skills = company.is_student_eligible(st)
            results.append({
                "Roll No": st.roll_no,
                "Name": st.name,
                "Department": st.department,
                "CGPA": st.cgpa,
                "Eligible": "Yes" if is_eligible else "No",
                "Reason": reason,
                "Matched Skills": ", ".join(matched_skills) if matched_skills else "None"
            })

        return results

    def get_eligible_companies_for_student(self, student: Student) -> list[dict]:
        """Check all companies against a student's profile."""
        companies_df = self.get_all_companies_df()
        results = []

        for _, row in companies_df.iterrows():
            comp = Company.from_dict(row.to_dict())
            is_eligible, reason, matched_skills = comp.is_student_eligible(student)
            results.append({
                "Company ID": comp.company_id,
                "Company Name": comp.name,
                "Role": comp.role,
                "Min CGPA": comp.min_cgpa,
                "Package (LPA)": comp.package_lpa,
                "Eligible": "Yes" if is_eligible else "No",
                "Status": "Qualified" if is_eligible else reason,
                "Matched Skills": ", ".join(matched_skills) if matched_skills else "None"
            })

        return results

    # =========================================================================
    # MODULE 3: APPLICATIONS & PLACEMENT MANAGEMENT
    # =========================================================================

    def get_all_applications_df(self) -> pd.DataFrame:
        """Load all job applications."""
        try:
            df = pd.read_csv(self.applications_file)
            if df.empty:
                return pd.DataFrame(columns=self.APPLICATION_COLUMNS)
            return df
        except Exception as e:
            print(f"Error loading applications: {e}")
            return pd.DataFrame(columns=self.APPLICATION_COLUMNS)

    def get_student_applications(self, roll_no: str) -> pd.DataFrame:
        """Get all applications submitted by a specific student."""
        df = self.get_all_applications_df()
        if df.empty:
            return df
        return df[df["Roll No"].str.upper() == roll_no.strip().upper()]

    def apply_student(self, roll_no: str, company_name: str, role: str) -> Application:
        """Create a new student application for a company role."""
        student = self.get_student_by_roll(roll_no)
        if not student:
            raise ValueError(f"Student '{roll_no}' does not exist.")

        app_df = self.get_all_applications_df()

        if not app_df.empty:
            duplicate = app_df[
                (app_df["Roll No"].str.upper() == roll_no.strip().upper()) &
                (app_df["Company Name"].str.lower() == company_name.strip().lower()) &
                (app_df["Role"].str.lower() == role.strip().lower())
            ]
            if not duplicate.empty:
                raise ValueError(f"Student {student.name} ({roll_no}) has already applied to {company_name} for the role '{role}'.")

        app_id = f"APP{datetime.now().strftime('%y%m%d%H%M%S')[-6:]}"
        application = Application(
            app_id=app_id,
            roll_no=student.roll_no,
            student_name=student.name,
            company_name=company_name.strip(),
            role=role.strip(),
            status="Applied",
            applied_date=datetime.now().strftime("%Y-%m-%d")
        )
        application.validate()

        new_row = pd.DataFrame([application.to_dict()])
        app_df = pd.concat([app_df, new_row], ignore_index=True)
        app_df.to_csv(self.applications_file, index=False)
        return application

    def update_application_status(self, app_id: str, new_status: str) -> bool:
        """Update recruitment status (Applied, Shortlisted, Selected, Rejected)."""
        app_df = self.get_all_applications_df()
        idx = app_df[app_df["Application ID"].str.upper() == app_id.strip().upper()].index

        if len(idx) == 0:
            raise ValueError(f"Application ID '{app_id}' not found.")

        clean_status = str(new_status).strip().capitalize()
        if clean_status not in Application.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {Application.VALID_STATUSES}")

        app_df.loc[idx[0], "Status"] = clean_status
        app_df.to_csv(self.applications_file, index=False)
        return True

    def delete_application(self, app_id: str) -> bool:
        """Delete an application record."""
        app_df = self.get_all_applications_df()
        clean_id = app_id.strip().upper()
        if clean_id not in app_df["Application ID"].str.upper().values:
            raise ValueError(f"Application ID '{clean_id}' not found.")

        app_df = app_df[app_df["Application ID"].str.upper() != clean_id]
        app_df.to_csv(self.applications_file, index=False)
        return True

    # =========================================================================
    # PLACEMENT STATISTICS WITH PANDAS & NUMPY
    # =========================================================================

    def get_placement_statistics(self) -> dict:
        """Compute placement statistics using Pandas and NumPy."""
        students_df = self.get_all_students_df()
        companies_df = self.get_all_companies_df()
        applications_df = self.get_all_applications_df()

        total_students = len(students_df)
        total_companies = len(companies_df)
        total_applications = len(applications_df)

        if total_students == 0:
            return {
                "total_students": 0,
                "total_companies": total_companies,
                "total_applications": total_applications,
                "placed_students_count": 0,
                "placement_rate": 0.0,
                "avg_cgpa_all": 0.0,
                "avg_cgpa_placed": 0.0,
                "cgpa_summary": {"mean": 0.0, "median": 0.0, "min": 0.0, "max": 0.0, "std": 0.0},
                "status_counts": {},
                "department_stats": pd.DataFrame(),
                "top_companies": {}
            }

        cgpa_array = np.array(students_df["CGPA"].dropna().values, dtype=float)
        cgpa_summary = {
            "mean": round(float(np.mean(cgpa_array)), 2) if len(cgpa_array) > 0 else 0.0,
            "median": round(float(np.median(cgpa_array)), 2) if len(cgpa_array) > 0 else 0.0,
            "min": round(float(np.min(cgpa_array)), 2) if len(cgpa_array) > 0 else 0.0,
            "max": round(float(np.max(cgpa_array)), 2) if len(cgpa_array) > 0 else 0.0,
            "std": round(float(np.std(cgpa_array)), 2) if len(cgpa_array) > 0 else 0.0,
        }

        if not applications_df.empty:
            selected_apps = applications_df[applications_df["Status"].str.lower() == "selected"]
            placed_roll_nos = set(selected_apps["Roll No"].str.upper().unique())
        else:
            placed_roll_nos = set()

        placed_count = len(placed_roll_nos)
        placement_rate = round(float(np.divide(placed_count * 100.0, total_students)), 2) if total_students > 0 else 0.0

        placed_mask = students_df["Roll No"].str.upper().isin(placed_roll_nos)
        placed_cgpas = students_df[placed_mask]["CGPA"].dropna().values
        avg_cgpa_placed = round(float(np.mean(placed_cgpas)), 2) if len(placed_cgpas) > 0 else 0.0

        if not applications_df.empty:
            status_series = applications_df["Status"].value_counts()
            status_counts = status_series.to_dict()
        else:
            status_counts = {}

        for s in Application.VALID_STATUSES:
            if s not in status_counts:
                status_counts[s] = 0

        dept_summary_list = []
        for dept, group in students_df.groupby("Department"):
            dept_total = len(group)
            dept_placed = sum(group["Roll No"].str.upper().isin(placed_roll_nos))
            dept_rate = round(float(np.divide(dept_placed * 100.0, dept_total)), 1) if dept_total > 0 else 0.0
            dept_summary_list.append({
                "Department": dept,
                "Total Students": dept_total,
                "Placed Students": dept_placed,
                "Placement Rate (%)": dept_rate
            })

        dept_df = pd.DataFrame(dept_summary_list)

        if not applications_df.empty and not selected_apps.empty:
            top_companies = selected_apps["Company Name"].value_counts().head(5).to_dict()
        else:
            top_companies = {}

        return {
            "total_students": total_students,
            "total_companies": total_companies,
            "total_applications": total_applications,
            "placed_students_count": placed_count,
            "unplaced_students_count": total_students - placed_count,
            "placement_rate": placement_rate,
            "avg_cgpa_all": cgpa_summary["mean"],
            "avg_cgpa_placed": avg_cgpa_placed,
            "cgpa_summary": cgpa_summary,
            "status_counts": status_counts,
            "department_stats": dept_df,
            "top_companies": top_companies
        }
