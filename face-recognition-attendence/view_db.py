import sqlite3

def view_students():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()
    return students

def view_attendance():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attendance')
    attendance = c.fetchall()
    conn.close()
    return attendance

if __name__ == "__main__":
    print("Students Table:")
    students = view_students()
    for student in students:
        print(student)

    print("\nAttendance Table:")
    attendance = view_attendance()
    for record in attendance:
        print(record)
