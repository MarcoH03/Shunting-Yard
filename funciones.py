import re

def proxima():
    print("proxima() Not implemented yet")
    
def shunting_yard(expression):

    output_queue=[]

    operator_stack=[]

    precedence={'+':1,'-':1,'*':2,'/':2}
    
    expression = re.findall(r"[+\-*/()\[\]]|\d*\.\d+|\d+|\w+", expression)

    for token in enumerate(expression):
        
        if token[1].isalpha(): #es un nombre de funcion
            if token[1] in functions:
                argumentos = [expression[token[0]+j+2] for j in range(functions[token[1]]['args'])]
                output_queue.append(evaluate_function(token[1], *argumentos))
            else:
                print(f"La función {token[1]} no está definida.")
                proxima()
                
        elif token[1].isnumeric():
            output_queue.append(float(token[1]))

        elif token in precedence:

            while (operator_stack and not operator_stack[-1]=='(' 
                and precedence[token]<=precedence[operator_stack[-1]]):

                output_queue.append(operator_stack.pop())

            operator_stack.append(token)

        elif token=='(':

            operator_stack.append(token)

        elif token==')':

            while operator_stack and not operator_stack[-1]=='(':

                output_queue.append(operator_stack.pop())

            operator_stack.pop()

    while operator_stack:

        output_queue.append(operator_stack.pop())

    return output_queue

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
    pass
    # if func_name not in functions:
    #     print(f"La función {func_name} no está definida.")
    #     proxima()
    # if not len(args)==functions[func_name]['args']:
    #     print(f"La función {func_name} requiere {functions[func_name]['args']} argumentos.")
    #     proxima()
    # print(f"La función {func_name} con argumentos {args} es igual a {evaluate_expression(functions[func_name]['expression'],dict(zip(functions[func_name]['params'],args)))}")

functions = {}
