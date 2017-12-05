#!/usr/bin/env python
# coding=utf-8
# Author: bloke


class School(object):

    course_dict = {}
    class_dict = {}
    teacher_list = []
    teacher_student_dict = {}
    teacher_class_dict = {}
    # member_list = teacher_list + student_list

    def __init__(self, school_name):
        self.school_name = school_name

    def create_course(self, course_name, course_city, course_cycle, course_price):
        self.course_dict[course_name] = {
            'city': course_city,
            'cycle': course_cycle,
            'price': course_price
        }
        for item in self.course_dict[course_name]:
            for key, value in item.items():
                print(key, ' --> ', value)

    def create_class(self, class_name):
        self.class_dict[class_name] = {
            'course': [],
            'student': [],
            'teacher': []
        }

    def enroll_student(self, student_name, class_name):
        self.class_dict[class_name]['student'].append(student_name)
        if not self.teacher_student_dict[self.class_dict[class_name]['teacher']]:
            self.teacher_student_dict[self.class_dict[class_name]['teacher']] = [student_name]
        else:
            self.teacher_student_dict[self.class_dict[class_name]['teacher']].append(student_name)

    def enroll_teacher(self, teacher_name, class_name):
        self.teacher_list.append(teacher_name)
        self.class_dict[class_name]['teacher'].append(teacher_name)
        self.teacher_class_dict[teacher_name] = [class_name]

    def add_class_for_teacher(self, teacher_name, class_name):
        self.teacher_class_dict[teacher_name].append(class_name)


class Student(School):

    student_dict = {}

    def __init__(self, student_name, school_name):
        super().__init__(school_name)
        self.student_name = student_name

    def init_student(self):
        self.student_dict[self.student_name] = {
            'class': None,
        }

    def show_class(self):
        class_dict = super().class_dict
        for class_name in class_dict:
            print(class_name)

    def select_class(self, class_name):
        super().enroll_student(self.student_name, class_name)
        for course in super().class_dict[class_name]['course']:
            print(course)


class Teacher(School, Student):

    def __init__(self, teacher_name, school_name):
        super().__init__(school_name)
        self.teacher_name = teacher_name

    def show_class(self):
        for class_name in super().teacher_class_dict[self.teacher_name]:
            print(class_name)

    def select_class(self, class_name):
        if class_name in super().teacher_class_dict[self.teacher_name]:
            class_dict = super().class_dict[class_name]
            for item in class_dict:
                print(item, ' --> ', class_dict[item])

    def set_score(self, student_name, score_item, score):
        student_object = Student(student_name, self.school_name)
        student_object.student_dict[score_item] = score

    def show_score(self):
        students = super().teacher_student_dict[self.teacher_name]
        for student in students:
            student_object = Student(student, self.school_name)
            print(student, ' --> ', student_object.student_dict['score'])






