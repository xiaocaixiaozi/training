#!/usr/bin/env python
# coding=utf-8
# Author: bloke

import datetime
import sys
import re
import pickle
import os


class School(object):
    # 学校类
    school_dict = {}
    course_dict = {}    # 课程字典，记录课程的详细信息
    class_dict = {}     # 班级字典，记录班级的详细信息
    teacher_school_dict = {}    # 讲师字典，记录讲师和班级的对应关系
    student_school_dict = {}    # 学员字典，记录学员信息，包括是否支付费用
    course_class_dict = {}
    # member_list = teacher_school_dict.keys() + student_school_dict.keys()     # 学员和讲师的总人数

    def __init__(self, school_name):
        self.school_name = school_name
        self.school_address = ''
        if school_name not in self.school_dict:
            self.school_dict[school_name] = {'classes': [], 'courses': [], 'teachers': []}

    def create_course(self, course_name, course_outline, course_cycle, course_price, course_semester):
        """
        创建课程
        :param course_name: 名称
        :param course_outline: 大纲
        :param course_cycle: 周期
        :param course_price: 价格
        :param course_semester: 学期
        """
        self.course_dict[course_name] = {
            'cycle': course_cycle,
            'price': course_price,
            'outline': course_outline,
            'semester': course_semester
        }
        self.school_dict[self.school_name]['courses'].append(course_name)

    def create_class(self, class_name, class_course):
        """
        创建班级
        :param class_name: 名称
        :param class_course: 关联课程
        """
        self.class_dict[class_name] = {
            'course': class_course,
            'student': [],
            'teacher': [],
        }
        self.course_class_dict[class_course] = class_name
        self.school_dict[self.school_name]['classes'].append(class_name)

    def enroll_student(self, student_name, student_age, class_name):
        """
        注册学员
        :param student_name: 名字
        :param student_age: 年龄
        :param class_name: 关联班级
        """
        self.student_school_dict[student_name] = {'age': student_age, 'courses': [], 'classes': [class_name]}
        self.class_dict[class_name]['student'].append(student_name)

    def enroll_teacher(self, teacher_name, class_name):
        """
        注册讲师
        :param teacher_name: 名字
        :param class_name: 关联班级
        """
        self.class_dict[class_name]['teacher'].append(teacher_name)
        if teacher_name not in self.teacher_school_dict:
            self.teacher_school_dict[teacher_name] = [class_name]
        else:
            self.teacher_school_dict[teacher_name].append(class_name)

    def pay(self, student_name, course_name):
        """
        学员支付课程费用，支付成功，会修改pay值为True，默认为False
        :param student_name: 学员名字
        :param course_name: 课程名
        """
        price = self.course_dict[course_name]['price']
        print('[ %s ]课程费用为: %s' % (course_name, price))
        money = input('支付: ').strip()
        if money == price.strip('￥'):   # 去掉单位
            self.student_school_dict[student_name]['courses'].append(course_name)
            print('支付成功')
            self.student_school_dict[student_name]['class'] = self.course_class_dict[course_name]
            return True
        else:
            print('支付失败，金额不符')
            return False

    @staticmethod
    def view_school_info():
        print('校区：[', end=' ')
        for school in School.school_dict.keys():
            print(school, end=' ')
        else:
            print(']')


class Student(School):
    # 学员类，继承 School 类
    student_dict = {}

    def __init__(self, student_name):
        self.student_name = student_name
        if self.student_name not in self.student_dict:
            self.student_dict[self.student_name] = {}

    def student_enroll_student(self, school_name, class_name, student_age):
        """
        学员注册
        :param class_name:
        :param student_age:
        :return:
        """
        self.student_dict[self.student_name]['school_name'] = school_name
        self.student_dict[self.student_name]['class'] = [class_name]
        self.student_dict[self.student_name]['age'] = student_age
        lesson = super().course_dict[super().class_dict[class_name]['course']]['semester']
        self.student_dict[self.student_name][class_name] = {}
        self.student_dict[self.student_name][class_name][lesson] = {}
        super().enroll_student(self.student_name, student_age, class_name)

    def submite_homework(self, class_name, lesson, the_day, data):
        """
        提交作业
        :param class_name: 班级
        :param lesson: 学期
        :param the_day: 天数
        :param data: 作业
        """
        self.student_dict[self.student_name][class_name][lesson][the_day]['submite_date'] = datetime.datetime.now()
        self.student_dict[self.student_name][class_name][lesson][the_day]['submite_data'] = data

    def study_record(self, class_name, lesson, the_day):
        """
        学习记录，打卡
        :param class_name: 班级
        :param lesson: 学期
        :param the_day: 天数
        """
        if the_day not in self.student_dict[self.student_name][class_name][lesson]:
            self.student_dict[self.student_name][class_name][lesson][the_day] = {'punch': True}
        else:
            self.student_dict[self.student_name][class_name][lesson][the_day]['punch'] = True

    def show_teacher_name(self, class_name):
        """
        查看讲师信息
        :param class_name: 班级
        :return: 返回讲师姓名
        """
        teacher_name = super().class_dict[class_name]['teacher']
        return teacher_name

    def student_pay(self, school_name):
        """
        学员支付，调用父类的pay方法
        :param course_name:
        :return:
        """
        for course_name in super().school_dict[school_name]['courses']:
            print(course_name)
        for i in range(3):
            course_name = decide_input('选择课程')
            if course_name not in super().course_dict:
                print('未知课程.')
                continue
            else:
                break
        else:
            persistent()
            sys.exit('Exit.')
        super().pay(self.student_name, course_name)

    def view_score(self, class_name, lesson, the_day):
        """
        查看成绩，需要提供班级名，学期名
        :param class_name: 班级名
        :param lesson: 学期名
        :param the_day: 天数
        :return: 返回成绩 ['score']
        """
        return self.student_dict[self.student_name][class_name][lesson][the_day]['score']

    @staticmethod
    def select_course(school_name):
        """
        学员选择课程
        :param school_name: 校区名
        :return: 返回指定课程的信息，字典格式
        """
        course_dict = {}
        courses = School.school_dict[school_name]['courses']
        print('课程信息:[', end=' ')
        for num, course_n in enumerate(courses, 1):
            course_dict[str(num)] = course_n
            print(str(num), ':', course_n, end=' ')
        else:
            print(']')
        while 1:
            choice = input('选择课程["q"退出] :').strip()
            if choice == 'q':
                persistent()
                sys.exit('Exit.')
            if choice not in course_dict:
                continue
            else:
                break
        course_name = course_dict[choice]
        print('[ %s ]详细信息' % course_name)
        return course_name, School.course_dict[course_name]


class Teacher(Student, School):
    # 讲师类，继承 Student 和 School 类
    teacher_dict = {}

    def __init__(self, teacher_name):
        self.teacher_name = teacher_name

    def teacher_enroll_teacher(self, school_name, class_name):
        """
        教师注册
        :param class_name: 关联班级
        """
        self.teacher_dict[class_name] = {}
        lesson = super().course_dict[super().class_dict[class_name]['course']]['semester']
        self.teacher_dict[class_name][lesson] = {}
        super().enroll_teacher(self.teacher_name, class_name)
        super().school_dict[school_name]['teachers'].append(self.teacher_name)

    def class_record(self, lesson, class_name, the_day):
        """
        上课记录
        :param lesson: 学期
        :param class_name: 班级名
        :param the_day: 天数
        """
        self.teacher_dict[class_name][lesson][the_day] = {'start': True, 'date': datetime.datetime.now()}

    def set_score(self, class_name, lesson, student_name, the_day, score):
        """
        打成绩
        :param class_name: 班级名
        :param lesson: 学期名
        :param student_name: 学员名
        :param the_day: 天数
        :param score: 成绩
        """
        super().student_dict[student_name][class_name][lesson][the_day]['score'] = score

    def show_student_study_record(self, student_name):
        """
        查看学员学习记录
        :param student_name: 学员名
        :return: 返回学员信息
        """
        student_info = super().student_dict[student_name]
        return student_info

    def select_class(self):
        """
        选择班级
        :return: 返回班级名
        """
        for class_name in super().teacher_school_dict[self.teacher_name]:
            return class_name


def decide_iter(the_iter, sign, warn_msg='', error_msg='Exit.', choice=False):
    num = 0
    while num < 3:
        value = decide_input(sign)
        if choice:
            if value in the_iter:
                num += 1
                if warn_msg:
                    print(warn_msg)
                continue
            else:
                return value
        elif value not in the_iter:
            num += 1
            if warn_msg:
                print(warn_msg)
            continue
        else:
            return value
    else:
        persistent()
        sys.exit(error_msg)


def decide_input(sign):
    key_num = 0
    while key_num < 3:
        value = input(sign + ': ').strip()
        if not value:
            key_num += 1
            continue
        elif value == 'q':
            persistent()
            sys.exit('Exit')
        else:
            return value
    else:
        persistent()
        sys.exit('Exit.')


def student_member():
    """
    成员类型为学员时，分为 注册 和 登陆 两种
    """
    choice_dict = {'1': '免费注册', '2': '立即登陆'}
    for choice_key, choice_value in choice_dict.items():
        print(choice_key, ': ', choice_value)
    choice = decide_iter(choice_dict, '选择 [q退出]')
    if choice == '1':
        student_enroll()
    elif choice == '2':
        name = decide_input('姓名')
        student_login(name, Student.student_dict[name]['school_name'])


def student_enroll():
    """
    学员注册接口，需要学员提供 姓名、年龄、选择校区、选择课程，最后缴纳学费，如果中间一项失败，则退出程序；
    如果全部通过，则询问是否立即学习，调用学员登陆接口 [student_login]
    """
    name = decide_input('姓名')
    age = decide_input('年龄')
    School.view_school_info()
    school = decide_iter(School.school_dict, '选择学校[q退出]', '未知校区', '未知校区')
    course_name, course_info = Student.select_course(school)
    for course_key, course_value in course_info.items():
        print(course_key, ':', course_value)
    course_choice = decide_input('确认 [y/n]')
    if course_choice.lower() != 'y':
        persistent()
        sys.exit('Exit.')
    price = decide_input('缴纳学费[ %s ]' % course_info['price'])
    if price != course_info['price'].strip('￥'):
        persistent()
        sys.exit('支付金额不符，退出.')
    student = Student(name)
    student.student_enroll_student(school, School.course_class_dict[course_name], age)
    student.student_dict[name]['class'] = School.course_class_dict[course_name]
    study_choice = decide_input('是否立即学习[y/n]')
    if study_choice != 'y':
        persistent()
        sys.exit('Exit.')
    else:
        student_login(name, school)


def student_login(name, school):
    """
    学员登陆接口,此接口提供功能：[购买课程、查询课程、上课打卡、提交作业、查看成绩]
    :param name: 学员名
    """
    if name not in Student.student_dict:
        persistent()
        print('未知学员.')
        sys.exit()
    student = Student(name)
    classes = student.student_dict[name]['class']
    interface_dict = {'1': '购买课程', '2': '查询课程', \
                      '3': '上课打卡', '4': '提交作业', '5': '查看成绩'}
    while 1:
        for key, value in interface_dict.items():
            print(key, ':', value)
        interface_choice = decide_iter(interface_dict, '选择操作项[q退出]', '无效选项')
        if interface_choice == '1':
            student.student_pay(school)
            continue
        if interface_choice == '2':
            course_name, course_info = student.select_course(school)
            for key, value in course_info.items():
                print(key, ':', value)
            continue
        print('已报班级:', student.student_dict[name]['class'])
        class_name = decide_iter(classes, '选择班级', '输入错误')
        lesson_name = Teacher.course_dict[Teacher.class_dict[class_name]['course']]['semester']
        if interface_choice == '3':
            print([x for x in Teacher.teacher_dict[class_name][lesson_name].keys()])
            day = decide_iter(Teacher.teacher_dict[class_name][lesson_name], '打卡课时[q退出]', '无效课时')
            student.study_record(class_name, lesson_name, day)
            continue
        if interface_choice == '4':
            print([x for x in Teacher.teacher_dict[class_name][lesson_name].keys()])
            try:
                day = decide_iter(Teacher.teacher_dict[class_name][lesson_name], '提交课时[q退出]', '无效课时')
                data = decide_input('作业')
            except SystemExit:
                continue
            student.submite_homework(class_name, lesson_name, day, data)
        if interface_choice == '5':
            print([x for x in Teacher.teacher_dict[class_name][lesson_name].keys()])
            try:
                day = decide_iter(Teacher.teacher_dict[class_name][lesson_name], '查询课时[q退出]', '无效课时')
            except SystemExit:
                continue
            try:
                print(student.view_score(class_name, lesson_name, day))
            except KeyError as e:
                print('讲师未批改')
                continue


def teacher_login():
    """
    讲师登陆接口，此接口提供功能：[上课、查看学员名单、批改成绩]
    """
    name = decide_iter(School.teacher_school_dict, '姓名[q退出]', '讲师不存在')
    teacher = Teacher(name)
    sub_interface_dict = {'1': '上课', '2': '查看学员名单', '3': '批改成绩'}
    while 1:
        print('管辖班级： ', [x for x in School.teacher_school_dict[name]])
        top_choice = decide_iter(School.teacher_school_dict[name], '选择班级[q退出]', '班级不存在')
        for key, value in sub_interface_dict.items():
            print(key, ': ', value)
        inter = decide_iter(sub_interface_dict, '选择工作项[q退出]', '无效项')
        class_name = top_choice
        course_name = teacher.class_dict[class_name]['course']
        lesson_name = teacher.course_dict[course_name]['semester']
        if inter == '1':    # 上课
            day_num = 0
            while day_num < 3:
                day = decide_input('课时 [格式：day+天数, 例如day01]')
                if not re.findall(r'day\d{1,3}', day):
                    print('非法课时名称')
                    day_num += 1
                    continue
                else:
                    break
            else:
                persistent()
                sys.exit('Exit.')
            teacher.class_record(lesson_name, class_name, day)
            continue
        if inter == '2':    # 查看学员名单
            print(teacher.class_dict[class_name]['student'])
            continue
        if inter == '3':    # 批改作业
            print('学员列表:', teacher.class_dict[class_name]['student'])
            student_name = decide_iter(teacher.class_dict[class_name]['student'], '学员名[q退出]', '学员不存在')
            lesson_name = teacher.course_dict[course_name]['semester']
            print('课时列表:', [x for x in teacher.teacher_dict[class_name][lesson_name].keys()])
            day = decide_iter(teacher.teacher_dict[class_name][lesson_name], '学期[q退出]', '无效学期')
            score = decide_input('成绩')
            teacher.set_score(class_name, lesson_name, student_name, day, score)
            continue


def manager():
    """
    管理员接口，提供功能：[创建课程、班级、讲师]
    """
    print('已存在校区:', [x for x in School.school_dict.keys()])
    school_name = decide_input('请输入要管理的校区名')
    interface_dict = {'1': '创建课程', '2': '创建班级', '3': '增添讲师'}
    for key, value in interface_dict.items():
        print(key, ': ', value)
    manager_inter = decide_iter(interface_dict, '选择功能[q退出]', '输入错误')
    school = School(school_name)
    if manager_inter == '1':    # 创建课程
        print('已有课程列表:', school.school_dict[school_name]['courses'])
        course_name = decide_iter(school.school_dict[school_name]['courses'], \
                                  '创建课程名称[q退出]', '课程已存在', choice=True)
        course_outline = decide_input('课程大纲')
        course_cycle = decide_input('课程周期')
        course_price = decide_input('课程价格')
        course_semester = decide_input('学期')
        school.create_course(course_name, course_outline, course_cycle, course_price, course_semester)
    elif manager_inter == '2':    # 创建班级
        print('已有班级列表:', school.school_dict[school_name]['classes'])
        class_name = decide_iter(school.school_dict[school_name]['classes'], '班级名称[q退出]', '班级已存在', choice=True)
        print('课程列表:', school.school_dict[school_name]['courses'])
        course_name = decide_iter(school.school_dict[school_name]['courses'], '关联课程名称[q退出]', '未知课程')
        school.create_class(class_name, course_name)
    elif manager_inter == '3':
        print('在职教师:', school.school_dict[school_name]['teachers'])
        teacher_name = decide_input('教师名称')
        print('班级列表:', school.school_dict[school_name]['classes'])
        class_name = decide_iter(school.school_dict[school_name]['classes'], '关联班级名称[q退出]', '未知班级')
        Teacher(teacher_name).teacher_enroll_teacher(school_name, class_name)


def persistent(the_file='config'):
    """
    持久化
    :param the_file: 写入的文件名
    """
    input_data = [School.school_dict, School.course_dict, School.class_dict, School.teacher_school_dict, \
            School.student_school_dict, School.course_class_dict, Student.student_dict, Teacher.teacher_dict]
    with open(the_file, 'wb') as f:
        pickle.dump(input_data, f)


if __name__ == '__main__':
    config_file = 'config'
    if os.path.exists(config_file):
        with open(config_file, 'rb') as f:
            data = pickle.load(f)
            School.school_dict, School.course_dict, School.class_dict, School.teacher_school_dict, \
            School.student_school_dict, School.course_class_dict, Student.student_dict, \
            Teacher.teacher_dict= data
    func_dict = {'Student': student_member, 'Teacher': teacher_login, 'Manager': manager}   # 视图
    member_dict = {'1': 'Student', '2': 'Teacher', '3': 'Manager'}
    print('成员类型:')
    for key, value in member_dict.items():
        print(key, ': ', value)
    member_choice = decide_iter(member_dict, '选择成员类型[q退出]')
    member = member_dict[member_choice]
    while 1:
        try:
            func_dict[member]()
        except KeyError as e:
            print('Error:', e)
            continue
        # except:
        #     persistent()
        #     sys.exit('Exit.')
        print('操作完成'.center(50, '-'))

        # School.school_list
        # School.course_dict    # 课程字典，记录课程的详细信息
        # School.class_dict     # 班级字典，记录班级的详细信息
        # School.teacher_school_dict    # 讲师字典，记录讲师和班级的对应关系
        # School.student_school_dict    # 学员字典，记录学员信息，包括是否支付费用
        # School.course_class_dict      # 课程与班级对应字典
        # Student.student_dict          # 学员字典，包含学员详细信息
        # Teacher.teacher_dict          # 讲师字典，包含讲师详细信息

