# module reglasPaginaTSE.py
# Este modulo contiene las reglas para parsear la pagina de consulta de TSE
# ///////////////////////

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