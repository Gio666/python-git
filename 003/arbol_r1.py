# --------------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
# File: arbol.py
#
# Nehemias Herrera | A52761 | Proyecto Automatas & Compiladores | I-2013 | Luis Quesada
# --------------------------------------------------------------------------------------
import consultaNombre
import consultaCedula
import re, sys

# esta funcion dibuja el arbol en un archivo png
def dibuje(arbol):
    import pygraphviz as pgv
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
# su hijo izquierdo esta en la posicion 2 * i + 1 y su hijo derecho en 2 * i + 2
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
    
    # agregamos la familia al arbol
    for p in lista:
        if (p != None):
            # sacamos de la lista el trio persona-madre-padre
            persona = p.nombre_completo
            madre = p.nombre_de_la_madre
            padre = p.nombre_del_padre
            # los agregamos al grafo
            arbol.add_node(persona)
            arbol.add_node(madre)
            arbol.add_node(padre)
            # agregamos un nodo donde unir los 3
            arbol.add_node(persona + madre + padre, shape = 'point')
            # recuperamos el nodo
            union = arbol.get_node(persona + madre + padre)
            # unimos los 3 en la pega
            arbol.add_edge(madre, union, arrowhead = cabezaDeFecha)
            arbol.add_edge(padre, union, arrowhead = cabezaDeFecha)
            arbol.add_edge(union, persona, arrowhead = cabezaDeFecha)
        
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

# esta lista contendra la familia
familia = []
familia.insert(0, None)
# insertamos al primer miembro de la familia, la persona a quien corresponda el numero de cedula ingresado
familia.append(buscarCedulaDePadres(consultaCedula.obtenerPersona(cedula)))
print 'familia[0] >> ' + str(familia[0])
seguir = True
indice = 1
while (indice < 4):
    print 'indice >>>>>>>>> ' + str(indice)
    if (familia[indice] != None):
        cedulaMadre = familia[indice].numero_de_cedula_de_la_madre
        print 'cedula mama >> ' + str (cedulaMadre)
        cedulaPadre = familia[indice].numero_de_cedula_del_padre
        print 'cedula papa >> ' + str (cedulaPadre)
        
        if cedulaMadre != '0':
            familia.append(buscarCedulaDePadres(consultaCedula.obtenerPersona(cedulaMadre)))
        else:
            print 'Sin informacion de cedula para '
            familia.append(None)
            
        if cedulaPadre != '0':
            familia.append(buscarCedulaDePadres(consultaCedula.obtenerPersona(cedulaPadre)))
        else:
            familia.append(None)
            print 'cedula papa es cero'
            
    print 'familia[' + str(indice) + '] >> ' + str(familia[indice])
    indice = indice + 1


hacerArbol(familia)    