import numpy as np
from finmarkets import call

s = 800
moneyness = [0.5, 0.75, 0.825, 1.0, 1.125, 1.25, 1.5]
vol = 0.3
ttm = "9m"
r = 0.005

result = {}
for m in moneyness:
    result[s*m] = call(s, m*s, r, vol, ttm)
print (result)







from math import pi

class Circle:
    def __init__(self, radius):
        self.radius = radius
        
    def area(self):
        return pi*self.radius**2
    
class Rectangle:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        
    def area(self):
        return self.width*self.height
    
    def perimeter(self):
        return self.width*2 + self.height*2
    
circle = Circle(5)
print ("My circle area is {:.1f} m**2".format(circle.area()))
rect = Rectangle(3, 6)
print ("My rect area is {:.1f} m**2 and the perimeter is {} m".format(rect.area(), rect.perimeter()))




class Menu:
    def __init__(self):
        self.dishes = {'1':("Spaghetti", 6.50),
                       '2':("Pizza", 7.00),
                       '3':("Sparkling Water", 0.50),
                       '4':("Red Wine 0.5l", 5.00)}
        self.current_choice = {}
        
    def clear_order(self):
        self.current_choice = {}
        
    def add_dish(self, dish_id, quantity = 1):
        if dish_id not in self.dishes.keys():
            print ("Dish {} currently not availble.".format(dish_id))
        else:
            self.current_choice[dish_id] = self.current_choice.setdefault(dish_id, 0) + quantity
            
    def remove_dish(self, dish_id, quantity = 1):
        if dish_id in self.current_choice.keys():
            self.current_choice[dish_id] = max(0, self.current_choice[dish_id] - quantity)
            
    def bill(self):
        cost = 0
        for id, qty in self.current_choice.items():
            cost += self.dishes[id][1] * qty
        print ("{:15} {:2} {:>6.2f}".format(self.dishes[id][0],
                                            qty,
                                            self.dishes[id][1]))
        
        print ("{:15} {:>6.2f}".format("Tot:", cost))
        
m = Menu()
m.add_dish('1')
m.add_dish('2')
m.add_dish('3')
m.bill()





from math import sqrt

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def distanceTo(self, x, y):
        dist = sqrt((self.x-x)**2 + (self.y-y)**2)
        return dist
    
    def distanceTo_v2(self, p):
        dist = sqrt((self.x-p[0])**2 + (self.y-p[1])**2)
        return dist
    
    def distanceTo_v3(self, p):
        dist = sqrt((self.x-p.x)**2 + (self.y-p.y)**2)
        return dist
    
point = Point2D(4, 5)
p0 = (0, 0)
point0 = Point2D(0, 0)
print ("distance to p0: {:.2f}".format(point.distanceTo(p0[0], p0[1])))
print ("distance_v2 to p0: {:.2f}".format(point.distanceTo_v2(p0)))
print ("distance_v3 to p0: {:.2f}".format(point.distanceTo_v3(point0)))

p1 = (3, 4)
point1 = Point2D(3, 4)
print ("distance to p1: {:.2f}".format(point.distanceTo(p1[0], p1[1])))
print ("distance_v to p1: {:.2f}".format(point.distanceTo_v2(p1)))
print ("distance_v3 to p1: {:.2f}".format(point.distanceTo_v3(point1)))



from datetime import date

class Person:
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday
        self.employment = None
        
    def age(self, d=date.today()):
        age = (d-self.birthday).days/365
        print ("{} is {:.0f} years old".format(self.name, age))
        
    def mainOccupation(self, occupation):
        self.employment = occupation
        print ("{}'s main occupation is: {}".format(self.name, self.employment))
        
class Student(Person):
    def __init__(self, name, birthday, school):
        Person.__init__(self, name, birthday)
        self.grade = school
        self.votes = {}
        
    def addVote(self, subject, vote):
        self.votes[subject] = vote
        
    def average(self):
        print ("List of votes")
        print ("−−−−−−−−−−−−−")
        for k, v in self.votes.items():
            print ("{}: {}".format(k, v))
        avg = sum(self.votes.values())/len(self.votes)
        print ("−−−−−−−−−−−−−")
        print ("Avg: {:.1f}".format(avg))
        
student = Student("Mario", date(1980, 5, 6), "Liceo Scientifico G. Galilei")
student.addVote("Calculus", 8)
student.addVote("Literature", 5.5)
student.addVote("Latin", 6.5)
student.average()
