"""
Automated Test Suite for College Placement Management System
Tests models, authentication, student registration, storage, pandas queries, and numpy stats.
"""

import sys
import os
import shutil
import tempfile
import unittest
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from models.student import Student
from models.company import Company
from models.application import Application
from models.user import User
from storage.data_manager import DataManager


class TestCollegePlacementSystem(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.dm = DataManager(data_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_user_authentication(self):
        admin_user = self.dm.authenticate("admin", "admin123", expected_role=User.ROLE_ADMIN)
        self.assertIsNotNone(admin_user)
        self.assertTrue(admin_user.is_admin())

        with self.assertRaises(ValueError):
            self.dm.authenticate("admin", "wrongpass", expected_role=User.ROLE_ADMIN)

        st_user = self.dm.authenticate("CS101", "student123", expected_role=User.ROLE_STUDENT)
        self.assertIsNotNone(st_user)
        self.assertTrue(st_user.is_student())
        self.assertEqual(st_user.roll_no, "CS101")

        with self.assertRaises(ValueError):
            self.dm.authenticate("CS101", "student123", expected_role=User.ROLE_ADMIN)

    def test_student_self_registration(self):
        student, user = self.dm.register_student_account(
            roll_no="REG999",
            name="Priya Sharma",
            dept="Computer Science",
            cgpa=9.15,
            skills="Python, SQL, React",
            password="mysecretpassword"
        )
        self.assertEqual(student.roll_no, "REG999")
        self.assertEqual(user.username, "reg999")
        self.assertTrue(user.is_student())

        logged_in = self.dm.authenticate("REG999", "mysecretpassword", expected_role=User.ROLE_STUDENT)
        self.assertEqual(logged_in.roll_no, "REG999")

        with self.assertRaises(ValueError):
            self.dm.register_student_account(
                roll_no="REG999",
                name="Duplicate",
                dept="IT",
                cgpa=8.0,
                skills="Java",
                password="password"
            )

    def test_student_model(self):
        st = Student("TEST01", "John Doe", "Computer Science", 8.75, "Python, SQL")
        self.assertEqual(st.roll_no, "TEST01")
        self.assertEqual(st.cgpa, 8.75)
        self.assertTrue(st.has_skill("python"))
        self.assertTrue(st.has_skill("SQL"))
        self.assertFalse(st.has_skill("Rust"))
        self.assertTrue(st.validate())

        with self.assertRaises(ValueError):
            Student("TEST02", "Jane", "IT", 11.5, "Python").validate()

    def test_company_model_and_eligibility(self):
        comp = Company("TCMP01", "Acme Corp", "Backend Engineer", 8.0, "Python, SQL", 10.0)
        self.assertTrue(comp.validate())

        eligible_st = Student("ST01", "Alice", "CS", 8.5, "Python, SQL, Docker")
        ineligible_cgpa_st = Student("ST02", "Bob", "CS", 7.5, "Python, SQL")
        ineligible_skills_st = Student("ST03", "Charlie", "CS", 8.5, "Java, C++")

        is_elig1, reason1, matched1 = comp.is_student_eligible(eligible_st)
        self.assertTrue(is_elig1)
        self.assertIn("python", matched1)

        is_elig2, reason2, _ = comp.is_student_eligible(ineligible_cgpa_st)
        self.assertFalse(is_elig2)

        is_elig3, reason3, _ = comp.is_student_eligible(ineligible_skills_st)
        self.assertFalse(is_elig3)

    def test_student_crud(self):
        new_st = Student("NEW999", "New Student", "Data Science", 9.10, "Python, Pandas")
        self.dm.add_student(new_st)

        retrieved = self.dm.get_student_by_roll("NEW999")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "New Student")

        with self.assertRaises(ValueError):
            self.dm.add_student(new_st)

        updated_st = Student("NEW999", "New Student Updated", "Data Science", 9.30, "Python, Pandas, ML")
        self.dm.update_student("NEW999", updated_st)
        updated_retrieved = self.dm.get_student_by_roll("NEW999")
        self.assertEqual(updated_retrieved.name, "New Student Updated")

        self.dm.delete_student("NEW999")
        self.assertIsNone(self.dm.get_student_by_roll("NEW999"))

    def test_application_lifecycle(self):
        app = self.dm.apply_student("CS101", "Infosys", "Systems Engineer")
        self.assertIsNotNone(app.app_id)
        self.assertEqual(app.status, "Applied")

        with self.assertRaises(ValueError):
            self.dm.apply_student("CS101", "Infosys", "Systems Engineer")

        self.dm.update_application_status(app.app_id, "Selected")
        app_df = self.dm.get_all_applications_df()
        updated_row = app_df[app_df["Application ID"] == app.app_id].iloc[0]
        self.assertEqual(updated_row["Status"], "Selected")

    def test_placement_statistics_with_numpy_and_pandas(self):
        stats = self.dm.get_placement_statistics()
        self.assertIn("total_students", stats)
        self.assertIn("placed_students_count", stats)
        self.assertIn("placement_rate", stats)
        self.assertIn("cgpa_summary", stats)

        cgpa_summary = stats["cgpa_summary"]
        self.assertGreater(cgpa_summary["mean"], 0.0)
        self.assertGreater(cgpa_summary["max"], 0.0)
        self.assertLessEqual(cgpa_summary["min"], cgpa_summary["max"])


if __name__ == "__main__":
    unittest.main()
