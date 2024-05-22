def add_function(function_str,functions):
    
    #el formato de la funcion es f[c,d,...] = c+d*... 

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
