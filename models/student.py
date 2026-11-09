"""
Student Data Model
Represents a student profile with academic and skill details.
"""

class Student:
    """Represents a student enrolled in the college."""

    def __init__(self, roll_no: str, name: str, department: str, cgpa: float, skills: str):
        self.roll_no = str(roll_no).strip().upper()
        self.name = str(name).strip().title()
        self.department = str(department).strip()
        self.cgpa = round(float(cgpa), 2)
        self.skills = self._clean_skills(skills)

    @staticmethod
    def _clean_skills(skills_input) -> str:
        """Helper to format and clean skill strings."""
        if isinstance(skills_input, list):
            items = [str(s).strip() for s in skills_input if str(s).strip()]
            return ", ".join(items)
        if isinstance(skills_input, str):
            items = [s.strip() for s in skills_input.split(",") if s.strip()]
            return ", ".join(items)
        return ""

    @property
    def skills_list(self) -> list:
        """Returns skills as a list of lowercase strings for matching."""
        if not self.skills:
            return []
        return [s.strip().lower() for s in self.skills.split(",") if s.strip()]

    def has_skill(self, skill_name: str) -> bool:
        """Check if student possesses a given skill."""
        return skill_name.strip().lower() in self.skills_list

    def to_dict(self) -> dict:
        """Convert student object to dictionary for storage and DataFrame."""
        return {
            "Roll No": self.roll_no,
            "Name": self.name,
            "Department": self.department,
            "CGPA": self.cgpa,
            "Skills": self.skills
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Student object from a dictionary or DataFrame row."""
        return cls(
            roll_no=data.get("Roll No") or data.get("roll_no", ""),
            name=data.get("Name") or data.get("name", ""),
            department=data.get("Department") or data.get("department", ""),
            cgpa=data.get("CGPA") or data.get("cgpa", 0.0),
            skills=data.get("Skills") or data.get("skills", "")
        )

    def validate(self):
        """Validate student fields. Raises ValueError if invalid."""
        if not self.roll_no:
            raise ValueError("Roll Number is required and cannot be empty.")
        if not self.name:
            raise ValueError("Student Name is required.")
        if not self.department:
            raise ValueError("Department must be selected.")
        if not (0.0 <= self.cgpa <= 10.0):
            raise ValueError(f"CGPA must be between 0.0 and 10.0 (received: {self.cgpa}).")
        if not self.skills:
            raise ValueError("Please provide at least one skill.")
        return True

    def __repr__(self):
        return f"<Student {self.roll_no} - {self.name} ({self.department}, CGPA: {self.cgpa})>"
