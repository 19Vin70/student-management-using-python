import mysql.connector
import re
from datetime import datetime

conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='',
    database='student_db'
)
cursor = conn.cursor()

def student_exists(Student_number):
    cursor.execute('SELECT * FROM users WHERE Student_number = %s', (Student_number,))
    return cursor.fetchone() is not None

def validate_non_empty(input_str, field_name):
    if not input_str.strip():
        print(f"Error: {field_name} is required.")
        return False
    return True

def validate_name(name, field_name):
    if not re.match("^[A-Za-z ]+$", name):
        print(f"Error: {field_name} should contain only letters.")
        return False
    return True

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        return False

def validate_age(age):
    if not age.isdigit() or int(age) <= 0:
        print("Error: Age must be a positive integer.")
        return False
    return True

def validate_contact(contact):
    if not contact.isdigit() or len(contact) < 10:
        print("Error: Contact number must be numeric and at least 10 digits.")
        return False
    return True

def add_student():
    while True:
        Student_number = input('Enter Student Number: ').strip()
        if not validate_non_empty(Student_number, "Student Number"):
            continue
        if student_exists(Student_number):
            print("Error: Student Number already exists.")
            continue
        break

    while True:
        Last_name = input('Enter Last Name: ').strip()
        if validate_non_empty(Last_name, "Last Name") and validate_name(Last_name, "Last Name"):
            break

    while True:
        First_name = input('Enter First Name: ').strip()
        if validate_non_empty(First_name, "First Name") and validate_name(First_name, "First Name"):
            break

    while True:
        Middle_name = input('Enter Middle Name: ').strip()
        if validate_non_empty(Middle_name, "Middle Name") and validate_name(Middle_name, "Middle Name"):
            break

    while True:
        Age = input('Enter Age: ').strip()
        if validate_non_empty(Age, "Age") and validate_age(Age):
            Age = int(Age)
            break

    while True:
        Birthday = input('Enter Birthday (YYYY-MM-DD): ').strip()
        if validate_non_empty(Birthday, "Birthday") and validate_date(Birthday):
            break

    while True:
        Contact_number = input('Enter Contact Number: ').strip()
        if validate_non_empty(Contact_number, "Contact Number") and validate_contact(Contact_number):
            break

    try:
        sql = 'INSERT INTO users (Student_number, Last_name, First_name, Middle_name, Age, Birthday, Contact_number) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        values = (Student_number, Last_name, First_name, Middle_name, Age, Birthday, Contact_number)
        cursor.execute(sql, values)
        conn.commit()
        print('Student Added Successfully!')
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

def display_all_records():
    cursor.execute('SELECT * FROM users')
    records = cursor.fetchall()
    if records:
        print("\nAll Student Records:")
        for rec in records:
            print(rec)
    else:
        print("No Records Found!")

def update_student():
    while True:
        Student_ID = input('Enter Student Number to Update: ').strip()
        if validate_non_empty(Student_ID, "Student Number") and student_exists(Student_ID):
            break
        print("Error: Student Number does not exist.")

    valid_columns = ["Student_number", "Last_name", "First_name", "Middle_name", "Age", "Birthday", "Contact_number"]
    while True:
        Column = input('Enter Column to Update (e.g., Last_name, Age, Contact_number): ').strip()
        if Column in valid_columns:
            break
        print("Error: Invalid column name.")

    while True:
        New_value = input('Enter New Value: ').strip()
        if validate_non_empty(New_value, "New Value"):
            if Column == "Age" and not validate_age(New_value):
                continue
            if Column == "Birthday" and not validate_date(New_value):
                continue
            if Column == "Contact_number" and not validate_contact(New_value):
                continue
            break

    try:
        sql = f'UPDATE users SET {Column} = %s WHERE Student_number = %s'
        cursor.execute(sql, (New_value, Student_ID))
        conn.commit()
        print('Student Record Updated Successfully!')
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

def delete_student():
    while True:
        Student_ID = input('Enter Student Number to Delete: ').strip()
        if validate_non_empty(Student_ID, "Student Number") and student_exists(Student_ID):
            break
        print("Error: Student Number does not exist.")

    try:
        sql = 'DELETE FROM users WHERE Student_number = %s'
        cursor.execute(sql, (Student_ID,))
        conn.commit()
        print('Student Deleted Successfully!')
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

def search_student():
    while True:
        Last_name = input('Enter Last Name to Search: ').strip()
        if validate_non_empty(Last_name, "Last Name") and validate_name(Last_name, "Last Name"):
            break

    cursor.execute('SELECT * FROM users WHERE Last_name = %s', (Last_name,))
    records = cursor.fetchall()
    if records:
        print("\nSearch Results:")
        for rec in records:
            print(rec)
    else:
        print("No records found with that last name.")

while True:
    print('\nStudent Database System')
    print('Choose an option: \n')
    print('1: Add Student')
    print('2: Display All Records')
    print('3: Update Student Record')
    print('4: Delete Student')
    print('5: Search Student by Last Name')
    print('6: Exit\n')

    choice = input('Enter your choice: ').strip()

    if choice == '1':
        add_student()
    elif choice == '2':
        display_all_records()
    elif choice == '3':
        update_student()
    elif choice == '4':
        delete_student()
    elif choice == '5':
        search_student()
    elif choice == '6':
        print('Exiting program...')
        break
    else:
        print('Invalid choice! Please try again.')

cursor.close()
conn.close()
