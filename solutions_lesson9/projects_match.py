#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 22:52:35 2019

@author: gioel
"""
from random import choice

students = []
projects = []


question = int(input('How many students do you want to add?'))

i = 0
while i < question:
    a = input('insert the name of the student')
    students.append(a)
    i += 1

question2 = int(input('How many projects do you want to add?'))

j = 0 
while j < question2:
    b = input('insert the name of the project')
    projects.append(b)
    j += 1

match = {}

for k in range(question):
    if question2 < question:
        mydict = {students[k]:choice(projects)}
        match.update(mydict)
    else:
        x = choice(projects)
        mydict = {students[k]:x}
        projects.remove(x)
        match.update(mydict) 
print(match)