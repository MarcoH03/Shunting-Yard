import re

# La función shunting_yard implementará el algoritmo Shunting Yard para convertir la expresión matemática
# en notación postfija, lo que facilitará su evaluación.

# La función evaluate_expression tomará la expresión matemática y las funciones definidas por el usuario, 
# y evaluará la expresión utilizando las funciones disponibles.

# La función add_function permitirá al usuario introducir una nueva función y la almacenará para su uso 
# posterior.

# La función main presentará un menú al usuario para que pueda seleccionar entre añadir una nueva función 
# o evaluar una expresión. Dependiendo de la opción seleccionada, se invocarán las funciones correspondientes.

def shunting_yard(expression):

    # Básicamente, el funcionamiento general de este algoritmo es el siguiente:

    # Se recorre la expresión matemática token por token.

    # Si el token es un número o una variable, se agrega directamente a la cola de salida.

    # Si el token es un operador, se compara su precedencia con los operadores en la pila. Si la precedencia 
    # es menor o igual, se van sacando operadores de la pila y se agregan a la cola de salida hasta que se 
    # cumpla la condición.

    # Si el token es un paréntesis de apertura, se agrega a la pila.

    # Si el token es un paréntesis de cierre, se van sacando operadores de la pila y se agregan a la cola 
    # de salida hasta encontrar el paréntesis de apertura correspondiente.

    # Al finalizar el recorrido, se vacía la pila y se agregan los operadores restantes a la cola de salida.
    # La cola de salida contiene la expresión en notación postfija.

    output_queue=[]

    operator_stack=[]

    precedence={'+':1,'-':1,'*':2,'/':2}

    for token in re.findall(r"[+\-*/()]|\w+",expression):

        if token.isalnum():

            output_queue.append(token)

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

# Una vez obtenida la expresión en notación postfija, el siguiente algoritmo evalúa dicha expresión y 
# devuelve el resultado numérico.

def evaluate_expression(expression,functions):

    # El funcionamiento general es el siguiente:

    # Se recorre la expresión postfija token por token.

    # Si el token es un número, se agrega a una pila.

    # Si el token es un operador, se extraen los operandos de la pila, se realiza la operación correspondiente 
    # y se agrega el resultado a la pila.

    # Si el token es una función definida por el usuario, se extraen los argumentos necesarios de la pila, 
    # se llama a la función con los argumentos y se agrega el resultado a la pila.

    # Al finalizar el recorrido, el resultado final estará en la cima de la pila y se devuelve como resultado 
    # de la evaluación.

    def evaluate_postfix(postfix):

        stack=[]

        for token in enumerate(postfix):
            
            if token[1].isnumeric():

                stack.append(float(token[1]))

            elif token[1] in functions:

                args=[postfix[token[0]+1+j] for j in range(functions[token[1]]['args'])]

                result=functions[token[1]]['func'](*args)

                stack.append(result)

            else:

                b=stack.pop()
                a=stack.pop()

                if token[1]=='+':

                    stack.append(a+b)

                elif token[1]=='-':

                    stack.append(a-b)

                elif token[1]=='*':

                    stack.append(a*b)

                elif token[1]=='/':

                    if b==0:

                        raise ZeroDivisionError("Division by zero")
                    
                    stack.append(a/b)
        
        if not len(stack)==1:

            raise ValueError("Invalid expression")

        return stack[0]

    postfix_expression=shunting_yard(expression)

    for token in postfix_expression:

        if token not in functions and not token.isalnum() and token not in ['+','-','*','/']:
            
            raise ValueError(f"Undefined token '{token}' in expression")

    result=evaluate_postfix(postfix_expression)

    return result

# El siguiente algoritmo permite al usuario agregar nuevas funciones al programa para su posterior uso en 
# las expresiones matemáticas.

def add_function(function_str,functions):

    # Funcionamiento general:

    # Se recibe una cadena que representa la definición de una nueva función en formato 
    # 'nombre_funcion=parametros:expresion'.

    # Se separa el nombre de la función, los parámetros y la expresión.

    # Se crea una función anónima que toma los argumentos necesarios, evalúa la expresión con esos 
    # argumentos y devuelve el resultado.

    # Se agrega esta nueva función al diccionario de funciones definidas por el usuario para que pueda ser 
    # utilizada en las evaluaciones de expresiones.

    parts=function_str.split('=')

    if not len(parts)==2:

        print("Formato de función incorrecto. Debe ser 'nombre_funcion=parametros:expresion'.")

        return

    func_name,signature=parts[0].strip(),parts[1].strip()

    params,expression=signature.split(':')

    params=params.split(',')

    num_params=len(params)

    def func_to_call(*args):

        if not len(args)==num_params:

            raise ValueError(f"La función {func_name} requiere {num_params} argumentos.")
        
        return evaluate_expression(expression,dict(zip(params,args)))

    functions[func_name]={'args':num_params,'func':func_to_call}

# A continuación en el main mostramos el menú de opciones al usuario y ponemos todo el programa en 
# funcionamiento

def main():

    functions={}

    while True:

        print("\n1. Añadir nueva función\n2. Evaluar expresión\n3. Salir")

        choice=input("Selecciona una opción: ")

        if choice=="1":

            function_str=input("Introduce la nueva función: ")

            add_function(function_str,functions)

        elif choice=="2":

            expression=input("Introduce la expresión a evaluar: ")

            result=evaluate_expression(expression,functions)

            print("Resultado:",result)

        elif choice=="3":

            break

        else:

            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":

    main()