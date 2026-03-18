import sqlite3

class Database:
    def __init__(self,db_name="student.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""create Table if not exists students(
                            roll_no INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            course TEXT NOT NULL
        )""")
        self.conn.commit()

    def execute(self, query, params=()):
        self.cursor.execute(query,params)
        self.conn.commit()
        return self.cursor

    def close(self):
        self.conn.close()


