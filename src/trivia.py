from functools import reduce
import random
from typing import Callable
import pandas as pd

def nombreUsuario(func) -> Callable:
    """Decorador que solicita el nombre del usuario y lo muestra en pantalla al inicio del juego"""
    def wrapper():
        nombre = func()
        return f'Hola {nombre}, bienvenid@ al trivia. ¿Preparad@ para jugar?'
    return wrapper
        
@nombreUsuario #decoradores
def usuario() -> str:
    """Solicita al usuario que ingrese su nombre."""
    nombre = input('Ingrese su nombre: ')
    print()
    return nombre

def eliminar_tildes(palabra, tildes=None, resultado=''): #recursion
    """Función que elimina las tildes de una palabra y la deja en minúsculas"""
    if tildes is None:
        tildes = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
    
    if not palabra:
        return resultado.lower()
    
    return eliminar_tildes(palabra[1:], tildes, resultado + tildes.get(palabra[0], palabra[0]))

def preguntas(): #generador y filter
    """Generador que selecciona 5 preguntas al azar y las muestra en pantalla para que el usuario responda una a una"""
    df =  pd.read_csv('trivia_questions.csv')
    preguntas_seleccionadas = random.sample(range(len(df)), 5)
    for i in preguntas_seleccionadas:
        preguntas_dic = df.iloc[i].to_dict()

        preguntas_sin_respuesta = dict(filter(lambda item : item[0] != 'Correcta', preguntas_dic.items()))
        
        print()
        for clave, valor in preguntas_sin_respuesta.items():
            print(f'{clave}: {valor}')
    
        yield preguntas_dic

def puntaje(respuestas) -> int: #lista x compresion y reduce
    """Función que calcula el puntaje obtenido por el usuario en una ronda de trivia"""
    respuestas_en_numeros = [10 if x else 0 for x in respuestas]
    return reduce(lambda x, y: x + y, respuestas_en_numeros)

# def puntaje(respuestas) -> int: #map y reduce
#     conteo = map(lambda x: 10 if x else 0, respuestas)
#     return reduce(lambda x, y: x + y, conteo) 

def jugar(preguntas_iter): 
    """Función que permite al usuario jugar una ronda de trivia y devuelve una lista con las respuestas correctas"""
    respuestas = []    
    try:
        pregunta = next(preguntas_iter) 
        respuesta = input('Ingrese su respuesta: ').strip()
        respuesta_sin_tildes = eliminar_tildes(respuesta)
        correcta_sin_tildes = eliminar_tildes(pregunta['Correcta'].strip().strip('"'))

        if respuesta_sin_tildes == correcta_sin_tildes:
            respuestas.append(True)
        else: respuestas.append(False)

        return respuestas + jugar(preguntas_iter)
    
    except StopIteration:
        return []

def trivia():
    """Función principal que ejecuta el juego de trivia"""
    preguntas_iter = iter(preguntas())
    respuestas = jugar(preguntas_iter)
    
    print(f'Obtuviste {puntaje(respuestas)} puntos en esta ronda')
    print()
    
    if input('¿Quieres jugar de nuevo? (s/n): ').strip().lower() == 's':
        trivia()
    else:
        print('Gracias por jugar, ¡Hasta la próxima!')

if __name__ == '__main__':
    print(usuario())
    trivia()