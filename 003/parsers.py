# ----------------------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# File: tseParser.py
# Nehemias Herrera | A52761 | Proyecto Automatas & Compiladores | I-2013 | Profesor Luis Quesada
# ----------------------------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc
import mechanize, re, sys

# esta funcion realiza una consulta a la pagina del tse de consulta de ciudadanos 
# por numero de cedula y devuelve el codigo HTML de la respuesta recibida
# pagina de consulta http://www.consulta.tse.go.cr/consulta_persona/consulta_cedula.aspx
def consulta_cedula(cedula):
    
    # direccion web de consulta por numero de cedula del tse
    URL = 'http://www.consulta.tse.go.cr/consulta_persona/consulta_cedula.aspx'
    # Crear instancia del navegador
    b = mechanize.Browser()
    # Cargar la pagina
    r = b.open(URL)
    # Obtener el codigo HTML
    htmlSource = r.read()
    print 'recibido HTML de ' + str(sys.getsizeof(htmlSource)) + ' bytes.'
    # Buscar Captcha dentro del codigo HTML
    valorCaptcha = re.search(r'[A-Z0-9]{6}\.bmp', htmlSource).group().rstrip('.bmp')
    # Seleccionamos el formulario
    b.select_form('form1')
    # Llenamos los campos requeridos para la consulta
    b['txtcedula'] = cedula
    b['txtcodigo'] = valorCaptcha
    # Enviamos el formulario y esperamos la respuesta
    print 'enviando formulario con cedula [' + cedula + '] y captcha [' + valorCaptcha + ']'
    respuesta = b.submit()
    # Obtenermos el codigo HTML de la respuesta
    htmlSource = respuesta.read()
    print 'respuesta recibida de ' + str(sys.getsizeof(htmlSource)) + ' bytes.'
    return htmlSource

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
    print 'El nombre tiene ' + str(len(partesDelNombre)) + ' partes.'
    
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
    # /////////////////////////////////////////////////
    #//////////////////// FIN DE LEX //////////////////
    # /////////////////////////////////////////////////
    
    # /////////////////////////////////////////////////
    # /////////////////////// YACC ////////////////////
    # /////////////////////////////////////////////////
    # Parsing rules below
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
        print 'Ningun resultado'
    
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
    
    # aqui se almacenan los nombres encontrados
    listaDeNombres = []
    
    # parse resultado
    yacc.parse(resultado)
    
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
   
# esta funcion parsea el resultado de consulta_nombres
def obtenerPersona(cedula):
    # /////////////////////////////////////////////////
    # /////////////////////// LEX /////////////////////
    # /////////////////////////////////////////////////
    tokens = ( 
        'ID_CEDULA',
        'ID_NOMBRE_COMPLETO', 
        'ID_SEXO', 
        'ID_CONOCIDO_COMO', 
        'ID_FECHA_DE_NACIMIENTO', 
        'ID_NOMBRE_DEL_PADRE', 
        'ID_NACIONALIDAD', 
        'ID_IDENTIFICACION_DEL_PADRE', 
        'ID_EDAD', 
        'ID_NOMBRE_DE_LA_MADRE', 
        'ID_IDENTIFICACION_DE_LA_MADRE',
        'CEDULA', 'NOMBRE', 'SEXO', 'FECHA', 'SPAN_INICIO', 'SPAN_STYLE', 'SPAN_CIERRE', 
        )
    
    t_ID_CEDULA = 'lblcedula'
    t_ID_NOMBRE_COMPLETO = 'lblnombrecompleto'
    t_ID_SEXO = 'lblsexo'
    t_ID_CONOCIDO_COMO = 'lblconocidocomo'
    t_ID_FECHA_DE_NACIMIENTO = 'lblfechaNacimiento'
    t_ID_NOMBRE_DEL_PADRE = 'lblnombrepadre'
    t_ID_NACIONALIDAD = 'lblnacionalidad'
    t_ID_IDENTIFICACION_DEL_PADRE = 'lblid_padre'
    t_ID_EDAD = 'lbledad'
    t_ID_NOMBRE_DE_LA_MADRE = 'lblnombremadre'
    t_ID_IDENTIFICACION_DE_LA_MADRE = 'lblid_madre'
    
    #t_CEDULA = r'[0-9]{9}'
    def t_CEDULA(t):
        r'[0-9]{9}|>0<'
        #print 'cedula ' + t.value
        return t
        
    #t_NOMBRE = r'[A-Z ]+'
    def t_NOMBRE(t):
        r'[A-ZÑ]+ [A-ZÑ]+ [A-ZÑ ]+'
        #print 'nombre ' + t.value
        return t
    
    #t_SEXO = r'MASCULINO|FEMENINO'
    def t_SEXO(t):
        r'MASCULINO|FEMENINO'
        print 'sexo ' + t.value
        return t
    
    #t_FECHA = r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}'
    def t_FECHA(t):
        r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}'
        #print 'fecha ' + t.value
        return t
    
    #t_SPAN_INICIO = r' <span id=\"'
    def t_SPAN_INICIO(t):
        r'<span\sid=\"'
        #print 'span inicio'
        return t
    
    #t_SPAN_STYLE = r'\" style=\"display:inline\-block;color:Navy;font\-family:Arial;font\-size:Smaller;width:344px;\">'
    def t_SPAN_STYLE(t):
        r'\"\sstyle=\"[a-zA-Z0-9\-;:]+\">'
        #print 'span style '
        return t
    
    #t_SPAN_CIERRE = r'</span>'
    def t_SPAN_CIERRE(t):
        r'</span>'
        #print 'span cierre'
        return t
    
    def t_error(t):
        #print "'%s'" % t.value[0]
        #print( "Lex error: ", t )
        t.lexer.skip(1)
        
    lex.lex()

    # /////////////////////////////////////////////////
    # //////////////////// FIN DE LEX /////////////////
    # /////////////////////////////////////////////////
    
    # /////////////////////////////////////////////////
    #/////////////////////// YACC /////////////////////
    # /////////////////////////////////////////////////
    # Parsing rules   
    def p_datos(p):
        'datos : datos_de_la_persona datos_del_padre datos_de_la_madre'
    
    def p_datos_de_la_persona(p):
        '''datos_de_la_persona : cedula_de_la_persona nombre_de_la_persona 
                               | cedula_de_la_persona
                               | nombre_de_la_persona'''
    
    def p_cedula_de_la_persona(p):
        'cedula_de_la_persona : SPAN_INICIO ID_CEDULA SPAN_STYLE CEDULA SPAN_CIERRE'
        global cedula_de_la_persona
        cedula_de_la_persona = p[4]
        print p[2] + ' : ' + cedula_de_la_persona
    
    def p_nombre_de_la_persona(p):
        'nombre_de_la_persona : SPAN_INICIO ID_NOMBRE_COMPLETO SPAN_STYLE NOMBRE SPAN_CIERRE'
        global nombre_de_la_persona
        nombre_de_la_persona = p[4]
        print p[2] + ' : ' + nombre_de_la_persona
    
    def p_datos_del_padre(p):
        '''datos_del_padre : nombre_del_padre cedula_del_padre  
                           | nombre_del_padre
                           | cedula_del_padre'''
    
    def p_nombre_del_padre(p):
        'nombre_del_padre : SPAN_INICIO ID_NOMBRE_DEL_PADRE SPAN_STYLE NOMBRE SPAN_CIERRE'
        global nombre_del_padre
        nombre_del_padre = p[4]
        print p[2] + ' : ' + nombre_del_padre
    
    def p_cedula_del_padre(p):
        'cedula_del_padre : SPAN_INICIO ID_IDENTIFICACION_DEL_PADRE SPAN_STYLE CEDULA SPAN_CIERRE'
        global cedula_del_padre
        cedula_del_padre = p[4]
        if (cedula_del_padre == '>0<'):
            cedula_del_padre = '0'
        print p[2] + ' : ' + cedula_del_padre
    
    def p_datos_de_la_madre(p):
        '''datos_de_la_madre : nombre_de_la_madre 
                             | cedula_de_la_madre  
                             | nombre_de_la_madre cedula_de_la_madre'''
    
    def p_nombre_de_la_madre(p):
        'nombre_de_la_madre : SPAN_INICIO ID_NOMBRE_DE_LA_MADRE SPAN_STYLE NOMBRE SPAN_CIERRE'
        global nombre_de_la_madre
        nombre_de_la_madre = p[4]
        print p[2] + ' : ' + nombre_de_la_madre
    
    def p_cedula_de_la_madre(p):
        'cedula_de_la_madre : SPAN_INICIO ID_IDENTIFICACION_DE_LA_MADRE SPAN_STYLE CEDULA SPAN_CIERRE'
        global cedula_de_la_madre
        cedula_de_la_madre = p[4]
        if (cedula_de_la_madre == '>0<'):
            cedula_de_la_madre = '0'
        print p[2] + ' : ' + cedula_de_la_madre
    
    def p_error(p):
        #print "Syntax error at token", p.type
        # Just discard the token and tell the parser it's okay.
        yacc.errok()
    
    yacc.yacc()
    # /////////////////////////////////////////////////
    #//////////////////// FIN DE YACC /////////////////
    # /////////////////////////////////////////////////
    # obtenemos el codigo HTML de respuesta de la consulta por cedula
    codigo = obtenerCodigoHTMLparaCedula(cedula)
    # lo paseamos para obtener los datos que queremos
    yacc.parse(codigo)
    #regresamos con el mandado return
    
    return Persona(nombre_completo = nombre_de_la_persona, 
                   numero_de_cedula = cedula_de_la_persona,  
                   nombre_del_padre = nombre_del_padre,
                   numero_de_cedula_del_padre = cedula_del_padre,
                   nombre_de_la_madre  = nombre_de_la_madre,
                   numero_de_cedula_de_la_madre = cedula_de_la_madre )