# -*- coding: UTF-8 -*-
# File: 003.py
import mechanize
import ply.lex as lex
import ply.yacc as yacc

URL = 'http://www.consulta.tse.go.cr/consulta_persona/consulta_cedula.aspx'

# Create a Browser instance
b = mechanize.Browser()
# Load the page
r = b.open(URL)
# Get HMTL code of URL
htmlSource = r.read()
valorCaptcha = '000000'

#//////////////////// LEX/YACC ////////////////////

tokens = ( 'CAPTCHA', )

t_CAPTCHA = r'[A-Z0-9]{6}\.bmp'

def t_error(t):
    #print "'%s'" % t.value[0]
    #print( "Lex error: ", t )
    t.lexer.skip(1)
    
lexer1 = lex.lex()

# Parsing rules

def p_captchaCompleto(p):
    "statement : CAPTCHA "
    global valorCaptcha
    valorCaptcha = p[1].rstrip('.bmp') 
    print ("Captcha es " +  valorCaptcha)

def p_error(p):
    if p:
        pass#print("Syntax error at '%s'" % p.value)
    else:
        pass#print("Syntax error at EOF")

parser1 = yacc.yacc()
parser1.parse(htmlSource, lexer=lexer1)

#//////////////////// LEX/YACC ////////////////////

cedula = '112120460'
# Select the form
print 'enviando formulario con [' + cedula + '] y [' + valorCaptcha + ']\n'
b.select_form('form1')
# Fill out the form
b['txtcedula'] = '112120468'
b['txtcodigo'] = valorCaptcha
# Submit!
respuesta = b.submit()

htmlSource = respuesta.read()

#//////////////////// LEX/YACC ////////////////////

tokens = ( 'ID_CEDULA', 'ID_NOMBRE_COMPLETO', 'ID_SEXO', 'ID_CONOCIDO_COMO', 'ID_FECHA_DE_NACIMIENTO', 'ID_NOMBRE_DEL_PADRE', 'ID_NACIONALIDAD', 'ID_IDENTIFICACION_DEL_PADRE', 'ID_EDAD', 'ID_NOMBRE_DE_LA_MADRE', 'ID_IDENTIFICACION_DE_LA_MADRE',
    'CEDULA', 'NOMBRE_COMPLETO', 'SEXO', 'CONOCIDO_COMO', 'FECHA_DE_NACIMIENTO', 'NOMBRE_DEL_PADRE', 'NACIONALIDAD', 'IDENTIFICACION_DEL_PADRE', 'EDAD', 'NOMBRE_DE_LA_MADRE', 'IDENTIFICACION_DE_LA_MADRE',
    'SPAN_INICIO', 'SPAN_STYLE', 'SPAN_CIERRE'
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

t_CEDULA = r'[0-9]{9}'
t_NOMBRE_COMPLETO = r'[A-Z ]+'
t_SEXO = r'MASCULION|FEMENINO'
t_CONOCIDO_COMO = r'[A-Z ]+'
t_FECHA_DE_NACIMIENTO = r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}'
t_IDENTIFICACION_DEL_PADRE = r'[A-Z ]+'
t_NACIONALIDAD = r'[A-Z ]+'
t_IDENTIFICACION_DEL_PADRE = r'[0-9]{9}'
t_EDAD = r'[[0-9]{2}|[0-9]{3}] AÑOS'
t_NOMBRE_DE_LA_MADRE = r'[A-Z ]+'
t_IDENTIFICACION_DE_LA_MADRE = r'[0-9]{9}'

t_SPAN_INICIO = r' <span id=\"'
t_SPAN_STYLE = r'\" style=\"display:inline\-block;color:Navy;font\-family:Arial;font\-size:Smaller;width:344px;\">'
t_SPAN_CIERRE = r'</span>'

def t_error(t):
    #print "'%s'" % t.value[0]
    #print( "Lex error: ", t )
    t.lexer.skip(1)
    
#import ply.lex as lex
lexer2 = lex.lex()

# Parsing rules

def p_Elemento(p):
    "elemento : SPAN_INICIO ID SPAN_STYLE DATO SPAN_CIERRE"
    print 'dato = ' + p[4] + '\n'
    
def p_id(p):
    '''ID : ID_CEDULA
          | ID_NOMBRE_COMPLETO
          | ID_SEXO
          | ID_CONOCIDO_COMO
          | ID_FECHA_DE_NACIMIENTO
          | ID_NOMBRE_DEL_PADRE
          | ID_NACIONALIDAD
          | ID_IDENTIFICACION_DEL_PADRE
          | ID_EDAD
          | ID_NOMBRE_DE_LA_MADRE
          | ID_IDENTIFICACION_DE_LA_MADRE'''
          
def p_Dato(p):
    '''DATO : CEDULA
            | NOMBRE_COMPLETO
            | SEXO
            | CONOCIDO_COMO
            | FECHA_DE_NACIMIENTO
            | NOMBRE_DEL_PADRE
            | NACIONALIDAD
            | IDENTIFICACION_DEL_PADRE
            | EDAD
            | NOMBRE_DE_LA_MADRE
            | IDENTIFICACION_DE_LA_MADRE'''

def p_error(p):
    if p:
        pass#print("Syntax error at '%s'" % p.value)
    else:
        pass#print("Syntax error at EOF")

#import ply.yacc as yacc
parser2 = yacc.yacc()
parser2.parse(htmlSource, lexer2)

#//////////////////// LEX/YACC ////////////////////



