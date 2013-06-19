# ----------------------------------------------------------------------------------------------
# ply: tseParser.py
#
# Nehemias Herrera | A52761 | Proyecto Automatas & Compiladores | I-2013 | Profesor Luis Quesada
# ----------------------------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc
import mechanize, re, sys
import tseNameParser

class Persona:
  nombre = ''
  cedula = 0
  nombreDeLaMadre = 'mama'
  nombreDelPadre = 'papa'

def consultarPorCedula(cedula):
    
    # url de la pagina del tse de consulta por numero de Cédula 
    url = 'http://www.consulta.tse.go.cr/consulta_persona/consulta_cedula.aspx'
    
    # navegador
    navegador = mechanize.Browser()
    
    # abrir URL en el navegador
    pagina = navegador.open(url)
    
    # obtener el codigo HTML de la pagina
    codigoHTML = pagina.read()
    print str(sys.getsizeof(codigoHTML)) + ' bytes recibidos.'
    
    # buscar captcha dentro del codigo HTML
    captcha = re.search(r'[A-Z0-9]{6}\.bmp', codigoHTML).group().rstrip('.bmp')
    
    # seleccionamos el formulario form1
    navegador.select_form('form1')
    
    # llenamos los campos necesarios del formulario
    navegador['txtcedula'] = cedula
    navegador['txtcodigo'] = captcha
    
    # enviamos el formulario y esperamos la respuesta
    print 'enviando formulario con cedula [' + cedula + '] y captcha [' + captcha + ']'
    respuesta = navegador.submit()
    
    # obtenemos el codigo HTML de la respuesta
    codigoHTML = respuesta.read()
    print str(sys.getsizeof(codigoHTML)) + ' bytes recibidos.'
    
    # nos devolvemos con el mandado
    return codigoHTML

def arbol(cedula):

    nombreCompleto = nombreDeLaMadre = nombreDelPadre = ''
    
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
        t.lexer.skip(1)
        
    lex.lex()
# //////////////////// FIN DE LEX ////////////////////
    
# /////////////////////// YACC ///////////////////////
    # reglas de parseo   
    def p_elementos(p):
        'elementos : nombre_completo nombre_del_padre nombre_de_la_madre '
    
    def p_nombre_completo(p):
        'nombre_completo : SPAN_INICIO ID_NOMBRE_COMPLETO SPAN_STYLE NOMBRE SPAN_CIERRE'
        print p[2] + ' : ' + p[4]
        global nombreCompleto
        nombreCompleto = p[4]

    def p_nombre_del_padre(p):
        'nombre_del_padre : SPAN_INICIO ID_NOMBRE_DEL_PADRE SPAN_STYLE NOMBRE SPAN_CIERRE'
        print p[2] + ' : ' + p[4]
        global nombreDelPadre
        nombreDelPadre = p[4]
        
    def p_nombre_de_la_madre(p):
        'nombre_de_la_madre : SPAN_INICIO ID_NOMBRE_DE_LA_MADRE SPAN_STYLE NOMBRE SPAN_CIERRE'
        print p[2] + ' : ' + p[4]
        global nombreDeLaMadre
        nombreDeLaMadre = p[4]
    
    def p_error(p):
        #print "Syntax error at token", p.type
        # Just discard the token and tell the parser it's okay.
        yacc.errok()
    
    yacc.yacc()
# //////////////////// FIN DE YACC ///////////////////

# ////////////////////// MAIN? //////////////////////

cedula = str(sys.argv[1])




for x in range(0, 2):
    
    yacc.parse(obtenerCodigoHTMLparaCedula(cedula))
    
    #cedulaDeMama = 'cedula de ' + mama + ' es ' + tseNameParser.obtenerCedula(mama)
    #//////////////////// CREAR IMAGEN  ///////////////////
    import pygraphviz as pgv
    
    A=pgv.AGraph(directed=True)
    A.graph_attr['label']='Familia'
    A.node_attr['shape']='box'
    A.node_attr['style']='rounded'
    A.graph_attr['sep']= 0.5
    A.graph_attr['overlap']= 'orthoxy'
    A.graph_attr['mode'] = 'ipsep'
    A.graph_attr['diredgeconstraints'] = 'true'
    cabezaDeFecha = 'none'
    
    A.add_node(nombre, color = 'yellow', style = 'filled,rounded' )
    
    A.add_node(mama)
    A.add_node(papa)
    
    union = '.'
    A.add_node(union, shape = 'point')
    nodo = A.get_node(union)
    
    A.add_edge(mama, union, arrowhead = cabezaDeFecha)
    A.add_edge(papa, union, arrowhead = cabezaDeFecha)
    
    A.add_edge(union, nombre, arrowhead = cabezaDeFecha)
    
    #A.add_edge(union, 'hijo1', arrowhead = cabezaDeFecha)
    #A.add_edge(union, 'hijo2', arrowhead = cabezaDeFecha)
    
    #print A.string() # print to screen
    print "Wrote simple.dot"
    A.write('simple.dot') # write to simple.dot
    
    B=pgv.AGraph('simple.dot') # create a new graph from file
    B.layout(prog='dot') # layout with default (neato)
    B.draw('familia.png') # draw png
    print "familia.png"
    
    #//////////////////// ABRIR IMAGEN  ///////////////////
    from PIL import Image
    f = Image.open("familia.png").show()