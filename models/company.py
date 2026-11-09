"""
Company Data Model
Represents a recruiting company, job vacancy, and eligibility criteria.
"""

class Company:
    """Represents a recruiting company and job opening."""

    def __init__(self, company_id: str, name: str, role: str, min_cgpa: float, required_skills: str, package_lpa: float = 0.0):
        self.company_id = str(company_id).strip().upper()
        self.name = str(name).strip()
        self.role = str(role).strip()
        self.min_cgpa = round(float(min_cgpa), 2)
        self.required_skills = self._clean_skills(required_skills)
        self.package_lpa = round(float(package_lpa), 2)

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
        """Returns required skills as lowercase list."""
        if not self.required_skills:
            return []
        return [s.strip().lower() for s in self.required_skills.split(",") if s.strip()]

    def is_student_eligible(self, student) -> tuple[bool, str, list]:
        """
        Check if a given student meets the company's eligibility criteria.
        Returns:
            (is_eligible: bool, reason: str, matched_skills: list)
        """
        if student.cgpa < self.min_cgpa:
            return False, f"CGPA {student.cgpa} is below minimum requirement of {self.min_cgpa}", []

        req_set = set(self.skills_list)
        student_set = set(student.skills_list)
        matched = list(req_set.intersection(student_set))

        if req_set and not matched:
            return False, f"Missing required skills ({self.required_skills})", []

        match_str = f"Eligible! CGPA {student.cgpa} >= {self.min_cgpa}. Matched {len(matched)}/{len(req_set)} skills."
        return True, match_str, matched

    def to_dict(self) -> dict:
        """Convert company object to dictionary."""
        return {
            "Company ID": self.company_id,
            "Company Name": self.name,
            "Role": self.role,
            "Min CGPA": self.min_cgpa,
            "Required Skills": self.required_skills,
            "Package (LPA)": self.package_lpa
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create Company object from dictionary or DataFrame row."""
        return cls(
            company_id=data.get("Company ID") or data.get("company_id", ""),
            name=data.get("Company Name") or data.get("name", ""),
            role=data.get("Role") or data.get("role", ""),
            min_cgpa=data.get("Min CGPA") or data.get("min_cgpa", 0.0),
            required_skills=data.get("Required Skills") or data.get("required_skills", ""),
            package_lpa=data.get("Package (LPA)") or data.get("package_lpa", 0.0)
        )

    def validate(self):
        """Validate company fields. Raises ValueError if invalid."""
        if not self.company_id:
            raise ValueError("Company ID is required.")
        if not self.name:
            raise ValueError("Company Name is required.")
        if not self.role:
            raise ValueError("Job Role is required.")
        if not (0.0 <= self.min_cgpa <= 10.0):
            raise ValueError(f"Minimum CGPA must be between 0.0 and 10.0 (received: {self.min_cgpa}).")
        if not self.required_skills:
            raise ValueError("Please provide at least one required skill.")
        if self.package_lpa < 0:
            raise ValueError("Package (LPA) cannot be negative.")
        return True

    def __repr__(self):
        return f"<Company {self.name} - {self.role} (Min CGPA: {self.min_cgpa})>"
