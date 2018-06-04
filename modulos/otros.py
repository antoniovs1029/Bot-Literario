def user_input(entrada = None, ruta_log = None):
    if entrada is None    :    
        entrada = ""
        while len(entrada) == 0 or entrada == '\n':
            entrada = input()
    
    if ruta_log is not None:
        with open(ruta_log, 'a') as f:
            f.write(entrada + '\n')
    return entrada

def crear_dir(ruta_dir):
    import pathlib
    pathlib.Path(ruta_dir).mkdir(parents=True, exist_ok=True)
