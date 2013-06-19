# --------------------------------------------------------------------------------------
# ply: tseNameParser.py
#
# Nehemias Herrera | A52761 | Proyecto Automatas & Compiladores | I-2013 | Luis Quesada
# --------------------------------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc
import mechanize, re, sys

def obtenerCodigoHTMLparaBusquedaPorNombre(nombreCompleto):
    
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

#/////////////////////// LEX ///////////////////////
tokens = ( 
    'LETRA', 
    'NUMERO',
    'PARENTESIS_ANGULAR_IZQUIERDO', 
    'PARENTESIS_ANGULAR_DERECHO', 
    'NOMBRE',
    'IGUAL',
    'DIAGONAL'
    'ATRIBUTOS'
    )

t_LETRA = r'[a-zA-Z]'
t_NUMERO = r'[0-9]'
t_PARENTESIS_ANGULAR_IZQUIERDO = r'<'
t_PARENTESIS_ANGULAR_DERECHO = r'>'
t_NOMBRE = r'[a-zA-Z_:][a-zA-Z_:\.\-]*'
t_IGUAL = r'='
t_DIAGONAL = r'\\'
t_ATRIBUTOS = '[a-zA-Z0-9\-;:]+'

def t_error(t):
    #print "'%s'" % t.value[0]
    #print( "Lex error: ", t )
    t.lexer.skip(1)
    
lex.lex()
#//////////////////// FIN DE LEX ////////////////////

#/////////////////////// YACC ///////////////////////
# Parsing rules   
def p_elemento(p):
    ' elemento : etiqueta_de_inicio contenido etiqueta_de_cierre'

def p_etiqueta_de_inicio(p):
    'etiqueta_de_inicio : PARENTESIS_ANGULAR_IZQUIERDO nombre atributos PARENTESIS_ANGULAR_DERECHO'
    
def p_nombre(p):
    'nombre : NOMBRE'
    
def p_atributos(p):
    'atributos : atributo '
                 
def p_atributo(p):
    'atributo : nombre IGUAL nombre'
    
def p_contenido(p):
    'contenido : nombre'
    
def p_etiqueta_de_cierre(p):
    'etiqueta_de_cierre : PARENTESIS_ANGULAR_IZQUIERDO DIAGONAL nombre PARENTESIS_ANGULAR_DERECHO'
    
def p_error(p):
    #print "Syntax error at token", p.type
    # Just discard the token and tell the parser it's okay.
    yacc.errok()

yacc.yacc()
#//////////////////// FIN DE YACC ///////////////////

#parseamos el codigo HTML de la pagina del tribunal
resultado = obtenerCodigoHTMLparaBusquedaPorNombre('ANA GABRIELA SANCHO FONSECA')
print resultado
yacc.parse(resultado)

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