# ----------------------------------------------------------------------------------------------
import sys
import ply.lex as lex
import ply.yacc as yacc

produccion = []

#/////////////////////// LEX ///////////////////////
tokens = ( 
    'NO_TERMINAL',
    'TERMINAL', 
    'FLECHA', 
    'O',
    'EPSILON',
    'NUEVA_LINEA',
    'ESPACIO'
    )

#t_NO_TERMINAL = r'[a-z]+\'*'
def t_NO_TERMINAL(t):
    r'[A-Z]+\'*'
    print 'NO TERMINAL [' + t.value + ']'
    return t

#t_TERMINAL = r'[a-z]+'
def t_TERMINAL(t):
    r'[a-z]+'
    print 'TERMINAL [' + t.value + ']'
    return t

#t_FLECHA = r'->|:'
def t_FLECHA(t):
    r'->|:'
    print 'FLECHA [' + t.value + ']'
    return t

#t_O = r'|'
def t_O(t):
    r'\|'
    print 'O [' + t.value + ']'
    return t

#t_EPSILON = r'EPS|eps'
def t_EPSILON(t):
    r'EPS|eps'
    print 'EPSILON [' + t.value + ']'
    return t

#t_NUEVA_LINEA = r' '
def t_NUEVA_LINEA(t):
    r'\n'
    print 'NUEVA LINEA'
    return t

def t_ESPACIO(t):
    r'\s'
    print 'ESPACIO'
    return t 

def t_error(t):
    print 'Lex error [' + t.value[0] + ']'
    #print( "Lex error: ", t )
    t.lexer.skip(1)

lex.lex()
#//////////////////// FIN DE LEX ////////////////////

#/////////////////////// YACC ///////////////////////
# Parsing rules   

def p_produccion(p):
    'produccion : parte_izquierda espacios flecha espacios parte_derecha NUEVA_LINEA'
    print 'produccion'
    print list(p)
    produccion.append('$')

def p_parte_izquierda(p):
    'parte_izquierda : NO_TERMINAL'
    print 'parte_izquierda'
    global produccion
    produccion.append(p[1])
    
def p_espacios(p):
    '''espacios : ESPACIO espacios 
                | ESPACIO'''
    print 'espacios'
    print list(p)

def p_flecha(p):
    ' flecha : FLECHA'
    print list(p)
    global produccion
    produccion.append(p[1])

def p_parte_derecha(p):
    '''parte_derecha : token 
                     | token parte_derecha'''
    print 'parte_derecha'
    print list(p)

def p_token(p):
    '''token : TERMINAL 
             | NO_TERMINAL
             | EPSILON'''
    print 'token'
    print list(p)
    global produccion
    produccion.append(p[1])

def p_error(p):
    print "Syntax error at token", p.type
    # Just discard the token and tell the parser it's okay.
    yacc.errok()

yacc.yacc()
#//////////////////// FIN DE YACC ///////////////////
listaDeRenglones = open(sys.argv[1]).read().splitlines(True)
#yacc.parse(open(sys.argv[1]).read())
#yacc.parse(listaDeRenglones[0])
#print(produccion)
listaDeProducciones = []
for linea in listaDeRenglones:
    produccion = []
    yacc.parse(linea)
    listaDeProducciones.append(produccion)
print listaDeProducciones