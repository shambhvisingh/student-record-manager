"""
Student Record Management System
Created by: Shambhvi Singh
Class 12 Student | Learning Python, SQL & DBMS
This beginner project helps manage student records using SQLite.
"""

import sqlite3
import os

# Database file name
db_file = "student.db"

# Check if database already exists
db_exists = os.path.isfile(db_file)

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

if db_exists:
    print("🔗 Connected to existing database: student.db")
else:
    print("📁 New database created: student.db")

# Create the students table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        roll_no INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        student_class TEXT NOT NULL,
        marks INTEGER NOT NULL
    )
''')

def get_valid_int(prompt):
    """Ask the user for a valid integer input."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Please enter a valid number.")

def student_exists(roll):
    cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll,))
    return cursor.fetchone()

def add_student():
    print("\n➕ Add Student Record")
    roll = get_valid_int("Enter Roll No: ")

    if student_exists(roll):
        print("⚠️ A student with this Roll No already exists.")
        return

    name = input("Enter Name: ").strip()
    student_class = input("Enter Class: ").strip()
    marks = get_valid_int("Enter Marks: ")

    try:
        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?)",
            (roll, name, student_class, marks)
        )
        conn.commit()
        print("✅ Student added successfully.")
    except sqlite3.Error as e:
        print("❌ Error adding student:", e)

def view_students():
    print("\n📋 All Student Records")
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        if students:
            for row in students:
                print(f"Roll No: {row[0]}, Name: {row[1]}, Class: {row[2]}, Marks: {row[3]}")
        else:
            print("ℹ️ No records found.")
    except sqlite3.Error as e:
        print("❌ Error fetching records:", e)

def update_marks():
    print("\n✏️ Update Student Marks")
    roll = get_valid_int("Enter Roll No to update: ")

    if not student_exists(roll):
        print("❌ Student not found.")
        return

    new_marks = get_valid_int("Enter new marks: ")

    try:
        cursor.execute("UPDATE students SET marks = ? WHERE roll_no = ?", (new_marks, roll))
        conn.commit()
        print("✅ Marks updated.")
    except sqlite3.Error as e:
        print("❌ Error updating marks:", e)

def delete_student():
    print("\n🗑️ Delete Student Record")
    roll = get_valid_int("Enter Roll No to delete: ")

    if not student_exists(roll):
        print("❌ Student not found.")
        return

    try:
        cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll,))
        conn.commit()
        print("✅ Student deleted.")
    except sqlite3.Error as e:
        print("❌ Error deleting student:", e)

def menu():
    while True:
        print("\n👩‍🎓 Shambhvi's Student Record Manager")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Marks")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            update_marks()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("👋 Thanks for using the app. Goodbye!")
            break
        else:
            print("⚠️ Please choose a valid option.")

try:
    menu()
finally:
    conn.close()