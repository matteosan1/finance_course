from scipy.optimize import fsolve
import math

m = 0.02  #Initial Guess

a2 = 100/(1+0.04991*0.25)**2
a3 = 100/(1+0.05030*0.25)**3
a4 = 100/(1+0.05126*0.25)**4
a5 = 100/(1+0.05166*0.25)**5
a6 = 100/(1+0.05207*0.25)**6


def HoLee(m):
    ru = (0.04969 + m*0.25  + 0.005*math.sqrt(0.25))
    rd = (0.04969 + m*0.25  - 0.005*math.sqrt(0.25))
    N1 = 100/(1+ru*0.25) #FV value of bond is 100 at maturity
    N2 = 100/(1+rd*0.25)
    return((0.5*N1 + 0.5*N2)/(1+0.04969*0.25) - a2)
    
mo = fsolve(HoLee,m)
print (mo[0])

ru = (0.04969 + mo*0.25  + 0.005*math.sqrt(0.25))
rd = (0.04969 + mo*0.25  - 0.005*math.sqrt(0.25))

print([ru,rd])

m = 0.02

def HoLee2(m):
    ruu = (0.04969 + (mo[0] + m)*0.25  + 2 *0.005*math.sqrt(0.25))
    rud = (0.04969 + (mo[0] + m)*0.25) 
    rdd = (0.04969 + (mo[0] + m)*0.25  - 2*0.005*math.sqrt(0.25))
  
    N1 = 100/(1+ruu*0.25) 
    N2 = 100/(1+rud*0.25)
    N3 = 100/(1+rdd*0.25)
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ru[0]*0.25)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + rd[0]*0.25)
  
    return((0.5*ans1 + 0.5*ans2)/(1+0.04969*0.25) - a3)

m1 = fsolve(HoLee2,m)
print (m1)


ruu = (0.04969 + (mo[0] + m1[0])*0.25  + 2 *0.005*math.sqrt(0.25))
rud = (0.04969 + (mo[0] + m1[0])*0.25) 
rdd = (0.04969 + (mo[0] + m1[0])*0.25  - 2*0.005*math.sqrt(0.25))

print ([ruu,rud,rdd])

def HoLee3(m):
    ruuu = (0.04969 + (mo[0] + m1[0]+m)*0.25  + 3 * 0.005*math.sqrt(0.25))
    ruud = (0.04969 + (mo[0] + m1[0]+m)*0.25  + 1 * 0.005*math.sqrt(0.25))
    rdud = (0.04969 + (mo[0] + m1[0]+m)*0.25  - 1 * 0.005*math.sqrt(0.25))
    rddd = (0.04969 + (mo[0] + m1[0]+m)*0.25  - 3 * 0.005*math.sqrt(0.25))
  
    N1 = 100/(1+ruuu*0.25) 
    N2 = 100/(1+ruud*0.25)
    N3 = 100/(1+rdud*0.25)
    N4 = 100/(1+rddd*0.25)
    
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ruu*0.25)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + rud*0.25)
    ans3 = ((0.5*N3 + 0.5*N4))/(1 + rdd*0.25)
    
    fans1 = ((0.5*ans1 + 0.5*ans2))/(1 + ru*0.25)
    fans2 = ((0.5*ans2 + 0.5*ans3))/(1 + rd*0.25)
    
    return((0.5*fans1 + 0.5*fans2)/(1+0.04969*0.25) - a4)

m2 = fsolve(HoLee3,m)
print (m2)

ruuu = (0.04969 + (mo[0] + m1[0]+m2[0])*0.25  + 3 * 0.005*math.sqrt(0.25))
ruud = (0.04969 + (mo[0] + m1[0]+m2[0])*0.25  + 1 * 0.005*math.sqrt(0.25))
rdud = (0.04969 + (mo[0] + m1[0]+m2[0])*0.25  - 1 * 0.005*math.sqrt(0.25))
rddd = (0.04969 + (mo[0] + m1[0]+m2[0])*0.25  - 3 * 0.005*math.sqrt(0.25))

print ([ruuu,ruud,rdud,rddd])

def HoLee4(m):
    ruuuu = (0.04969 + (mo[0] + m1[0]+ m2[0] + m)*0.25 + 4 * 0.005*math.sqrt(0.25))
    ruuud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m)*0.25  + 2 * 0.005*math.sqrt(0.25))
    rudud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m)*0.25  - 0 * 0.005*math.sqrt(0.25))
    ruddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m)*0.25  - 2 * 0.005*math.sqrt(0.25))
    rdddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m)*0.25  - 4 * 0.005*math.sqrt(0.25))
  
    N1 = 100/(1+ruuuu*0.25) 
    N2 = 100/(1+ruuud*0.25)
    N3 = 100/(1+rudud*0.25)
    N4 = 100/(1+ruddd*0.25)
    N5 = 100/(1+rdddd*0.25)
    
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ruuu*0.25)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + ruud*0.25)
    ans3 = ((0.5*N3 + 0.5*N4))/(1 + rdud*0.25)
    ans4 = ((0.5*N4 + 0.5*N5))/(1 + rddd*0.25)
    
    fans1 = ((0.5*ans1 + 0.5*ans2))/(1 + ruu*0.25)
    fans2 = ((0.5*ans2 + 0.5*ans3))/(1 + rud*0.25)
    fans3 = ((0.5*ans3 + 0.5*ans4))/(1 + rdd*0.25)
    
    xans1 = ((0.5*fans1 + 0.5*fans2))/(1 + ru*0.25)
    xans2 = ((0.5*fans2 + 0.5*fans3))/(1 + rd*0.25)
    
    return((0.5*xans1 + 0.5*xans2)/(1+0.04969*0.25) - a5)

m3 = fsolve(HoLee4,m)
print (m3)

ruuuu = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0])*0.25 + 4 * 0.005*math.sqrt(0.25))
ruuud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0])*0.25  + 2 * 0.005*math.sqrt(0.25))
rudud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0])*0.25  - 0 * 0.005*math.sqrt(0.25))
ruddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0])*0.25  - 2 * 0.005*math.sqrt(0.25))
rdddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0])*0.25  - 4 * 0.005*math.sqrt(0.25))


print([ruuuu,ruuud,rudud,ruddd,rdddd])


def HoLee5(m):
    ruuuuu = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25 + 5 * 0.005*math.sqrt(0.25))
    ruuuud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25  + 3 * 0.005*math.sqrt(0.25))
    ruuudd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25  + 1 * 0.005*math.sqrt(0.25))
    ruuddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25  - 1 * 0.005*math.sqrt(0.25))
    rudddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25  - 3 * 0.005*math.sqrt(0.25))
    rddddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25  - 5 * 0.005*math.sqrt(0.25))
  
    N1 = 100/(1+ruuuuu*0.25) 
    N2 = 100/(1+ruuuud*0.25)
    N3 = 100/(1+ruuudd*0.25)
    N4 = 100/(1+ruuddd*0.25)
    N5 = 100/(1+rudddd*0.25)
    N6 = 100/(1+rddddd*0.25)
    
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ruuuu*0.25)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + ruuud*0.25)
    ans3 = ((0.5*N3 + 0.5*N4))/(1 + rudud*0.25)
    ans4 = ((0.5*N4 + 0.5*N5))/(1 + ruddd*0.25)
    ans5 = ((0.5*N5 + 0.5*N6))/(1 + rdddd*0.25)
    
    fans1 = ((0.5*ans1 + 0.5*ans2))/(1 + ruuu*0.25)
    fans2 = ((0.5*ans2 + 0.5*ans3))/(1 + ruud*0.25)
    fans3 = ((0.5*ans3 + 0.5*ans4))/(1 + rdud*0.25)
    fans4 = ((0.5*ans4 + 0.5*ans5))/(1 + rddd*0.25)
    
    xans1 = ((0.5*fans1 + 0.5*fans2))/(1 + ruu*0.25)
    xans2 = ((0.5*fans2 + 0.5*fans3))/(1 + rud*0.25)
    xans3 = ((0.5*fans3 + 0.5*fans4))/(1 + rdd*0.25)
    
    yans1 = ((0.5*xans1 + 0.5*xans2))/(1 + ru*0.25)
    yans2 = ((0.5*xans2 + 0.5*xans3))/(1 + rd*0.25)
    
    return((0.5*yans1 + 0.5*yans2)/(1+0.04969*0.25) - a6)

m4 = fsolve(HoLee5,m)
print (m4)

ruuuuu = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25 + 5 * 0.005*math.sqrt(0.25))
ruuuud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25  + 3 * 0.005*math.sqrt(0.25))
ruuudd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25  + 1 * 0.005*math.sqrt(0.25))
ruuddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25  - 1 * 0.005*math.sqrt(0.25))
rudddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25  - 3 * 0.005*mat.sqrt(0.25))
rddddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25  - 5 * 0.005*math.sqrt(0.25))


print([ruuuuu,ruuuud,ruuudd,ruuddd,rudddd,rddddd])
