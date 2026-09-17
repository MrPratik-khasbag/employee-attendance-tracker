"""A simple employee attendance tracker.

This program uses only Python's built-in tools. You do not need to install
anything extra. It saves your attendance records in attendance_records.csv,
which you can also open with Excel.
"""

import csv
from pathlib import Path
from datetime import date

PROJECT_FOLDER = Path(__file__).parent
EMPLOYEE_FILE = PROJECT_FOLDER / "employees.csv"
ATTENDANCE_FILE = PROJECT_FOLDER / "attendance_records.csv"


def create_attendance_file_if_needed():
    """Create the attendance file and its column headings the first time."""
    if not ATTENDANCE_FILE.exists():
        with ATTENDANCE_FILE.open("w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(["Employee ID", "Employee Name", "Date", "Status", "Notes"])


def load_employees():
    """Read employees.csv and return a dictionary using ID as the key."""
    employees = {}
    with EMPLOYEE_FILE.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            employees[row["Employee ID"]] = row
    return employees


def choose_status():
    """Ask for a valid attendance status until the user types one."""
    allowed_statuses = ["Present", "Absent", "Late", "Leave"]
    print("Choose a status: Present, Absent, Late, or Leave")
    while True:
        status = input("Status: ").strip().title()
        if status in allowed_statuses:
            return status
        print("Please type one of these: Present, Absent, Late, Leave.")


def record_attendance(employees):
    """Ask simple questions, then save one attendance record."""
    employee_id = input("Employee ID: ").strip().upper()
    if employee_id not in employees:
        print("I cannot find that Employee ID. Check employees.csv and try again.")
        return
    employee_name = employees[employee_id]["Employee Name"]
    print(f"Employee found: {employee_name}")
    attendance_date = input("Date (YYYY-MM-DD, or press Enter for today): ").strip() or str(date.today())
    status = choose_status()
    notes = input("Notes (optional): ").strip()
    with ATTENDANCE_FILE.open("a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow([employee_id, employee_name, attendance_date, status, notes])
    print("Attendance saved successfully.\n")


def show_summary():
    """Count each status in the saved attendance file and print the result."""
    counts = {"Present": 0, "Absent": 0, "Late": 0, "Leave": 0}
    with ATTENDANCE_FILE.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if row["Status"] in counts:
                counts[row["Status"]] += 1
    print("\nAttendance summary\n------------------")
    for status, count in counts.items(): print(f"{status}: {count}")
    print(f"Total records: {sum(counts.values())}\n")


def show_all_records():
    """Print every attendance record in a tidy, readable way."""
    with ATTENDANCE_FILE.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    if not rows:
        print("\nThere are no attendance records yet.\n")
        return
    print("\nSaved attendance records\n------------------------")
    for row in rows:
        print(f"{row['Date']} | {row['Employee ID']} | {row['Employee Name']} | {row['Status']} | {row['Notes']}")
    print()


def main():
    """Run the menu until the user chooses Exit."""
    create_attendance_file_if_needed()
    employees = load_employees()
    while True:
        print("Employee Attendance Tracker\n1. Record attendance\n2. Show summary\n3. Show all records\n4. Exit")
        choice = input("Choose 1, 2, 3, or 4: ").strip()
        if choice == "1": record_attendance(employees)
        elif choice == "2": show_summary()
        elif choice == "3": show_all_records()
        elif choice == "4": print("Goodbye!"); break
        else: print("Please choose a number from 1 to 4.\n")

if __name__ == "__main__":
    main()
