import sqlite3

def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            date TEXT,
            time TEXT,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    conn.commit()
    conn.close()

def insert_attendance(name, date, time):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO students (name) VALUES (?)', (name,))
    c.execute('SELECT id FROM students WHERE name = ?', (name,))
    student_id = c.fetchone()[0]
    c.execute('INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)', (student_id, date, time))
    conn.commit()
    conn.close()
