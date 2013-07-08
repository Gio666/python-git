# --------------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# File: arbol.py
#
# Nehemias Herrera | A52761 | Proyecto Automatas & Compiladores | I-2013 | Luis Quesada
# --------------------------------------------------------------------------------------
import consultaNombre
import consultaCedula
import re, sys, string

# esta funcion dibuja el arbol en un archivo png
def dibuje(arbol):
    import pygraphviz as pgv
    #print A.string() # print to screen
    print "Wrote simple.dot"
    arbol.write('simple.dot') # write to simple.dot
    
    B=pgv.AGraph('simple.dot') # create a new graph from file
    B.layout(prog='dot') # layout with default (neato)
    nombreDeArchivo = 'ancestros.png'
    
    B.draw(nombreDeArchivo) # draw png
    
    # Aqui abrimos la imagen y la mostramos
    from PIL import Image
    f = Image.open(nombreDeArchivo).show()
    
    try:
    from PIL import Image
    f = Image.open(nombreDeArchivo).show()
except ImportError:
    print 'Imagen ancestros.png creada en el directorio de ejecucion de esta aplicacion'

# Esta funciona recibe una lista que se comporta como un arbol binario, dado un elemento x
# su hijo izquierdo esta en la posicion 2 * i + 1 y su hijo derecho en 2 * i + 2
def hacerArbol(lista):
    #aqui creamos el arbol
    import pygraphviz as pgv
    
    # inicializamos el arbol
    arbol=pgv.AGraph(directed=True)
    arbol.graph_attr['label']='Ancestros de ' + lista[0]
    arbol.node_attr['shape']='box'
    arbol.node_attr['style']='rounded'
    arbol.graph_attr['sep']= 0.5
    arbol.graph_attr['overlap']= 'orthoxy'
    arbol.graph_attr['mode'] = 'ipsep'
    arbol.graph_attr['diredgeconstraints'] = 'true'
    cabezaDeFecha = 'none'
    
    tamanio = len(lista)
    indice = 1;
    while (indice < tamanio / 2):
    # sacamos de la lista el trio persona-madre-padre
        persona = string.replace(lista[indice],'Ñ','N')
        madre = string.replace(lista[2 * indice],'Ñ','N')
        padre = string.replace(lista[2 * indice + 1],'Ñ','N')
        
        print 'insertando ' + persona + '|' + madre +'|' + padre
        
        # los agregamos al grafo
        arbol.add_node(persona)
        arbol.add_node(madre)
        arbol.add_node(padre)
        # agregamos un nodo donde unir los 3
        if (persona != 'SIN INFORMACION' and madre != 'SIN INFORMACION' and padre != 'SIN INFORMACION'):
            arbol.add_node(persona + madre + padre, shape = 'point')
            # recuperamos el nodo
            union = arbol.get_node(persona + madre + padre)
            # unimos los 3 en la pega
            arbol.add_edge(madre, union, arrowhead = cabezaDeFecha)
            arbol.add_edge(padre, union, arrowhead = cabezaDeFecha)
            arbol.add_edge(union, persona, arrowhead = cabezaDeFecha)
            
        indice = indice + 1
    
    if (arbol.has_node('SIN INFORMACION')):
            arbol.delete_node(arbol.get_node('SIN INFORMACION'))
    
    #dibujamos el arbol
    dibuje(arbol)
    
def buscarCedulaDePadres(persona):
    # Buscar cedula de la madre si no esta presente
    if (persona.numero_de_cedula_de_la_madre == '0'):
        cedulaMadre = consultaNombre.obtenerCedula(persona.nombre_de_la_madre)
        persona = Persona(nombre_completo = persona.nombre_completo, 
                          numero_de_cedula = persona.numero_de_cedula,  
                          nombre_del_padre = persona.nombre_del_padre,
                          numero_de_cedula_del_padre = persona.numero_de_cedula_del_padre,
                          nombre_de_la_madre  = persona.nombre_de_la_madre,
                          numero_de_cedula_de_la_madre = cedulaMadre )
    
    
    # Buscar cedula del padre si no esta presente
    if (persona.numero_de_cedula_del_padre == '0'):
        cedulaPadre = consultaNombre.obtenerCedula(persona.nombre_del_padre)
        persona = Persona(nombre_completo = persona.nombre_completo, 
                          numero_de_cedula = persona.numero_de_cedula,  
                          nombre_del_padre = persona.nombre_del_padre,
                          numero_de_cedula_del_padre = cedulaPadre,
                          nombre_de_la_madre  = persona.nombre_de_la_madre,
                          numero_de_cedula_de_la_madre = persona.numero_de_cedula_de_la_madre )
    
    return persona

# ////////////////////////////////////////////////////////////////////////
# ////////////////////////////////  MAIN  ////////////////////////////////
# ////////////////////////////////////////////////////////////////////////
from collections import namedtuple
Persona = namedtuple("Persona", "nombre_completo numero_de_cedula nombre_del_padre numero_de_cedula_del_padre nombre_de_la_madre numero_de_cedula_de_la_madre")

# recibimos la cedula como parametro
cedula = str(sys.argv[1])

# Listas para almacenar nombres y sus respectivos numeros de cedula
listaNombre = []
listaCedula = []
# vamos a contar a partir de 1
listaNombre.insert(0,None)
listaCedula.insert(0,None)
indice = 1
# buscamos datos de la primer persona
persona = consultaCedula.obtenerPersona(cedula)
# agregamos la primer persona
listaNombre.append(persona.nombre_completo)
listaCedula.append(persona.numero_de_cedula)
# enclochese
while (indice <= 30 ): 
    if (listaCedula[indice] == '0' and listaNombre[indice] != 'SIN INFORMACION'):
        listaCedula[indice] = consultaNombre.obtenerCedula(listaNombre[indice])
    
    if (listaCedula[indice] != '0'):
        
        persona = consultaCedula.obtenerPersona(listaCedula[indice])
        
        #madre
        listaNombre.insert(2 * indice, persona.nombre_de_la_madre)
        listaCedula.insert(2 * indice, persona.numero_de_cedula_de_la_madre)
        
        #padre
        listaNombre.insert(2 * indice + 1, persona.nombre_del_padre)
        listaCedula.insert(2 * indice + 1, persona.numero_de_cedula_del_padre)
        
    else:
        
        # mama de relleno
        listaNombre.insert(2 * indice, 'SIN INFORMACION')
        listaCedula.insert(2 * indice, '0')
        # papa de relleno
        listaNombre.insert(2 * indice + 1, 'SIN INFORMACION')
        listaCedula.insert(2 * indice + 1, '0')
        
    print listaNombre
    if (listaCedula[indice] != '0'):
        hacerArbol(listaNombre)
    indice = indice + 1
    

hacerArbol(listaNombre)