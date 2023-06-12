import re
from string import ascii_letters


class Student:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


def check_name(name):
    if re.match("^(?![-'])(?!.*[-']$)(?!.*[-'][-'])(?!.*[-'][-'\\s])[A-Za-z'\\s-]+$", name) and len(name) >= 2:
        return True
    return False


def check_email(email):
    if re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$", email):
        return True
    return False


def check_credentials(first_name, last_name, email):
    if not check_name(first_name):
        print('Incorrect first name.')
        return False
    if not check_name(last_name):
        print('Incorrect last name.')
        return False
    if not check_email(email):
        print('Incorrect email.')
        return False
    return True


def add_students():
    students_list = []
    while True:
        credentials = list(input().split())
        if ''.join(credentials) == 'back':
            print(f'Total {len(students_list)} students have been added.')
            return main()
        elif len(credentials) < 3:
            print("Incorrect credentials.")
            continue

        concatenated_string = ' '.join(credentials[1:-1])
        credentials[1:-1] = [concatenated_string]
        student = Student(credentials[0], credentials[1], credentials[2])
        if check_credentials(student.first_name, student.last_name, student.email):
            students_list.append(student)
            print('The student has been added.')


def main():
    print("Learning Progress Tracker")

    while True:
        command = input()
        if command == "add students":
            print("Enter student credentials or 'back' to return:")
            return add_students()
        elif command == "back":
            print("Enter 'exit' to exit the program.")
            continue
        elif command == "exit":
            print("Bye!")
            break
        elif all(map(lambda j: j not in ascii_letters, command)):
            print("No input.")
            continue

        print("Error: unknown command!")
        continue


if __name__ == '__main__':
    main()
