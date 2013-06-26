# ----------------------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# ----------------------------------------------------------------------------------------------
import sys
import ply.lex as lex
import ply.yacc as yacc

produccion = [] #Variable global para ir guardando las producciones

def expandirGramatica(listaDeProducciones):
    for produccion in listaDeProducciones:
        for token in produccion:
            if token == '|':
                indice = produccion.index(token)
                nuevaProduccion = []
                nuevaProduccion.append(produccion[0])
                nuevaProduccion.append(produccion[1])
                produccion.pop(indice)
                while token != '$':
                    token = produccion.pop(indice)
                    nuevaProduccion.append(token)
                listaDeProducciones.append(nuevaProduccion)
                produccion.append('$')
    return listaDeProducciones
    
#/////////////////////// LEX ///////////////////////
tokens = ( 
    'NO_TERMINAL',
    'TERMINAL', 
    'FLECHA', 
    'O',
    'EPSILON',
    'ESPACIO'
    )

t_NO_TERMINAL = r'[A-Z]+\'*'
t_TERMINAL = r'[a-z]+'
t_FLECHA = r'->|:'
t_O = r'\|'
t_ESPACIO = r'\s'

def t_EPSILON(t):
    r'EPS|eps'
    t.value = 'EPSILON'
    return t

def t_error(t):
    print ('Lex error [' + t.value[0] + ']')
    #print( "Lex error: ", t )
    t.lexer.skip(1)

lex.lex()
#//////////////////// FIN DE LEX ////////////////////

#/////////////////////// YACC ///////////////////////
# Parsing rules   

def p_produccion(p):
    'produccion : parte_izquierda espacios flecha espacios parte_derecha'
    global produccion
    produccion.append('$')
    print (list(p))

def p_parte_izquierda(p):
    'parte_izquierda : NO_TERMINAL'
    #global produccion
    produccion.append(p[1])
    
def p_espacios(p):
    '''espacios : espacios ESPACIO 
                | ESPACIO'''

def p_flecha(p):
    ' flecha : FLECHA'
    produccion.append(p[1])

def p_parte_derecha(p):
    '''parte_derecha : token 
                     | token parte_derecha'''

def p_token(p):
    '''token : TERMINAL 
             | NO_TERMINAL
             | O
             | EPSILON'''
    produccion.append(p[1])

def p_error(p):
    print ("Syntax error at token", p.type)
    # Just discard the token and tell the parser it's okay.
    yacc.errok()

yacc.yacc()
#//////////////////// FIN DE YACC ///////////////////

listaDeRenglones = open(sys.argv[1]).read().splitlines(True)

listaDeProducciones = []

for linea in listaDeRenglones:
    produccion = []
    yacc.parse(linea.rstrip('\n'))
    listaDeProducciones.append(produccion)

print ('Gramatica: --------------')
for p in listaDeProducciones:
    print (p)
    
print ('Gramatica Expandida -----')
    
listaDeProducciones = expandirGramatica(listaDeProducciones)
for p in listaDeProducciones:
    print (p)
    

                    
                    