import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='',
    database='student_db'
)
cursor = conn.cursor()

def add_student(Student_number, Last_name, First_name, Middle_name, Age, Birthday, Contact_number):
    try:
        sql = 'INSERT INTO users (Student_number, Last_name, First_name, Middle_name, Age, Birthday, Contact_number) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        values = (Student_number, Last_name, First_name, Middle_name, Age, Birthday, Contact_number)
        cursor.execute(sql, values)
        conn.commit()
        print('Student Added Successfully!')
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def display_all_records():
    cursor.execute('SELECT * FROM users')
    records = cursor.fetchall()
    if records:
        print("\nAll Student Records:")
        for rec in records:
            print(rec)
    else:
        print("No Records Found!")


def update_student(Student_ID, Column, New_value):
    valid_columns = ["Student_number", "Last_name", "First_name", "Middle_name", "Age", "Birthday", "Contact_number"]
    
    if Column not in valid_columns:
        print("Invalid column name. Please choose a valid column.")
        return
    
    try:
        cursor.execute('SELECT * FROM users WHERE Student_number = %s', (Student_ID,))
        existing_record = cursor.fetchone()
        
        if not existing_record:
            print("No student found with the given Student number.")
            return
        
        sql = f'UPDATE users SET {Column} = %s WHERE Student_number = %s'
        cursor.execute(sql, (New_value, Student_ID))
        conn.commit()

        if cursor.rowcount > 0:
            print('Student Record Updated Successfully!')

            cursor.execute('SELECT * FROM users WHERE Student_number = %s', (Student_ID,))
            updated_record = cursor.fetchone()
            print("\nUpdated Record:", updated_record)
        else:
            print('Update failed. No changes were made.')

    except mysql.connector.Error as err:
        print(f"Error: {err}")


def delete_student(Student_ID):
    try:
        sql = 'DELETE FROM users WHERE Student_number = %s'
        cursor.execute(sql, (Student_ID,))
        conn.commit()
        print('Student Deleted Successfully!')
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def search_student(Last_name):
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
    print('6: Exit')

    choice = input('Enter your choice: ')

    if choice == '1':
        Student_number = input('Enter Student Number: ')
        Last_name = input('Enter Last Name: ')
        First_name = input('Enter First Name: ')
        Middle_name = input('Enter Middle Name: ')
        
        try:
            Age = int(input('Enter Age: '))
        except ValueError:
            print("Invalid age input. Please enter an integer.")
            continue
        
        Birthday = input('Enter Birthday (YYYY-MM-DD): ')
        Contact_number = input('Enter Contact Number: ')
        
        add_student(Student_number, Last_name, First_name, Middle_name, Age, Birthday, Contact_number)

    elif choice == '2':  
        display_all_records()

    elif choice == '3':  
        try:
            Student_ID = int(input('Enter Student number to Update: '))
            Column = input('Enter Column to Update (e.g., Last_name, Age, Contact_number): ')
            New_value = input('Enter New Value: ')
            update_student(Student_ID, Column, New_value)
        except ValueError:
            print("Invalid input. Please enter a valid Student number.")

    elif choice == '4': 
        try:
            Student_ID = int(input('Enter Student number to Delete: '))
            delete_student(Student_ID)
        except ValueError:
            print("Invalid input. Please enter a valid Student number.")

    elif choice == '5': 
        Last_name = input('Enter Last Name to Search: ')
        search_student(Last_name)

    elif choice == '6': 
        print('Exiting program...')
        break

    else:
        print('Invalid choice! Please try again.')

cursor.close()
conn.close()
