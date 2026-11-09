# 🎓 College Placement Management System

A beginner-friendly desktop application built with **Python**, **Tkinter**, **Pandas**, **NumPy**, and **Matplotlib**. It provides role-based access with dedicated login pages for both **Administrators** and **Students**, including self-registration for new students, company eligibility matching, and dynamic placement analytics.

---

## 🔐 Authentication & Roles

The system features secure login pages and role-based views backed by persistent storage in `data/users.csv`:

### 1. 👨‍💼 Admin Portal
- **Login Credentials**:
  - **Username**: `admin`
  - **Password**: `admin123`
- **Full System Management**:
  - **Student Management**: Add, view, search, update, and delete student records.
  - **Company & Eligibility**: Post company openings, criteria, and run bulk eligibility matchers.
  - **Applications & Placement**: Process applications, update status (`Applied` ➔ `Shortlisted` ➔ `Selected` ➔ `Rejected`), view statistics, and inspect embedded Matplotlib charts.

### 2. 🎓 Student Portal
- **Login Credentials**:
  - **Username / Roll Number**: `CS101` (or any registered roll number, e.g., `CS102`, `IT201`, `DS501`)
  - **Password**: `student123`
- **Personalized Student Career Dashboard**:
  - **My Profile**: View Name, Roll Number, Department, CGPA, and registered skills. Includes an **"Update Skills"** dialog.
  - **Job Openings & Eligibility**: View company vacancies with eligibility tags (`Eligible` in Green, `Ineligible` in Red) showing matched technical skills, and a **"🚀 Apply for Selected Job"** button.
  - **My Applications**: Track all submitted applications with real-time status badges (`Applied`, `Shortlisted`, `Selected 🎉`, `Rejected`) and the ability to withdraw pending applications.

### 3. 📝 Student Self-Registration
- New students can register themselves directly from the login page by providing:
  - Roll Number, Full Name, Department dropdown, CGPA, Technical Skills, and Password.
- Automatically creates both their student profile in `students.csv` and credentials in `users.csv`.

---

## 🌟 Core Modules Breakdown

### Module 1: 🎓 Student Management (Admin)
- **Add New Students**: Input Roll Number, Name, Department, CGPA (0.00 – 10.00), and Skills.
- **View Records**: Clean table (`ttk.Treeview`) with sorting, striped rows, and scrollbars.
- **Search & Filter**: Real-time filtering by Roll Number, Name, Skills, or Department.
- **Update Records**: Double-click any student row to load into form and edit.
- **Delete Records**: Safe deletion with confirmation dialogs and cascading clean-up.

### Module 2: 🏢 Company & Eligibility (Admin)
- **Post Openings**: Company ID, Name, Job Role, Minimum CGPA, Required Skills, Package (LPA).
- **Two-Way Eligibility Checker**:
  - **Company ➔ Students**: Find which students qualify for a given company opening.
  - **Student ➔ Companies**: Find which company openings a student qualifies for.

### Module 3: 📊 Applications & Placement Analytics (Admin)
- **Apply Students**: Direct application submission with duplicate prevention.
- **Status Lifecycle**: Update statuses (`Applied`, `Shortlisted`, `Selected`, `Rejected`).
- **KPI Metrics**: Total Students, Placed Students, Placement Rate (%), Average Placed CGPA.
- **Embedded Matplotlib Visualizations**:
  - 🍩 Application Status Breakdown (Donut chart)
  - 📊 Department-wise Placement Rates (Grouped bar chart)
  - 📈 Student CGPA Distribution (Histogram with NumPy Mean & Median lines)
  - 🏢 Top Hiring Companies (Horizontal bar chart)

---

## 🛠️ Technologies & Concepts Used

| Technology / Concept | Implementation |
| :--- | :--- |
| **Core Python & File Handling** | Persistent storage using CSV files in the `data/` directory (`students.csv`, `companies.csv`, `applications.csv`, `users.csv`). Standard `open()` and `csv` modules ensure data persistence across app restarts. |
| **Object-Oriented Programming (OOP)** | Modular classes: [`Student`](models/student.py), [`Company`](models/company.py), [`Application`](models/application.py), and [`User`](models/user.py) with validation and methods. |
| **Pandas** | High-performance CSV reading/writing, table filtering, and department aggregations in [`DataManager`](storage/data_manager.py). |
| **NumPy** | Statistical calculations: Mean, Median, Min, Max, Standard Deviation of CGPA, and placement percentage formulas. |
| **Matplotlib** | Interactive charts embedded directly inside the Tkinter window using `FigureCanvasTkAgg`. |
| **Tkinter GUI** | Modern desktop UI with login/registration views, role-based dashboards, `ttk.Notebook` tabs, and responsive layout grids. |

---

## 📁 Project Directory Structure

```text
college_placement_system/
│
├── data/                                 # Persistent CSV database folder (auto-created)
│   ├── students.csv                      # Student profiles
│   ├── companies.csv                     # Company criteria
│   ├── applications.csv                  # Application records & statuses
│   └── users.csv                         # User accounts & hashed passwords
│
├── models/                               # OOP Data Models
│   ├── __init__.py                       # Package exports
│   ├── user.py                           # User model & password hashing
│   ├── student.py                        # Student class & skill checks
│   ├── company.py                        # Company class & eligibility logic
│   └── application.py                    # Application lifecycle model
│
├── storage/                              # Data Persistence & Numerical Analytics
│   ├── __init__.py                       # Package exports
│   └── data_manager.py                   # CSV read/write, Pandas querying & NumPy stats
│
├── gui/                                  # Modular Tkinter Interface
│   ├── __init__.py                       # Package exports
│   ├── style.py                          # Theme, color palette & fonts
│   ├── login_window.py                   # Login & Student Registration UI
│   ├── student_portal.py                 # Student personalized dashboard
│   ├── student_tab.py                    # Module 1: Student Management (Admin)
│   ├── company_tab.py                    # Module 2: Company & Eligibility (Admin)
│   └── placement_tab.py                  # Module 3: Applications & Placement (Admin)
│
├── main.py                               # Application entry point & session controller
├── test_system.py                        # Automated unit tests (7 passing tests)
├── requirements.txt                      # Dependencies (pandas, numpy, matplotlib)
├── .gitignore                            # Git ignore configuration
└── README.md                             # Documentation
```

---

## 🚀 How to Set Up and Run

### 1. Open Terminal / PowerShell
```powershell
cd "your_folder_path"
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run the Desktop Application
```powershell
python main.py
```

### 4. Run the Automated Tests
```powershell
python test_system.py
```

---

## 💡 Quick Test Credentials

| Role | Username / Identifier | Password | Access |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full 3-module Admin Dashboard |
| **Student** | `CS101` (or any Roll No) | `student123` | Personalized Student Portal |
| **New Student** | Register on the **"📝 Student Registration"** tab | *Set by user* | Personalized Student Portal |
