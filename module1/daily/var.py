#/usr/bin/env python
#coding=utf8
#Author: itanony


name = input("name: ")
age = input("age: ")
job = input("job: ")
salary = input("salary: ")
info = '''
----- info of %s-----
Name : %s
Age : %s
Job : %s
Salary : %s
 ''' %(name,name,age,job,salary)

info2 = '''
------ info2 of {_name}-----
Name: {_name}
Age: {_age}
Job: {_job}
Salary: {_salary}
'''.format(_name=name,_age=age,_job=job,_salary=salary)
info3 = '''
------ info3 of {0}-----
Name: {0}
Age: {1}
Job: {2}
Salary: {3}
'''.format(name,age,job,salary)
print (info3)