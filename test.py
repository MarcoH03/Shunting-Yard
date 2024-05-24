#create a program to generate random functions to test the calculator

import random

if __name__ == "__main__":
        
    names = ["f","g","h","i","j"]
    parameters = ["x","y","z","w","v"]

    with open('operaciones.txt', 'w') as text:
        for i in range(5):
            text.write("def:")
            text.write(names[i])
            text.write("[")
            for j in range(5):
                text.write(parameters[j])
                if j< 5-1:
                    text.write(",")
            text.write("]=")
            for j in range(5):
                text.write(parameters[j])
                if j<5-1:
                    text.write(random.choice(["+","-","*","/"]))
            text.write("\n")   
        
        for i in range(5):
            text.write("eval:")
            text.write(names[i])
            text.write("[")
            for j in range(5):
                text.write(str(random.randint(0,9)))
                if j< 5-1:
                    text.write(",")
            text.write("]\n")  
            
        text.write("fin")
        
