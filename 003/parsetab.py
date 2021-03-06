
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\x86\xd8\xfd\xcam\x9e\x02Y\x8b\xa6\x01\xbfY\x84_\xa0'
    
_lr_action_items = {'SPAN_STYLE':([12,13,20,21,26,27,],[22,23,28,29,32,33,]),'ID_NOMBRE_DE_LA_MADRE':([19,],[26,]),'ID_NOMBRE_DEL_PADRE':([11,],[20,]),'SPAN_CIERRE':([30,31,34,35,38,39,],[36,37,40,41,42,43,]),'ID_IDENTIFICACION_DE_LA_MADRE':([19,25,],[27,27,]),'ID_NOMBRE_COMPLETO':([5,7,],[12,12,]),'ID_IDENTIFICACION_DEL_PADRE':([11,15,],[21,21,]),'NOMBRE':([22,28,32,],[30,34,38,]),'$end':([3,16,17,18,24,42,43,],[0,-1,-12,-13,-14,-15,-16,]),'SPAN_INICIO':([0,1,2,4,6,8,9,10,14,17,36,37,40,41,42,],[5,7,-4,11,-2,15,-9,19,-7,25,-6,-5,-10,-11,-15,]),'CEDULA':([23,29,33,],[31,35,39,]),'ID_CEDULA':([5,],[13,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'nombre_del_padre':([4,],[8,]),'cedula_de_la_madre':([10,17,],[18,24,]),'nombre_de_la_madre':([10,],[17,]),'cedula_de_la_persona':([0,],[1,]),'nombre_de_la_persona':([0,1,],[2,6,]),'cedula_del_padre':([4,8,],[9,14,]),'datos':([0,],[3,]),'datos_de_la_persona':([0,],[4,]),'datos_del_padre':([4,],[10,]),'datos_de_la_madre':([10,],[16,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> datos","S'",1,None,None,None),
  ('datos -> datos_de_la_persona datos_del_padre datos_de_la_madre','datos',3,'p_datos','/Users/yo/Desktop/python/003/consultaCedula.py',133),
  ('datos_de_la_persona -> cedula_de_la_persona nombre_de_la_persona','datos_de_la_persona',2,'p_datos_de_la_persona','/Users/yo/Desktop/python/003/consultaCedula.py',136),
  ('datos_de_la_persona -> cedula_de_la_persona','datos_de_la_persona',1,'p_datos_de_la_persona','/Users/yo/Desktop/python/003/consultaCedula.py',137),
  ('datos_de_la_persona -> nombre_de_la_persona','datos_de_la_persona',1,'p_datos_de_la_persona','/Users/yo/Desktop/python/003/consultaCedula.py',138),
  ('cedula_de_la_persona -> SPAN_INICIO ID_CEDULA SPAN_STYLE CEDULA SPAN_CIERRE','cedula_de_la_persona',5,'p_cedula_de_la_persona','/Users/yo/Desktop/python/003/consultaCedula.py',141),
  ('nombre_de_la_persona -> SPAN_INICIO ID_NOMBRE_COMPLETO SPAN_STYLE NOMBRE SPAN_CIERRE','nombre_de_la_persona',5,'p_nombre_de_la_persona','/Users/yo/Desktop/python/003/consultaCedula.py',147),
  ('datos_del_padre -> nombre_del_padre cedula_del_padre','datos_del_padre',2,'p_datos_del_padre','/Users/yo/Desktop/python/003/consultaCedula.py',153),
  ('datos_del_padre -> nombre_del_padre','datos_del_padre',1,'p_datos_del_padre','/Users/yo/Desktop/python/003/consultaCedula.py',154),
  ('datos_del_padre -> cedula_del_padre','datos_del_padre',1,'p_datos_del_padre','/Users/yo/Desktop/python/003/consultaCedula.py',155),
  ('nombre_del_padre -> SPAN_INICIO ID_NOMBRE_DEL_PADRE SPAN_STYLE NOMBRE SPAN_CIERRE','nombre_del_padre',5,'p_nombre_del_padre','/Users/yo/Desktop/python/003/consultaCedula.py',158),
  ('cedula_del_padre -> SPAN_INICIO ID_IDENTIFICACION_DEL_PADRE SPAN_STYLE CEDULA SPAN_CIERRE','cedula_del_padre',5,'p_cedula_del_padre','/Users/yo/Desktop/python/003/consultaCedula.py',164),
  ('datos_de_la_madre -> nombre_de_la_madre','datos_de_la_madre',1,'p_datos_de_la_madre','/Users/yo/Desktop/python/003/consultaCedula.py',172),
  ('datos_de_la_madre -> cedula_de_la_madre','datos_de_la_madre',1,'p_datos_de_la_madre','/Users/yo/Desktop/python/003/consultaCedula.py',173),
  ('datos_de_la_madre -> nombre_de_la_madre cedula_de_la_madre','datos_de_la_madre',2,'p_datos_de_la_madre','/Users/yo/Desktop/python/003/consultaCedula.py',174),
  ('nombre_de_la_madre -> SPAN_INICIO ID_NOMBRE_DE_LA_MADRE SPAN_STYLE NOMBRE SPAN_CIERRE','nombre_de_la_madre',5,'p_nombre_de_la_madre','/Users/yo/Desktop/python/003/consultaCedula.py',177),
  ('cedula_de_la_madre -> SPAN_INICIO ID_IDENTIFICACION_DE_LA_MADRE SPAN_STYLE CEDULA SPAN_CIERRE','cedula_de_la_madre',5,'p_cedula_de_la_madre','/Users/yo/Desktop/python/003/consultaCedula.py',183),
]
