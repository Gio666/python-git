# --------------------------------------------------------------------------------------
# ply: tseNameParser.py
#
# Nehemias Herrera | A52761 | Proyecto Automatas & Compiladores | I-2013 | Luis Quesada
# --------------------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc
import mechanize, re, sys

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
    #//////////////////// FIN DE LEX ////////////////////
    
    #/////////////////////// YACC ///////////////////////
    # Parsing rules   
    def p_nombres(p):
        '''nombres : nombre nombres
                   | nombre'''
        #print 'nombres'
    
    def p_nombre(p):
        ' nombre : PARTE_IZQUIERDA_LABEL CEDULA NOMBRE PARTE_DERECHA_LABEL'
        listaDeNombres[p[2]] = p[3] 
        #print p[2] + ' ' + p[3]
        
        
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
    
    for cedula in listaDeNombres:
        print  listaDeNombres[cedula] + ' cedula ' + cedula
    
    if len(listaDeNombres) == 1:
        for cedula in listaDeNombres:
            print 'La cedula de ' + listaDeNombres[cedula] + ' es ' + cedula
            return cedula
    else: 
        palabrasDelNombre = nombre.split()
        for cedula in listaDeNombres:
            posibleMatch = True
            for palabra in palabrasDelNombre:
                if listaDeNombres[cedula].find(palabra) < 0:
                    posibleMatch = False
            if posibleMatch:
                print 'La cedula de ' + listaDeNombres[cedula] + ' es ' + cedula
                return cedula

#listaDeNombres = {'1':'1',}
listaDeNombres = {}
#print obtenerCedula('JOSE JOAQUIN HERRERA CASTRO')
#print obtenerCedula('NEHEMIAS ESAU HERRERA SANCHO')
#print obtenerCedula('ANA GABRIELA SANCHO FONSECA')
#print obtenerCedula('JUAN MANUEL PREGONERO CABALLO')