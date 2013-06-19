# -*- coding: UTF-8 -*-
# File: 003.py
import mechanize
import re
import sys
import pygraphviz as pgv
from collections import namedtuple

MyStruct = namedtuple("Persona", "cedula nombre sexo fechaDeNacimiento nombreDelPadre identificacionDelPadre nombreDeLaMadre identificacionDeLaMadre")

def obtenerDatos(cedula='112120468'):

    URL = 'http://www.consulta.tse.go.cr/consulta_persona/consulta_cedula.aspx'
    persona = Persona()
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
    # Llenamos los campos
    b['txtcedula'] = cedula
    b['txtcodigo'] = valorCaptcha
    # Enviamos el formulario y esperamos la respuesta
    print 'enviando formulario con cedula [' + cedula + '] y captcha [' + valorCaptcha + ']'
    respuesta = b.submit()
    # Obtenermos el codigo HTML de la respuesta
    htmlSource = respuesta.read()
    print 'respuesta recibida de ' + str(sys.getsizeof(htmlSource)) + ' bytes.'
    #//////////////////// LEX/YACC ////////////////////
    
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
        #print 'sexo ' + t.value
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
        #r'\"\sstyle=\"display:inline\-block;color:Navy;font\-family:Arial;font\-size:Smaller;width:344px;\">'
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
        
    import ply.lex as lex
    lexer = lex.lex()
    A=pgv.AGraph()
    
    # Parsing rules   
    def p_elementos(p):
        #'elementos : cedula nombre sexo'
        'elementos : nombre nombreDelPadre nombreDeLaMadre '
    
    #def p_elementos(p):
    #    'elementos : infoPersona'
        
    #def p_infoPersona(p):
    #    'infoPersona : nombre sexo cedula fechaDeNacimiento nacionalidad'
    
    def p_nombre(p):
        'nombre : SPAN_INICIO ID_NOMBRE_COMPLETO SPAN_STYLE NOMBRE SPAN_CIERRE'
        print p[2] + ' : ' + p[4]
        nombrePersona = p[4]
        A.add_node(nombrePersona)
        
    def p_nombreDelPadre(p):
        'nombreDelPadre : SPAN_INICIO ID_NOMBRE_DEL_PADRE SPAN_STYLE NOMBRE SPAN_CIERRE'
        print p[2] + ' : ' + p[4]
        nombrePapa = p[4]
        A.add_node(nombrePapa)
        A.add_edge(nombrePapa,nombrePersona)
        
    def p_nombreDeLaMadre(p):
        'nombreDeLaMadre : SPAN_INICIO ID_NOMBRE_DE_LA_MADRE SPAN_STYLE NOMBRE SPAN_CIERRE'
        print p[2] + ' : ' + p[4]
        nombreMama = p[4]
        A.add_node(nombreMama)
        A.add_edge(nombreMama,nombrePersona)
    
    def p_error(p):
        #print "Syntax error at token", p.type
        # Just discard the token and tell the parser it's okay.
        yacc.errok()
    
    import ply.yacc as yacc
    yacc.yacc()
    #parseamos la respuesta
    yacc.parse(htmlSource)
    
    #//////////////////// LEX/YACC ////////////////////







print A.string() # print to screen
print "Wrote simple.dot"
A.write('simple.dot') # write to simple.dot

B=pgv.AGraph('simple.dot') # create a new graph from file
B.layout() # layout with default (neato)
B.draw('familia.png') # draw png
print "familia.png"

from PIL import Image
f = Image.open("familia.png").show()