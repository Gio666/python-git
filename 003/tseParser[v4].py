# ----------------------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# ply: tseParser.py
#
# Nehemias Herrera | A52761 | Proyecto Automatas & Compiladores | I-2013 | Profesor Luis Quesada
# ----------------------------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc
import mechanize, re, sys
import tseNameParser

# Esta funcion realiza una consulta a la pagina del tse de consulta de ciudadanos por numero de cedula
# y devuelve el codigo HTML de la respuesta recibida
def obtenerCodigoHTMLparaCedula(cedula):
    
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

# Esta funcion contiene el analizador lexico y sintactico que parsea codigo HTML de respuesta
# a una consulta por numero de cedula
def obtenerNombre(cedula):

    #/////////////////////// LEX ///////////////////////
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
        r'[0-9]{9}'
        #print 'cedula ' + t.value
        return t
        
    #t_NOMBRE = r'[A-Z ]+'
    def t_NOMBRE(t):
        r'[A-Z]+ [A-Z]+ [A-Z ]+'
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
    #//////////////////// FIN DE LEX ////////////////////
    
    #/////////////////////// YACC ///////////////////////
    # Parsing rules   
    def p_elementos(p):
        #'elementos : cedula nombre sexo'
        'elementos : nombre nombreDelPadre nombreDeLaMadre '
    
    def p_nombre(p):
        'nombre : SPAN_INICIO ID_NOMBRE_COMPLETO SPAN_STYLE NOMBRE SPAN_CIERRE'
        print p[2] + ' : ' + p[4]
        global nombre
        nombre = p[4]
        
    def p_nombreDelPadre(p):
        'nombreDelPadre : SPAN_INICIO ID_NOMBRE_DEL_PADRE SPAN_STYLE NOMBRE SPAN_CIERRE'
        print p[2] + ' : ' + p[4]
        global papa
        papa = p[4]
        
    def p_nombreDeLaMadre(p):
        'nombreDeLaMadre : SPAN_INICIO ID_NOMBRE_DE_LA_MADRE SPAN_STYLE NOMBRE SPAN_CIERRE'
        print p[2] + ' : ' + p[4]
        global mama
        mama = p[4]
    
    def p_error(p):
        #print "Syntax error at token", p.type
        # Just discard the token and tell the parser it's okay.
        yacc.errok()
    
    yacc.yacc()
    #//////////////////// FIN DE YACC ///////////////////
    
    # obtenemos el codigo HTML de respuesta de la consulta por cedula
    codigo = obtenerCodigoHTMLparaCedula(cedula)
    # lo paseamos para obtener los datos que queremos
    yacc.parse(codigo)
    #regresamos con el mandado return
    return Persona(nombre_completo = nombre, numero_de_cedula = cedula, nombre_del_padre = papa, nombre_de_la_madre = mama)
    
# Esta funcion dibuja el arbol genealogico en un archivo de imagen
def dibuje(arbol):

    #print A.string() # print to screen
    print "Wrote simple.dot"
    arbol.write('simple.dot') # write to simple.dot
    
    B=pgv.AGraph('simple.dot') # create a new graph from file
    B.layout(prog='dot') # layout with default (neato)
    nombreDeArchivo = 'familia.png'
    
    B.draw(nombreDeArchivo) # draw png
    print nombreDeArchivo
    
    # Aqui abrimos la imagen y la mostramos
    from PIL import Image
    f = Image.open(nombreDeArchivo).show()
    
# Esta funciona recibe una lista que se comporta como un arbol binario, dado un elemento x
# su hijo izquierdo esta en la posicion 2 * n - 1 y su hijo derecho en 2 * n
def hacerArbol(lista):
    #aqui creamos el arbol
    import pygraphviz as pgv
    
    # inicializamos el arbol
    arbol=pgv.AGraph(directed=True)
    arbol.graph_attr['label']='Familia'
    arbol.node_attr['shape']='box'
    arbol.node_attr['style']='rounded'
    arbol.graph_attr['sep']= 0.5
    arbol.graph_attr['overlap']= 'orthoxy'
    arbol.graph_attr['mode'] = 'ipsep'
    arbol.graph_attr['diredgeconstraints'] = 'true'
    cabezaDeFecha = 'none'
    
    #agregamos la familia al grafo
    for x in range(1, 3):
        # sacamos de la lista el trio persona-madre-padre
        persona = lista[x - 1].nombre_completo
        madre = lista[2 * x - 1].nombre_completo
        padre = lista[2 * x].nombre_completo
        # los agregamos al grafo
        arbol.add_node(persona)
        arbol.add_node(madre)
        arbol.add_node(padre)
        # agregamos un nodo donde unir los 3
        arbol.add_node(persona + madre + padre, shape = 'point')
        # recuperamos el nodo
        nodo = arbol.get_node(persona + madre + padre)
        # unimos los 3 en la pega
        arbol.add_edge(madre, union, arrowhead = cabezaDeFecha)
        arbol.add_edge(padre, union, arrowhead = cabezaDeFecha)
        arbol.add_edge(union, persona, arrowhead = cabezaDeFecha)
        
    # agregamos ultimo nivel de parentezco
    for x in range(1, 3):
        # sacamos de la lista el trio persona-madre-padre
        persona = lista[x - 1].nombre_completo
        madre = lista[2 * x - 1].nombre_completo
        padre = lista[2 * x].nombre_completo
        # los agregamos al grafo
        arbol.add_node(persona)
        arbol.add_node(madre)
        arbol.add_node(padre)
        # agregamos un nodo donde unir los 3
        arbol.add_node(persona + madre + padre, shape = 'point')
        # recuperamos el nodo
        nodo = arbol.get_node(persona + madre + padre)
        # unimos los 3 en la pega
        arbol.add_edge(madre, union, arrowhead = cabezaDeFecha)
        arbol.add_edge(padre, union, arrowhead = cabezaDeFecha)
        arbol.add_edge(union, persona, arrowhead = cabezaDeFecha)
    
    #dibujamos el arbol
    dibuje(arbol)
    
    
# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////  MAIN  ////////////////////////////////
# ////////////////////////////////////////////////////////////////////////
from collections import namedtuple
Persona = namedtuple("Persona", "nombre_completo numero_de_cedula nombre_del_padre nombre_de_la_madre")

# recibimos la cedula como parametro
cedula = str(sys.argv[1])

# datos de la persona consultada
persona = obtenerNombre(cedula)

# datos de la mama de la persona consultada
cedula = tseNameParser.obtenerCedula(persona.nombre_de_la_madre)
madre = obtenerNombre(cedula)

# datos del papa de la persona consultada
cedula = tseNameParser.obtenerCedula(persona.nombre_del_padre)
padre = obtenerNombre(cedula)

# datos de la abuela materna de la persona consultada
cedula = tseNameParser.obtenerCedula(madre.nombre_de_la_madre)
abuela_materna = obtenerNombre(cedula)

# datos del abuelo materno de la persona consultada
cedula = tseNameParser.obtenerCedula(madre.nombre_del_padre)
abuelo_materno = obtenerNombre(cedula)

# datos de la abuela paterna de la persona consultada
cedula = tseNameParser.obtenerCedula(padre.nombre_de_la_madre)
abuela_paterna = obtenerNombre(cedula)

# datos del abuelo paterno de la persona consultada
cedula = tseNameParser.obtenerCedula(padre.nombre_del_padre)
abuelo_paterno = obtenerNombre(cedula)

# enlistamos a la familia en algun orden
listaFamiliar = [persona, madre, padre, abuela_materna, abuelo_materno, abuela_paterna, abuelo_paterno]

hacerArbol(listaFamiliar)