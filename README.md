# Employee Management System

This is a Django-based Employee Management System designed to streamline various employee-related operations for an organization, from face recognition for attendance to task assignments and leave requests. The system includes an admin interface, individual admin dashboards, and QR code generation for easy profile access, along with CRUD operations for managing employees.

Repository: [Sabarevason07/employee_management_Django](https://github.com/Sabarevason07/employee_management_Django)

## Features

- **Employee CRUD Operations**: Add, update, and delete employee records.
- **Face Recognition Model**: Used for employee attendance verification.
- **QR Code Generation**: Generates QR codes for individual employee profiles.
- **Task Assignment**: Admins can assign tasks to employees and track their progress.
- **Leave Request Management**: Employees can request leaves, which are then managed by the HR/admin.
- **Individual Admin Page**: Admins have dedicated pages for managing their operations.
- **Dashboard**: A comprehensive dashboard for tracking employee status, tasks, leave requests, etc.
- **Admin Interface**: A user-friendly interface for managing all features and functions.
  
## Tech Stack

- **Back-End**: Django
- **Front-End**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Machine Learning**: Face recognition model for employee attendance
- **Other Libraries**: `qrcode` for QR code generation, `dlib` and `face_recognition` for facial recognition

## Prerequisites

- **Python** (version 3.8 or above)
- **Git**
- **Virtualenv** (recommended for creating a virtual environment)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Sabarevason07/employee_management_Django.git
   cd employee_management_Django
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the App**:
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Requirements

Ensure that `requirements.txt` includes the following packages:
- Django
- qrcode
- face_recognition
- dlib
- pillow

(For a full list, refer to the `requirements.txt` in the repository.)

## Usage

1. **Admin Dashboard**: Access the admin dashboard for employee and task management.
2. **Employee Registration**: Use the CRUD functionality to manage employee records.
3. **Face Recognition for Attendance**: Run the face recognition model for employee attendance verification.
4. **QR Code Profile Access**: Generate QR codes for employees that link directly to their profiles.
5. **Task Assignment and Leave Management**: Assign tasks to employees and handle leave requests via the dashboard.

## Advantages

- **Automated Employee Management**: Simplifies HR tasks like attendance, leave management, and task assignments.
- **Enhanced Security**: Utilizes face recognition for attendance verification, ensuring accurate tracking.
- **Easy Access**: QR codes provide quick and accessible links to employee profiles.
- **Efficient Task Tracking**: Admins can assign and monitor tasks, promoting better productivity.
- **Centralized Management**: All features accessible from a single dashboard for admins.

## License

This project is open-source under the MIT License.

---

Let me know if you want any specific sections or details added!
