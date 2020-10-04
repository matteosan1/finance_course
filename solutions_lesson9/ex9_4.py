import math
from datetime import date
from dateutil.relativedelta import relativedelta
import finmarkets
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

number_of_projects = 5
number_of_students = 20

projects=[]
students=[]
i=1
while i <= number_of_projects:
    projects.append('p'+str(i))
    i+=1
print(number_of_projects,' projects: ', projects)

i=1
while i <= number_of_students:
    students.append('s'+str(i))
    i+=1
print(number_of_students,' students: ', students)

from random import randint
i=0
project_to_student = []
while i < len(students):
    n_random = randint(0,len(projects)-1)
    project_to_student.append(students[i]+'<=='+projects[n_random])
    i+=1
print('project_to_student: ', project_to_student)
