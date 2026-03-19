import sqlite3

class Database:
    def __init__(self,db_name="student.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        self.create_table()

    def create_table(self):
      
        self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students'")
        existing = self.cursor.fetchone()
        if existing:
            self.cursor.execute("PRAGMA table_info(students)")
            columns = self.cursor.fetchall()
           
            col_names = [c[1].lower() for c in columns]
            if 'id' not in col_names or 'roll_no' in col_names and columns[0][1] == 'roll_no' and columns[0][5] == 1:
                self.cursor.execute("ALTER TABLE students RENAME TO students_old")
                self.cursor.execute("""create table students(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    roll_no INTEGER NOT NULL,
                                    name TEXT NOT NULL,
                                    course TEXT NOT NULL,
                                    UNIQUE(roll_no, course)
                )""")
                self.cursor.execute("INSERT OR IGNORE INTO students(roll_no, name, course) SELECT roll_no, name, course FROM students_old")
                self.cursor.execute("DROP TABLE students_old")
                self.conn.commit()
                return

        self.cursor.execute("""create table if not exists students(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            roll_no INTEGER NOT NULL,
                            name TEXT NOT NULL,
                            course TEXT NOT NULL,
                            UNIQUE(roll_no, course)
        )""")
        self.conn.commit()

    def execute(self, query, params=()):
        self.cursor.execute(query,params)
        self.conn.commit()
        return self.cursor

    def close(self):
        self.conn.close()


