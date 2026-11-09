"""
Application Data Model
Represents an application made by a student for a job opening.
"""
from datetime import datetime

class Application:
    """Represents a job application and its recruitment status."""

    VALID_STATUSES = ["Applied", "Shortlisted", "Selected", "Rejected"]

    def __init__(self, app_id: str, roll_no: str, student_name: str, company_name: str, role: str, status: str = "Applied", applied_date: str = None):
        self.app_id = str(app_id).strip().upper()
        self.roll_no = str(roll_no).strip().upper()
        self.student_name = str(student_name).strip()
        self.company_name = str(company_name).strip()
        self.role = str(role).strip()
        
        status_clean = str(status).strip().capitalize()
        if status_clean not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Must be one of {self.VALID_STATUSES}")
        self.status = status_clean

        if applied_date:
            self.applied_date = str(applied_date).strip()
        else:
            self.applied_date = datetime.now().strftime("%Y-%m-%d")

    def update_status(self, new_status: str):
        """Update recruitment status with validation."""
        clean = str(new_status).strip().capitalize()
        if clean not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self.status = clean

    def to_dict(self) -> dict:
        """Convert application object to dictionary."""
        return {
            "Application ID": self.app_id,
            "Roll No": self.roll_no,
            "Student Name": self.student_name,
            "Company Name": self.company_name,
            "Role": self.role,
            "Status": self.status,
            "Applied Date": self.applied_date
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create Application object from dictionary or DataFrame row."""
        return cls(
            app_id=data.get("Application ID") or data.get("app_id", ""),
            roll_no=data.get("Roll No") or data.get("roll_no", ""),
            student_name=data.get("Student Name") or data.get("student_name", ""),
            company_name=data.get("Company Name") or data.get("company_name", ""),
            role=data.get("Role") or data.get("role", ""),
            status=data.get("Status") or data.get("status", "Applied"),
            applied_date=data.get("Applied Date") or data.get("applied_date", "")
        )

    def validate(self):
        """Validate application fields."""
        if not self.app_id:
            raise ValueError("Application ID is required.")
        if not self.roll_no:
            raise ValueError("Student Roll Number is required.")
        if not self.company_name:
            raise ValueError("Company Name is required.")
        if not self.role:
            raise ValueError("Job Role is required.")
        return True

    def __repr__(self):
        return f"<Application {self.app_id} | {self.roll_no} -> {self.company_name} ({self.status})>"
