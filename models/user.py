"""
User Model
Represents an authenticated user (Admin or Student) with password hashing.
"""

import hashlib


class User:
    """Represents a system user with role-based access."""

    ROLE_ADMIN = "admin"
    ROLE_STUDENT = "student"
    VALID_ROLES = [ROLE_ADMIN, ROLE_STUDENT]

    def __init__(self, username: str, password_hash: str, role: str, roll_no: str = ""):
        self.username = str(username).strip()
        self.password_hash = str(password_hash).strip()
        self.role = str(role).strip().lower()
        self.roll_no = str(roll_no).strip().upper() if roll_no else ""

        if self.role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{self.role}'. Must be one of {self.VALID_ROLES}")

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Hash a plain text password using standard SHA-256."""
        return hashlib.sha256(plain_password.strip().encode("utf-8")).hexdigest()

    def verify_password(self, plain_password: str) -> bool:
        """Check if provided plain password matches stored hash."""
        return self.password_hash == self.hash_password(plain_password)

    def to_dict(self) -> dict:
        """Convert user object to dictionary for storage."""
        return {
            "Username": self.username,
            "Password_Hash": self.password_hash,
            "Role": self.role,
            "Roll_No": self.roll_no
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a User object from a dictionary or DataFrame row."""
        return cls(
            username=data.get("Username") or data.get("username", ""),
            password_hash=data.get("Password_Hash") or data.get("password_hash", ""),
            role=data.get("Role") or data.get("role", "student"),
            roll_no=data.get("Roll_No") or data.get("roll_no", "")
        )

    def is_admin(self) -> bool:
        return self.role == self.ROLE_ADMIN

    def is_student(self) -> bool:
        return self.role == self.ROLE_STUDENT

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
