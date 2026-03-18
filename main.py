from student import student

def menu():
    print("\n-- Student Management System ---")
    print("1. Add Student")
    print("2. View all Students")
    print("3. Search by Roll No")
    print("4. Search by name")
    print("5. Search by course")
    print("6. update student")
    print("7. delete student")
    print("8. exit")
2
def main():
    system=student()

    while True:
        menu()
        choice= input("enter the choice: ")

        if choice == "1":
            roll = int(input("roll no: "))
            name=input("Name: ")
            course=input("course: ")
            system.add_student(roll, name, course)

        elif choice =="2":
            system.view_all()

        elif choice =="3":
            roll=int(input("roll no: "))
            system.search_by_roll(roll)

        elif choice == "4":
            name=input("name: ")
            system.search_by_name(name)

        elif choice =="5":
            course=input("name: ")
            system.search_by_course(course)

        elif choice =="6":
            roll=int(input("roll no: "))
            name=input("new name: ")
            course=input("new course: ")
            system.update_student(roll, name, course)

        elif choice =="7":
            roll=int(input("roll no: "))
            system.delete_student(roll)

        elif choice =="8":
            print("exit")
            break

        else:
            print("invalid choice")

if __name__ == "__main__":
    main()

    menu()
        


