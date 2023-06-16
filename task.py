import re
import string
import random
from string import ascii_letters

students_points = {}
courses_activity = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
points_to_complete_course = {'Python': 600, 'DSA': 400, 'Databases': 480, 'Flask': 550}


class Student:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.id = generate_unique_id()


def generate_unique_id():
    # Generate a random 6-digit ID
    unique_id = random.randint(10000, 99999)
    return unique_id


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
    if any(student.email == email for student in students_points):
        print('This email is already taken.')
        return False
    return True


def check_points_format(points_list):
    if len(points_list) == 4 and all(x.isdecimal() for x in points_list):
        return True
    return False


def find_student_by_id(student_id):
    return next((stud for stud in students_points if stud.id == int(student_id)), None)


def add_students():
    while True:
        credentials = list(input().split())
        if ''.join(credentials) == 'back':
            print(f'Total {len(students_points)} students have been added.')
            return main()
        elif len(credentials) < 3:
            print("Incorrect credentials.")
            continue

        concatenated_string = ' '.join(credentials[1:-1])
        credentials[1:-1] = [concatenated_string]
        student = Student(credentials[0], credentials[1], credentials[2])
        if check_credentials(student.first_name, student.last_name, student.email):
            students_points[student] = [0, 0, 0, 0]
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
        students_points[student] = [float(a) + float(b) for a, b in zip(students_points[student], student_score[1:])]
        for points, course in zip(student_score[1:], courses_activity):
            if int(points):
                courses_activity[course] += 1
        print('Points updated.')


def compute_statistic():
    print(f'Most popular: {", ".join(str(num) for num in find_course_popularity())}')
    print(f'Least popular: {find_course_popularity(False)}')
    print(f'Highest activity: {", ".join(str(num) for num in find_course_activity())}')
    print(f'Lowest activity: {find_course_activity(False)}')
    print(f'Easiest course: {", ".join(str(num) for num in find_course_average())}')
    print(f'Hardest course: {find_course_average(False)}')

    while True:
        course = input()
        if ''.join(course) == 'back':
            return main()
        search_for_course = next((key for key in courses_activity.keys()
                                  if course.lower() == key.lower()), None)
        if search_for_course is None:
            print('Unknown course.')
            continue

        print(search_for_course, "\n{:<6}{:<10}{:5}".format("id", "points", "completed"))
        position = find_position(search_for_course)
        sorted_dict = dict(sorted(students_points.items(), key=sorting_key_by_id))
        reversed_dict = dict(sorted(sorted_dict.items(),
                                    key=lambda item: sorting_key_by_points(item, position), reverse=True))
        for element in reversed_dict:
            print("{:<6}{:<10}{:<5}".format(element.id, int(sorted_dict[element][position]),
                  str(round(calculate_percentage(int(sorted_dict[element][position]), search_for_course), 1)) + '%'))


def notify_student():
    counter = 0
    for student in students_points:
        ok = False
        i = 0
        for points, course in zip(students_points[student], points_to_complete_course):
            if points >= points_to_complete_course[course]:
                print(f'To: {student.email}')
                print('Re: Your Learning Progress')
                print(f'Hello, {student.first_name} {student.last_name}! You have accomplished our {course} course!')
                students_points[student][i] = 0
                ok = True
            i += 1
        if ok:
            counter += 1
    print(f'Total {counter} students have been notified.')
    return main()


def calculate_percentage(points, course):
    return points * 100 / points_to_complete_course[course]


def find_position(course):
    if course == 'Python':
        return 0
    if course == 'DSA':
        return 1
    if course == 'Databases':
        return 2
    if course == 'Flask':
        return 3


def sorting_key_by_id(item):
    key, value = item
    return key.id


def sorting_key_by_points(item, position):
    key, value = item
    return value[position]


def find_course_popularity(popular=True):
    courses = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
    for points in students_points.values():
        for score, course in zip(points, courses):
            if score:
                courses[course] += 1

    if check_for_zero_elements(courses):
        return "n/a"
    highest = max(courses.values())
    max_list = [k for k, v in courses.items() if v == highest]
    if popular:
        return max_list
    if len(max_list) == 4:
        return "n/a"
    return min(courses, key=courses.get)


def find_course_activity(activity=True):
    if check_for_zero_elements(courses_activity):
        return "n/a"
    highest = max(courses_activity.values())
    max_list = [k for k, v in courses_activity.items() if v == highest]
    if activity:
        return max_list
    if len(max_list) == 4:
        return "n/a"
    return min(courses_activity, key=courses_activity.get)


def find_course_average(easy=True):
    avg_courses = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
    total_points = [0, 0, 0, 0]
    for points_list in students_points.values():
        for i, score in enumerate(points_list):
            total_points[i] += score

    for i, avg in enumerate(avg_courses):
        if total_points[i]:
            avg_courses[avg] = total_points[i] / courses_activity.get(avg)

    if check_for_zero_elements(avg_courses):
        return "n/a"
    if easy:
        highest = max(avg_courses.values())
        return [k for k, v in avg_courses.items() if v == highest]
    return min(avg_courses, key=avg_courses.get)


def check_for_zero_elements(list_to_check):
    if all(element == 0 for element in list_to_check.values()):
        return True
    return False


def print_students_list():
    print('Students:')
    if len(students_points) == 0:
        print('No students found.')
    else:
        [print(student.id) for student in students_points]


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
        score_list = students_points[student]
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
        elif command == "statistics":
            print("Type the name of a course to see details or 'back' to quit:")
            return compute_statistic()
        elif command == "notify":
            return notify_student()
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
