import re


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


def main():
    print("Learning Progress Tracker")

    while True:
        command = input()
        if command == 'exit':
            print('Bye!')
            break
        elif command == '' or command.isspace():
            print('No input.')
        elif command == 'add students':
            print("Enter student credentials or 'back' to return:")
            students_list = []

            while True:
                credentials = [word for word in input().split()]
                if len(credentials) != 0 and credentials[0] == 'back':
                    break
                if len(credentials) <= 2:
                    print("Incorrect credentials.")
                else:
                    if len(credentials) > 3:
                        concatenated_string = ' '.join(credentials[1:-1])
                        credentials[1:-1] = [concatenated_string]
                    student = Student(credentials[0], credentials[1], credentials[2])
                    if check_credentials(student.first_name, student.last_name, student.email):
                        students_list.append(student)
                        print('The student has been added.')
            print(f'Total {len(students_list)} students have been added.')
        elif command == 'back':
            print("Enter 'exit' to exit the program.")
        else:
            print('Error: unknown command!')


if __name__ == '__main__':
    main()
