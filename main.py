import re

problem = False

def error_Manager():
    print("Hay un error en el txt")
    global problem 
    problem = True
    
    
def shunting_yard(expression):

    output_queue=[]

    operator_stack=[]

    precedence={'+':1,'-':1,'*':2,'/':2}
    
    expression = re.findall(r"[+\-*/()\[\]]|\d*\.\d+|\d+|\w+|\,", expression)

    for token in enumerate(expression):
        
        if token[1].isalpha(): #es un nombre de funcion
            if token[1] in functions:
                argumentos = [expression[token[0]+j*2+2] for j in range(functions[token[1]]['args'])]
                output_queue.append(evaluate_function(token[1], *argumentos))
            else:
                print(f"La función {token[1]} no está definida.")
                error_Manager()
                return 0
                
        elif (token[1].isnumeric() or '.' in token[1]) and expression[token[0]-1] != ',' and expression[token[0]-1] != '[':
            output_queue.append(float(token[1]))

        elif token[1] in precedence:

            while (operator_stack and not operator_stack[-1]=='(' 
                and precedence[token[1]]<=precedence[operator_stack[-1]]):

                output_queue.append(operator_stack.pop())

            operator_stack.append(token[1])

        elif token[1]=='(':

            operator_stack.append(token[1])

        elif token[1]==')':

            while operator_stack and not operator_stack[-1]=='(':

                output_queue.append(operator_stack.pop())

            operator_stack.pop()

    while operator_stack:

        output_queue.append(operator_stack.pop())
        
    while len(output_queue) != 1:
        size = len(output_queue)
        i=0
        for j in range(size):
            if output_queue[i] in precedence:
                if output_queue[i]=='+':
                    a = output_queue[i-2]
                    b = output_queue[i-1]
                    output_queue[i-2] = a+b
                    i=i-2
                    output_queue.pop(i+1)                        
                    output_queue.pop(i+1)
                elif output_queue[i]=='-':
                    a = output_queue[i-2]
                    b = output_queue[i-1]
                    output_queue[i-2] = a-b
                    i=i-2
                    output_queue.pop(i+1)                        
                    output_queue.pop(i+1)
                elif output_queue[i]=='*':
                    a = output_queue[i-2]
                    b = output_queue[i-1]
                    output_queue[i-2] = a*b
                    i=i-2
                    output_queue.pop(i+1)                        
                    output_queue.pop(i+1)
                elif output_queue[i]=='/':
                    a = output_queue[i-2]
                    b = output_queue[i-1]
                    
                    if b==0:
                        print("Division por cero")
                        error_Manager()
                        return 0
                    else:
                        output_queue[i-2] = a/b
                        i=i-2
                        output_queue.pop(i+1)                        
                        output_queue.pop(i+1)
            i=i+1
    return output_queue[0]  
                    

def add_function(function_str,functions):
    
    #el formato de la funcion es f[c,d,...] = c+d*... 

    parts=function_str.split('=')

    if not len(parts)==2:

        print("Formato de función incorrecto. Debe ser 'nombre_funcion[parametros]=expresion'.")

        return

    func_name = parts[0].split('[')[0].strip()
    params = parts[0].split('[')[1].split(']')[0].strip()
    expression=parts[1].strip()

    params=params.split(',')

    num_params=len(params)
    
    for variable in params:
        if not variable.isalpha():
            print(f"Los parametros de la función deben ser letras en la funcion {func_name}.")
            error_Manager() 
            return 0
        if params.count(variable)>1:
            print(f"El parametro {variable} está repetido en la funcion {func_name}.")
            error_Manager()
            return 0
    # for variable in expression:
    #     if variable.isalpha() and variable not in params:
    #         print(f"La variable {variable} no está definida en los parametros de la funcion {func_name}.")
    #         error_Manager()
    #         return 0
    
        
    functions[func_name]={'args':num_params,'params':params,'expression':expression}

def evaluate_function(func_name,*args):
    if func_name not in functions:
        print(f"La función {func_name} no está definida.")
        error_Manager()
        return 0
    if not len(args)==functions[func_name]['args']:
        print(f"La función {func_name} requiere {functions[func_name]['args']} argumentos.")
        error_Manager()
        return 0
    #print(f"La función {func_name} con argumentos {args} es igual a {evaluate_expression(functions[func_name]['expression'],dict(zip(functions[func_name]['params'],args)))}")
    
    expression = functions[func_name]['expression']
    for i in range(len(args)):
        expression = expression.replace(functions[func_name]['params'][i],args[i])
    
    return shunting_yard(expression) 
    
functions={}

def main():
    
    global problem
    
    with open('operaciones.txt', 'r') as text:

        while True:

            #print("\n def: Añadir nueva función\n eval: Evaluar expresión\n fin Salir")
            
            for line in text:
                 #line=input("Selecciona una opción: ")
                if line.startswith("def:"):
                    function_str=line.split(":")[1]

                    add_function(function_str,functions)
                    
                    if not problem:
                        print("funcion agregada:\n")
                        print("\n")
                    else:
                        problem = False
                        continue
                    

                elif line.startswith("eval:"):

                    expression=line.split(":")[1]

                    result=shunting_yard(expression)
                    
                    if not problem:
                        print("Resultado:\n",result)
                    else:
                        problem = False
                        continue

                elif line.startswith("fin"):

                    break

                else:

                    print("Opción no válida. Inténtalo de nuevo.\n")
            

if __name__ == "__main__":

    main()
