import json
import numpy as np
import matplotlib.pyplot as plt

class Student:
    def __init__(self, name, roll_no, enrollment_no, department):
        self.name = name
        self.roll_no = roll_no
        self.enrollment_no = enrollment_no
        self.department = department
        self.marks = {}

    def add_marks(self, semester, subjects):
        self.marks[semester] = subjects

    def get_subjects(self, semester):
        return self.marks.get(semester, {})

    def calculate_cgpa(self, semester):
        semester_marks = self.marks.get(semester, {})
        total_marks = sum(semester_marks.values())
        if total_marks == 0:
            return 0
        cgpa = total_marks / (len(semester_marks) * 10)
        return cgpa

    def calculate_total_marks(self, semester):
        semester_marks = self.marks.get(semester, {})
        return sum(semester_marks.values())
    def display_all_semester_marks(self):
        print(f"Student: {self.name}, Enrollment No: {self.enrollment_no}")
        all_marks = {}
        for semester, subjects in self.marks.items():
            print(f"\nSemester: {semester}")
            print("Subjects and Marks:")
            for subject, marks in subjects.items():
                print(f"  {subject}: {marks}")
                if subject in all_marks:
                    all_marks[subject].append(marks)
                else:
                    all_marks[subject] = [marks]
            print("Total Marks:", sum(subjects.values()))
            print("CGPA:", self.calculate_cgpa(semester))
        # Plotting graph for all semesters
        all_subjects = []
        all_marks = []
        for semester, subjects in self.marks.items():
            for subject, marks in subjects.items():
                all_subjects.append(f"{subject} (Semester {semester})")
                all_marks.append(marks)
        plt.figure(figsize=(10, 5))
        plt.bar(all_subjects, all_marks, color='skyblue')
        plt.xlabel('Subjects')
        plt.ylabel('Marks')
        plt.title('Marks vs Subjects for All Semesters')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

class PerformanceTracker:
    def __init__(self):
        self.students = {}
        self.admin_password = "admin123"
        self.load_data()

    def admin_login(self):
        password = input("Enter admin password: ")
        if password == self.admin_password:
            return True
        else:
            print("Incorrect password.")
            return False

    def add_student(self, student):
        self.students[student.enrollment_no] = student
        self.save_data()

    def remove_student(self, enrollment_no):
        if enrollment_no in self.students:
            del self.students[enrollment_no]
            print(f"Student with enrollment number '{enrollment_no}' removed successfully.")
            self.save_data()
        else:
            print(f"Student with enrollment number '{enrollment_no}' not found.")

    def update_marks(self, enrollment_no, semester, subjects):
        if enrollment_no in self.students:
            student = self.students[enrollment_no]
            for subject, marks in subjects.items():
                while marks > 100:
                    print("Marks cannot exceed 100. Please enter marks less than or equal to 100.")
                    marks = float(input(f"Enter marks obtained in {subject}: "))
                subjects[subject] = marks
            student.add_marks(semester, subjects)
            print(f"Marks updated for student with enrollment number '{enrollment_no}' for semester '{semester}'.")
            self.save_data()
        else:
            print(f"Student with enrollment number '{enrollment_no}' not found.")

    def display_student_info(self, enrollment_no, semester):
        if enrollment_no in self.students:
            student = self.students[enrollment_no]
            print(f"Name: {student.name}")
            print(f"Roll No: {student.roll_no}")
            print(f"Enrollment No: {student.enrollment_no}")
            print(f"Department: {student.department}")
            print(f"Semester: {semester}")
            print("Subjects and Marks:")
            print()
            semester_subjects = student.get_subjects(semester)
            for subject, marks in semester_subjects.items():
                print(f"  {subject} - Marks: {marks}")
            print("Total Marks:", student.calculate_total_marks(semester))
            print("CGPA:", student.calculate_cgpa(semester))
            subjects = list(semester_subjects.keys())
            marks = list(semester_subjects.values())
            plt.bar(subjects, marks, color='skyblue')
            plt.xlabel('Subjects')
            plt.ylabel('Marks')
            plt.title('Marks vs Subjects')
            
            plt.tight_layout()
            plt.show()
        else:
            print(f"Student with enrollment number '{enrollment_no}' not found.")
    

    def load_data(self):
        try:
            with open('student_data.json', 'r') as file:
                data = json.load(file)
                for enrollment_no, student_data in data.items():
                    student = Student(student_data['name'], student_data['roll_no'], enrollment_no, student_data['department'])
                    student.marks = student_data['marks']
                    self.students[enrollment_no] = student
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {}
        for enrollment_no, student in self.students.items():
            data[enrollment_no] = {
                'name': student.name,
                'roll_no': student.roll_no,
                'department': student.department,
                'marks': student.marks
            }
        with open('student_data.json', 'w') as file:
            json.dump(data, file)


tracker = PerformanceTracker()

while True:
        print("\nMenu:")
        print("1. Admin Login")
        print("2. Student Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            if tracker.admin_login():
                while True:
                    print("\nAdmin Menu:")
                    print("1. Add Student")
                    print("2. Remove Student")
                    print("3. Update Marks")
                    print("4. Display Student Information(Sem Wise)")
                    print("5. Display Student Information")
                    print("6. Name And Enrollment Number Of Student")
                    print("7. Logout")
                    print()
                    admin_choice = input("Enter your choice: ")
                    if admin_choice == '1':
                        name = input("Enter student name: ")
                        roll_no = input("Enter student roll number: ")
                        enrollment_no = input("Enter student enrollment number: ")
                        department = input("Enter student department: ")
                        student = Student(name, roll_no, enrollment_no, department)
                        num_semesters = int(input("Enter the number of semesters: "))
                        for i in range(num_semesters):
                            semester = input(f"Enter semester {i + 1} name: ")
                            num_subjects = int(input("Enter the number of subjects: "))
                            subjects = {}
                            for _ in range(num_subjects):
                                subject = input("Enter subject name: ")
                                marks = float(input(f"Enter marks obtained in {subject}: "))
                                while marks > 100:
                                    print("Marks cannot exceed 100. Please enter marks less than or equal to 100.")
                                    marks = float(input(f"Enter marks obtained in {subject}: "))
                                subjects[subject] = marks
                            student.add_marks(semester, subjects)
                        tracker.add_student(student)
                        print(f"Student with enrollment number '{enrollment_no}' added successfully.")
                    elif admin_choice == '2':
                        enrollment_no = input("Enter enrollment number of student to remove: ")
                        tracker.remove_student(enrollment_no)
                    elif admin_choice == '3':
                        enrollment_no = input("Enter enrollment number of student: ")
                        semester = input("Enter semester name: ")
                        num_subjects = int(input("Enter the number of subjects: "))
                        subjects = {}
                        subject_marks = {}
                        for _ in range(num_subjects):
                            subject = input("Enter subject name: ")
                            marks = float(input(f"Enter marks obtained in {subject}: "))
                            while marks > 100:
                                print("Marks cannot exceed 100. Please enter marks less than or equal to 100.")
                                marks = float(input(f"Enter marks obtained in {subject}: "))
                            subject_marks[subject] = marks
                        tracker.update_marks(enrollment_no, semester, subject_marks)
                    elif admin_choice == '4':
                        enrollment_no = input("Enter enrollment number of student: ")
                        
                        semester = input("Enter semester name: ")
                        tracker.display_student_info(enrollment_no, semester)
                    elif admin_choice == '5':
                        enrollment_no = input("Enter enrollment number of student: ")
                        if enrollment_no in tracker.students:
                            student = tracker.students[enrollment_no]
                            student.display_all_semester_marks()
                        
                    elif admin_choice == '6':
                        print("\nAll Students:")
                        for enrollment_no, student in tracker.students.items():
                            print(f"Name: {student.name}")
                            print(f"Roll No: {student.roll_no}")
                            print(f"Enrollment No: {student.enrollment_no}")
                        print()
                        
                    elif admin_choice == '7':
                        break
                    else:
                        print("Invalid choice. Please enter a valid option.")
        elif choice == '2':
            while True:
                print("\nStudent Menu:")
                print("1. Display Student Information(Sem Wise)")
                print("2. Display Student Information")
                print("3. Logout")
                student_choice = input("Enter your choice: ")
                if student_choice == '1':
                    enrollment_no = input("Enter enrollment number of student: ")
                    semester = input("Enter semester name: ")
                    tracker.display_student_info(enrollment_no, semester)
                elif student_choice == '2':
                    enrollment_no = input("Enter enrollment number of student: ")
                    if enrollment_no in tracker.students:
                            student = tracker.students[enrollment_no]
                            student.display_all_semester_marks()
                    
                elif student_choice == '3':
                    break    
                else:
                    print("Invalid choice. Please enter a valid option.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")



