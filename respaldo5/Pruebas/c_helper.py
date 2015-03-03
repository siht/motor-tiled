from ctypes import c_char, c_int, POINTER, cast
import string

def char_parse_int(char):
    '''el valor de un char de c pasa como una cadena de longitud 1 en python
    asi que hay que convertirlo a variables nativas de c para poder obtener el
    valor entero lo cual no esta implementado en las cadenas de python.
    valor de entrada: str o unicode (longitud 1)
    valor de regreso: int
    int_value_of_str1('a') --> return 97
    int_value_of_str1('A') --> return 65
    int_value_of_str1(otro_objeto) --> Exception no es aceptable u otra excepcion'''
    if not (type(char) != str or type(char) != unicode) and len(char) > 1:
        raise Exception, 'no es aceptable'
    puntero_int = cast((c_char * 1)(char),POINTER(c_int)) #se castea como puntero de c
    variable_int = puntero_int.contents # se obtiene la variable apuntada de c
    valor = variable_int.value # se obtiene el valor de la variable apuntada como valor de python
    return valor
    
def int_parse_char(eent):
    pointer_char = cast((c_int * 1)(eent),POINTER(c_char))
    var_char = pointer_char.contents
    valor = var_char.value
    return valor
    
if __name__ == '__main__':
    print char_parse_int('a')
    print char_parse_int('A')
    print char_parse_int('-')
    print hex(char_parse_int('0'))
    print hex(char_parse_int('9'))
##    for i in range(0x30,0xff):
##        print int_parse_char(i)
