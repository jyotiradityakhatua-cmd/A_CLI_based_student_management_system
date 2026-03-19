from student import student


def menu():
    print("\n-- Student Management System ---")
    print("1. Add Student")
    print("2. View all Students")
    print("3. Search by Roll No")
    print("4. Search by Name")
    print("5. Filter by Course")
    print("6. Update Student")
    print("7. Delete Student")
    print("8. Exit")


def get_roll(prompt):
    raw = input(prompt).strip()
    if raw is None:
        print("Give correct credentials as input")
        return None
    value = raw.strip()
    if not value or not value.isdigit():
        print("Roll no must contain digits only. Give correct credentials as input.")
        return None
    return int(value)


def get_text(prompt):
    raw = input(prompt).strip()
    if raw is None:
        print("Give correct credentials as input")
        return None
    value = raw.strip()
    if not value:
        print("Input cannot be blank or spaces. Give correct credentials as input.")
        return None
    return value


def main():
    system = student()

    while True:
        menu()
        choice = input("enter the choice: ").strip()

        if choice == "1":
            roll = get_roll("roll no: ")
            if roll is None:
                continue
            name = get_text("Name: ")
            if name is None:
                continue
            course = get_text("course: ")
            if course is None:
                continue
            system.add_student(roll, name, course)

        elif choice == "2":
            system.view_all()

        elif choice == "3":
            roll = get_roll("roll no: ")
            if roll is None:
                continue
            system.search_by_roll(roll)

        elif choice == "4":
            name = get_text("name: ")
            if name is None:
                continue
            system.search_by_name(name)

        elif choice == "5":
            course = get_text("course: ")
            if course is None:
                continue
            system.filter_by_course(course)

        elif choice == "6":
            roll = get_roll("roll no to update: ")
            if roll is None:
                continue
            course = get_text("course of record to update: ")
            if course is None:
                continue
            name = get_text("new name: ")
            if name is None:
                continue
            system.update_student(roll, course, name)

        elif choice == "7":
            roll = get_roll("roll no: ")
            if roll is None:
                continue
            course = get_text("course: ")
            if course is None:
                continue
            system.delete_student(roll, course)

        elif choice == "8":
            print("exit")
            break

        else:
            print("invalid choice")


if __name__ == "__main__":
    main()
