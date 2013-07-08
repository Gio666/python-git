# ----------------------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# File: consultaNombre.py
#
# Nehemias Herrera | A52761 | Proyecto Automatas & Compiladores | I-2013 | Profesor Luis Quesada
# ----------------------------------------------------------------------------------------------

import ply.lex as lex
import ply.yacc as yacc
import mechanize, re, sys

from collections import namedtuple
Persona = namedtuple("Persona", "nombre_completo numero_de_cedula nombre_del_padre numero_de_cedula_del_padre nombre_de_la_madre numero_de_cedula_de_la_madre")


# esta funcion realiza una consulta a la pagina del tse de consulta de ciudadanos 
# por nombre y devuelve el codigo HTML de la respuesta recibida
# pagina de consulta http://www.consulta.tse.go.cr/consulta_persona/consulta_nombres.aspx
def consulta_nombres(nombreCompleto):
    global nombre
    nombre = nombreCompleto
    
    URL = 'http://www.consulta.tse.go.cr/consulta_persona/consulta_nombres.aspx'
    
    # Crear instancia del navegador
    b = mechanize.Browser()
    
    # Cargar la pagina
    r = b.open(URL)
    
    # obtener el codigo HTML
    htmlSource = r.read()
    print 'recibido HTML de ' + str(sys.getsizeof(htmlSource)) + ' bytes.'
    
    # buscar Captcha dentro del codigo HTML
    valorCaptcha = re.search(r'[A-Z0-9]{6}\.bmp', htmlSource).group().rstrip('.bmp')
    
    # dividir el nombre en palabras
    partesDelNombre = nombreCompleto.split()
    #print 'El nombre tiene ' + str(len(partesDelNombre)) + ' partes.'
    
    # batear un rato con las asignaciones
    txtnombre = partesDelNombre[0]
    txtapellido1 = partesDelNombre[len(partesDelNombre) - 2]
    txtapellido2 = partesDelNombre[len(partesDelNombre) - 1]
    
    # seleccionamos el formulario
    b.select_form('form1')
    
    # llenamos los campos
    b['txtnombre'] = txtnombre
    b['txtapellido1'] = txtapellido1
    b['txtapellido2'] = txtapellido2
    b['txtcodigo'] = valorCaptcha
    
    # enviamos el formulario y esperamos la respuesta
    print 'enviando formulario con txtnombre [' + txtnombre + '], txtapellido1 [' + txtapellido1 + '], txtapellido2 [' + txtapellido2 + '] y CAPTCHA [' + valorCaptcha + ']'
    respuesta = b.submit()
    # obtenermos el codigo HTML de la respuesta
    htmlSource = respuesta.read()
    print 'respuesta recibida de ' + str(sys.getsizeof(htmlSource)) + ' bytes.'
    return htmlSource

# esta funcion calcula la distancia-levenshtein entre dos string y devuelve ese valor
# http://code.activestate.com/recipes/576874-levenshtein-distance/
def levenshtein(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    
    matrix = [range(l1 + 1)] * (l2 + 1)
    for zz in range(l2 + 1):
      matrix[zz] = range(zz,zz + l1 + 1)
    for zz in range(0,l2):
      for sz in range(0,l1):
        if s1[sz] == s2[zz]:
          matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
        else:
          matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
    return matrix[l2][l1]
    
# esta funcion parsea el resultado de consulta_cedula
def obtenerCedula(nombre):
    # /////////////////////////////////////////////////
    # /////////////////////// LEX /////////////////////
    # /////////////////////////////////////////////////
    tokens = ( 
        'PARTE_IZQUIERDA_LABEL', 
        'CEDULA',
        'NOMBRE',
        'PARTE_DERECHA_LABEL' 
        )
    
    def t_PARTE_IZQUIERDA_LABEL(t):
        r'<label\ for=\"chk[0-9]_[0-9]+\">'
        #print '<label>: ' + t.value
        return t
    
    def t_CEDULA(t):
        r'[0-9]{9}'
        #print 'cedula ' + t.value
        return t
    
    def t_NOMBRE(t):
        r'[A-Z]+ [A-Z]+ [A-Z ]+'
        #print 'nombre ' + t.value
        return t
        
    def t_PARTE_DERECHA_LABEL(t):
        r'<\/label>'
        #print '</label>'
        return t
    
    def t_error(t):
        #print "'%s'" % t.value[0]
        #print( "Lex error: ", t )
        t.lexer.skip(1)
        
    lex.lex()
    # /////////////////////////////////////////////////
    #//////////////////// FIN DE LEX //////////////////
    # /////////////////////////////////////////////////
    
    # /////////////////////////////////////////////////
    # /////////////////////// YACC ////////////////////
    # /////////////////////////////////////////////////
    # Parsing rules below
    
    def p_nombres(p):
        '''nombres : nombre nombres
                   | nombre'''
    
    def p_nombre(p):
        'nombre : PARTE_IZQUIERDA_LABEL CEDULA NOMBRE PARTE_DERECHA_LABEL'
        listaDeNombres[p[2]] = p[3].strip() 
        # print p[2] + ' ' + p[3]
    
    def p_error(p):
        #print "Syntax error at token", p.type
        # Just discard the token and tell the parser it's okay.
        yacc.errok()
    
    yacc.yacc()
    # /////////////////////////////////////////////////
    # //////////////////// FIN DE YACC ////////////////
    # /////////////////////////////////////////////////
    
    print 'buscando [' + nombre + ']'
    # parseamos el codigo HTML de la pagina del tribunal
    resultado = consulta_nombres(nombre)
    
    # busquemos si hay algun resultados
    posibles = re.search(r'total de [0-9]', resultado).group().lstrip('total de ')
    
    bestMatchCedula = '0'
    if (posibles != '0'):
        
        # aqui se almacenan los nombres encontrados
        listaDeNombres = {}
        
        # parse resultado
        yacc.parse(resultado)
        
        print 'Encontrados ' + str(len(listaDeNombres)) + ' posibles nombres'
        
        distanciaLevenshtein = 100
        bestMatchNombre = ''
        for cedula in listaDeNombres:
            #print  listaDeNombres[cedula] + ' cedula ' + cedula
            distancia = levenshtein(nombre, listaDeNombres[cedula])
            if (distancia < distanciaLevenshtein):
                bestMatchNombre = listaDeNombres[cedula]
                bestMatchCedula = cedula
                distanciaLevenshtein = distancia
            #print 'levenshtein de [',nombre, '] y [', listaDeNombres[cedula], '] es ', distancia
        
        print 'La mejor opcion es [' + bestMatchNombre + '] con la cedula [' + bestMatchCedula + '] y distancia levenshtein de ' + str(distanciaLevenshtein)
    else:
        print 'No hay resultado para [' + nombre + ']'
    return bestMatchCedula

#print obtenerCedula('ALBA FONSECA DELGADO')