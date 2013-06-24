# --------------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# ply: tseNameParser.py
#
# Nehemias Herrera | A52761 | Proyecto Automatas & Compiladores | I-2013 | Luis Quesada
# --------------------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc
import mechanize, re, sys


# Calcula la distancia-levenshtein entre dos string y devuelve ese valor
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
    #print "That's the Levenshtein-Matrix:"
    #printMatrix(matrix)
    return matrix[l2][l1]

#Devuelve el codigo HTML de la pagina de resultado de realizar la consulta por nombre a la pagina del tse
def obtenerCodigoHTMLparaBusquedaPorNombre(nombreCompleto):
    global nombre
    nombre = nombreCompleto
    
    URL = 'http://www.consulta.tse.go.cr/consulta_persona/consulta_nombres.aspx'
    
    # Crear instancia del navegador
    b = mechanize.Browser()
    
    # Cargar la pagina
    r = b.open(URL)
    
    # Obtener el codigo HTML
    htmlSource = r.read()
    print 'recibido HTML de ' + str(sys.getsizeof(htmlSource)) + ' bytes.'
    
    # Buscar Captcha dentro del codigo HTML
    valorCaptcha = re.search(r'[A-Z0-9]{6}\.bmp', htmlSource).group().rstrip('.bmp')
    
    #dividir el nombre en palabras
    partesDelNombre = nombreCompleto.split()
    print 'El nombre tiene ' + str(len(partesDelNombre)) + ' partes.'
    
    #batear un rato con las asignaciones
    txtnombre = partesDelNombre[0]
    txtapellido1 = partesDelNombre[len(partesDelNombre) - 2]
    txtapellido2 = partesDelNombre[len(partesDelNombre) - 1]
    
    # Seleccionamos el formulario
    b.select_form('form1')
    
    # Llenamos los campos
    b['txtnombre'] = txtnombre
    b['txtapellido1'] = txtapellido1
    b['txtapellido2'] = txtapellido2
    b['txtcodigo'] = valorCaptcha
    
    #control = b.form.find_control('cmbresultados')
    #control.disabled = False
    #b[control.name] = ['500',]
    #print '---->> Valores: ' + str(b.form.find_control('cmbresultados')) 
    
    # Enviamos el formulario y esperamos la respuesta
    print 'enviando formulario con txtnombre [' + txtnombre + '], txtapellido1 [' + txtapellido1 + '], txtapellido2 [' + txtapellido2 + '] y CAPTCHA [' + valorCaptcha + ']'
    respuesta = b.submit()
    # Obtenermos el codigo HTML de la respuesta
    htmlSource = respuesta.read()
    print 'respuesta recibida de ' + str(sys.getsizeof(htmlSource)) + ' bytes.'
    return htmlSource

#//////////////////// OBTENER CEDULA  ///////////////////
def obtenerCedula(nombre):
    listaDeNombres.clear()
    #/////////////////////// LEX ///////////////////////
    tokens = ( 
        'PARTE_IZQUIERDA_LABEL', 
        'CEDULA',
        'NOMBRE',
        'PARTE_DERECHA_LABEL', 
        'NOMBRE_NO_ENCONTRADO'
        )
    
    def t_NOMBRE_NO_ENCONTRADO(t):
        r'1 de un total de 0'
        print 'NOMBRE NO ENCONTRADO'
        return t

    
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
    #//////////////////// FIN DE LEX ////////////////////
    
    #/////////////////////// YACC ///////////////////////
    # Parsing rules   
    def p_buscar_nombres(p):
         '''buscar_nombres : nombre_no_encontrado
                           | nombres'''
    
    def p_nombres(p):
        '''nombres : nombre nombres
                   | nombre'''
    
    def p_nombre(p):
        'nombre : PARTE_IZQUIERDA_LABEL CEDULA NOMBRE PARTE_DERECHA_LABEL'
        listaDeNombres[p[2]] = p[3].strip() 
        #print p[2] + ' ' + p[3]
        
    def p_nombre_no_encontrado(p):
        'nombre_no_encontrado : NOMBRE_NO_ENCONTRADO'
        listaDeNombres['0'] = 'NADIE' 
        print p[2] + ' ' + p[3]
        print 'NAN'
        
    def p_error(p):
        #print "Syntax error at token", p.type
        # Just discard the token and tell the parser it's okay.
        yacc.errok()
    
    yacc.yacc()
    #//////////////////// FIN DE YACC ///////////////////
    
    print 'buscando [' + nombre + ']'
    #parseamos el codigo HTML de la pagina del tribunal
    resultado = obtenerCodigoHTMLparaBusquedaPorNombre(nombre)
    
    #parse resultado
    yacc.parse(resultado)
    #del listaDeNombres['1']
    
    print 'Encontrados ' + str(len(listaDeNombres)) + ' posibles nombres'
    
    distanciaLevenshtein = 100
    bestMatchNombre = ''
    bestMatchCedula = 0
    for cedula in listaDeNombres:
        #print  listaDeNombres[cedula] + ' cedula ' + cedula
        distancia = levenshtein(nombre, listaDeNombres[cedula])
        if (distancia < distanciaLevenshtein):
            bestMatchNombre = listaDeNombres[cedula]
            bestMatchCedula = cedula
            distanciaLevenshtein = distancia
        #print 'levenshtein de [',nombre, '] y [', listaDeNombres[cedula], '] es ', distancia
    
    print 'La mejor opcion es [' + bestMatchNombre + '] con la cedula [' + bestMatchCedula + '] y distancia levenshtein de ' + str(distanciaLevenshtein)
    return bestMatchCedula
    #if len(listaDeNombres) == 1:
    #    for cedula in listaDeNombres:
    #        print 'La cedula de ' + listaDeNombres[cedula] + ' es ' + cedula
    #        return cedula
    #else: 
    #    palabrasDelNombre = nombre.split()
    #    for cedula in listaDeNombres:
    #        posibleMatch = True
    #        for palabra in palabrasDelNombre:
    #            if listaDeNombres[cedula].find(palabra) < 0:
    #                posibleMatch = False
    #        if posibleMatch:
    #            print 'La cedula de ' + listaDeNombres[cedula] + ' es ' + cedula
    #            return cedula

#listaDeNombres = {'1':'1',}
listaDeNombres = {}

#print obtenerCedula('JOSE JOAQUIN HERRERA CASTRO')
#print obtenerCedula('NEHEMIAS ESAU HERRERA SANCHO')
#print obtenerCedula('ANA GABRIELA SANCHO FONSECA')
#print obtenerCedula('JUAN MANUEL PREGONERO CABALLO')