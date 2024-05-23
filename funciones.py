import re

def proxima():
    print("proxima() Not implemented yet")
    
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
                proxima()
                
        elif token[1].isnumeric() and expression[token[0]-1] != ',' and expression[token[0]-1] != '[':
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
                        proxima()
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
            proxima() 
        if params.count(variable)>1:
            print(f"El parametro {variable} está repetido en la funcion {func_name}.")
            proxima()
    for variable in expression:
        if variable.isalpha() and variable not in params:
            print(f"La variable {variable} no está definida en los parametros de la funcion {func_name}.")
            proxima()
        
    functions[func_name]={'args':num_params,'params':params,'expression':expression}

def evaluate_function(func_name,*args):
    if func_name not in functions:
        print(f"La función {func_name} no está definida.")
        proxima()
    if not len(args)==functions[func_name]['args']:
        print(f"La función {func_name} requiere {functions[func_name]['args']} argumentos.")
        proxima()
    #print(f"La función {func_name} con argumentos {args} es igual a {evaluate_expression(functions[func_name]['expression'],dict(zip(functions[func_name]['params'],args)))}")
    
    expression = functions[func_name]['expression']
    for i in range(len(args)):
        expression = expression.replace(functions[func_name]['params'][i],args[i])
        
    return shunting_yard(expression) 
    
functions={}

def main():

    while True:

        print("\n1. Añadir nueva función\n3. Evaluar expresión\n4. Salir")

        choice=input("Selecciona una opción: ")

        if choice=="1":

            function_str=input("Introduce la nueva función: ")

            add_function(function_str,functions)

        elif choice=="3":

            expression=input("Introduce la expresión a evaluar: ")

            result=shunting_yard(expression)

            print("Resultado:",result)

        elif choice=="4":

            break

        else:

            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":

    main()
