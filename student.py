from database import Database

class student:
    def __init__(self):
        self.db=Database()

    def add_student(self, roll_no, name, course):
        try:
            self.db.execute(
                "insert into students values (?,?,?)",
                (roll_no, name, course)
            )
            print("student added successfully")
        except:
            print("Roll number already exists")

    def view_all(self):
        result=self.db.execute("Select * from students")
        for row in result.fetchall():
            print(row)

    def search_by_roll(self, roll_no):
        result= self.db.execute(
            "select * from students where roll_no=?",
            (roll_no,)
        )
        print(result.fetchone())

    def search_by_name(self, name):
        result=self.db.execute(
            "select * from students where name like ?",
            ("%"+name+"%",)
        )
        for row in result.fetchall():
            print(row)

    def search_by_course(self, course):
        result=self.db.execute(
            "select * from students where course like ?",
            ("%"+course+"%",)
        )
        for row in result.fetchall():
            print(row)

    def update_student(self, roll_no, name, course):
        self.db.execute(
            "update students set name=?, course=? where roll_no=?",
            (name, course, roll_no)
        )
        print("student updated")

    def delete_student(self, roll_no):
        self.db.execute(
            "delete from students where roll_no=?",
            (roll_no,)
        )
        print("student deleted")