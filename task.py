import re
import string
from string import ascii_letters

students_list = []
students_dict = {}


class Student:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.id = id(self)


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
    if any(student.email == email for student in students_list):
        print('This email is already taken.')
        return False
    return True


def check_points_format(points_list):
    if len(points_list) == 4 and all(x.isdecimal() for x in points_list):
        return True
    return False


def find_student_by_id(student_id):
    return next((stud for stud in students_list if stud.id == int(student_id)), None)


def add_students():
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
            students_dict[student] = [0, 0, 0, 0]
            print('The student has been added.')


def add_points():
    while True:
        student_score = list(input().split())
        if ''.join(student_score) == 'back':
            return main()
        if any(x not in string.digits for x in ''.join(student_score[0])):
            print(f'No student is found for id={student_score[0]}.')
            continue
        student = find_student_by_id(student_score[0])
        if student is None:
            print(f'No student is found for id={student_score[0]}.')
            continue
        elif not check_points_format(student_score[1:]):
            print('Incorrect points format.')
            continue
        students_dict[student] = [float(a) + float(b) for a, b in zip(students_dict[student], student_score[1:])]
        print('Points updated.')


def print_students_list():
    print('Students:')
    if len(students_list) == 0:
        print('No students found.')
    else:
        [print(student.id) for student in students_list]


def find_student_score():
    while True:
        student_id = ''.join(input())
        if student_id == 'back':
            return main()
        if any(ch not in string.digits for ch in student_id) or student_id == '':
            print(f'No student is found for id={student_id}.')
            continue
        student = find_student_by_id(student_id)
        if student is None:
            print(f'No student is found for id={student_id}.')
            continue
        score_list = students_dict[student]
        print(f'{student_id} points: Python={round(score_list[0])}; DSA={round(score_list[1])}; '
              f'Databases={round(score_list[2])}; Flask={round(score_list[3])}')


def main():
    while True:
        command = input()
        if command == "add students":
            print("Enter student credentials or 'back' to return:")
            return add_students()
        elif command == "back":
            print("Enter 'exit' to exit the program.")
            continue
        elif command == "list":
            print_students_list()
            continue
        elif command == "add points":
            print("Enter an id and points or 'back' to return:")
            return add_points()
        elif command == "find":
            print("Enter an id or 'back' to return:")
            return find_student_score()
        elif command == "exit":
            print("Bye!")
            break
        elif all(map(lambda j: j not in ascii_letters, command)):
            print("No input.")
            continue
        print("Error: unknown command!")
        continue


if __name__ == '__main__':
    print("Learning Progress Tracker")
    main()
