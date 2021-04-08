import A as a
import B as b
import C as c

typeOfImplementation = input("Please enter A, B or C for the type of implementation: ")

if typeOfImplementation == 'A':
    a.implementationA()
elif typeOfImplementation == 'B':
    b.implementationB()
elif typeOfImplementation == 'C':
    c.implementationC()
else:
    print("Wrong implementation!")