from database import Database

class student:
    def __init__(self):
        self.db = Database()

    def add_student(self, roll_no, name, course):
        try:
            self.db.execute(
                "insert into students(roll_no, name, course) values (?, ?, ?)",
                (roll_no, name, course)
            )
            print("Student added successfully")
        except Exception as e:
            # Unique constraint error for same roll+course
            print("Could not add student. Either same roll number already exists in this course or invalid input.")

    def _format_student(self, row):
        if len(row) == 4:
            _, roll_no, name, course = row
        elif len(row) == 3:
            roll_no, name, course = row
        else:
            return str(row)
        return f"Roll no.: {roll_no}, Name: {name}, Course: {course}"

    def view_all(self):
        result = self.db.execute("select * from students")
        rows = result.fetchall()

        if not rows:
            print("No student found in the database")
            return

        for row in rows:
            print(self._format_student(row))

    def search_by_roll(self, roll_no):
        result = self.db.execute(
            "select * from students where roll_no=?",
            (roll_no,)
        )
        rows = result.fetchall()

        if not rows:
            print("No student found with roll number", roll_no)
            return

        for row in rows:
            print(self._format_student(row))

    def search_by_name(self, name):
        result = self.db.execute(
            "select * from students where name like ?",
            ("%" + name + "%",)
        )
        rows = result.fetchall()

        if not rows:
            print("No student found with this name", name)
            return

        for row in rows:
            print(self._format_student(row))

    def filter_by_course(self, course):
        result = self.db.execute(
            "select * from students where course like ?",
            ("%" + course + "%",)
        )
        rows = result.fetchall()

        if not rows:
            print("No student found in this course")
            return

        for row in rows:
            print(self._format_student(row))

    def update_student(self, roll_no, course, name):
        result = self.db.execute(
            "select * from students where roll_no=? and course=?",
            (roll_no, course)
        )
        stud = result.fetchone()

        if stud is None:
            print("No student found for given roll no and course")
            return

        self.db.execute(
            "update students set name=? where roll_no=? and course=?",
            (name, roll_no, course)
        )
        print("Student updated successfully")

    def delete_student(self, roll_no, course):
        result = self.db.execute(
            "select * from students where roll_no=? and course=?",
            (roll_no, course)
        )
        if result.fetchone() is None:
            print("Student does not exist for given roll no and course")
            return

        self.db.execute(
            "delete from students where roll_no=? and course=?",
            (roll_no, course)
        )
        print("Student deleted")