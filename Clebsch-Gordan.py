#!/usr/bin/python

'''this file should be saved with a '.py' extension to work properly.'''

from easygui import *
import sys
from numarray import *

def factorial(n):
    if n == 1:
        return 1
    elif n == 0:
        return 1
#Technically, the factorial of a negative number is negative infinity, but this will do
#for our purposes.  
    elif n < 0:
        return -100000000000000.0
    else:
        return n * factorial(n-1)

while 1:
    msg ="Which Quantum numbers do you have?"
    title = "Choice of path"
    choices = ["j,m", "m1,m2"]
    choice = choicebox(msg, title, choices)
    if choice != None:
        pass
    else:
        sys.exit(0)
    
    if choice == "j,m":
        msg = "Enter your Quantum Numbers"
        title = "Clebsch-Gordan Coefficients"
        fieldNames = ["j1","j2","j","m"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multenterbox(msg,title, fieldNames)
        # make sure that none of the fields was left blank
        while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
            if errmsg == "": break # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    
        #Now we have to get the quantum numbers from the user as well as defining some variables
        
        j1=float(fieldValues[0])
        j2=float(fieldValues[1])
        j=float(fieldValues[2])
        m=float(fieldValues[3])
        z=0
        a=0.0
        b=0.0
        c=0.0
        l=""
        #First we have to politely catch the bad numbers
        if abs(m)>j:
            print "I'm sorry but |m| is greater than j"
        elif (j1+j2)<j:
            print "I'm sorry but j does not follow the triangle relationship."
        elif abs(j1-j2)>j:
            print "I'm sorry but j does not follow the triangle relationship."
        #MAIN PROGRAM where we actually compute the clebsch-gordan coefficients.
        else:
            for m1 in arange(-j1-1,(j1+1)):
            
                for m2 in arange(-j2-1,(j2+1)):
        #These are just some conditions which need to give zero.            
                    if (m1+m2) != m:
                        d=0
                    elif (j1-j2-m)%1!=0.0:
                        d=0
                    elif (j1-j2+m)%1!=0.0:
                        d=0
                    else:
                        c=0.0
                        z=0
        #This is the algorithm itself, Not very pretty, but that is what it is.             
                        a=((factorial(j1+j2-j)*factorial(j1-j2+j)*factorial(-j1+j2+j))/(factorial(j1+j2+j+1.0)))**.5
                        b=(factorial(j1+m1)*factorial(j1-m1)*factorial(j2+m2)*factorial(j2-m2)*factorial(j-m)*factorial(j+m))**.5
                        while z<(j1-m1+3):
            
                            c+=((-1.0)**(z+j1-j2+m))/(factorial(z)*factorial(j1+j2-j-z)*factorial(j1-m1-z)*factorial(j2+m2-z)*factorial(j-j2+m1+z)*factorial(j-j1-m2+z))
                            z+=1
                        d=((-1.0)**(j1-j2+m))*((2.0*j+1.0)**.5)*a*b*c
                        if abs(d)> .0001:
                            l+= "\n|"+str(m1)+str(m2)+">"+str(d)
        msgbox(l,"Coefficients")
    elif choice == "m1,m2":
        msg = "Enter your Quantum Numbers"
        title = "Clebsch-Gordan Coefficients"
        fieldNames = ["j1","j2","m1","m2"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multenterbox(msg,title, fieldNames)
        # make sure that none of the fields was left blank
        while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
            if errmsg == "": break # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    
        #Now we have to get the quantum numbers from the user as well as defining some variables
        j1=float(fieldValues[0])
        j2=float(fieldValues[1])
        m1=float(fieldValues[2])
        m2=float(fieldValues[3])
        z=0
        a=0.0
        b=0.0
        c=0.0
        l=""
        
        
        #MAIN PROGRAM where we actually calculate the coefficients
        for j in arange(abs(j1-j2)-1,(j1+j2)+1):
        
            for m in arange(-j-1,j+2):
            
        #First we define the values we know must be zero.       
                if abs(m)>j:
                    d=0
                elif (m1+m2)!= m:
                    d=0
                elif (j1-j2-m)%1!=0.0:
                    d=0
                elif (j1-j2+m)%1!=0.0:
                    d=0
                else:
                
                    c=0.0
                    z=0
        #Here is the algorithm itself, not pretty, but it does work.
                    a=((factorial(j1+j2-j)*factorial(j1-j2+j)*factorial(-j1+j2+j))/(factorial(j1+j2+j+1.0)))**.5
                    b=(factorial(j1+m1)*factorial(j1-m1)*factorial(j2+m2)*factorial(j2-m2)*factorial(j+m)*factorial(j-m))**.5
                    while z<(j1-m1+3):
            
                        c+=((-1.0)**(z+j1-j2+m))/(factorial(z)*factorial(j1+j2-j-z)*factorial(j1-m1-z)*factorial(j2+m2-z)*factorial(j-j2+m1+z)*factorial(j-j1-m2+z))
                        z+=1
                    d=(-1.0)**(j1-j2+m)*(2.0*j+1.0)**.5*a*b*c   
                    if abs(d)> .0001:
                        l+= "\n|"+str(j)+str(m)+">"+str(d)
        msgbox(l,"Coefficients")
