
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = 'k\xae^\x04\x1d\x01\xb4\x97\x8c\x0f\xc7\x97\xdb\x95A\x95'
    
_lr_action_items = {'NOMBRE':([5,],[6,]),'PARTE_IZQUIERDA_LABEL':([0,2,7,],[3,3,-3,]),'PARTE_DERECHA_LABEL':([6,],[7,]),'CEDULA':([3,],[5,]),'$end':([1,2,4,7,],[0,-2,-1,-3,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'nombres':([0,2,],[1,4,]),'nombre':([0,2,],[2,2,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> nombres","S'",1,None,None,None),
  ('nombres -> nombre nombres','nombres',2,'p_nombres','/Users/yo/Desktop/proyecto A&C/consultaNombre.py',129),
  ('nombres -> nombre','nombres',1,'p_nombres','/Users/yo/Desktop/proyecto A&C/consultaNombre.py',130),
  ('nombre -> PARTE_IZQUIERDA_LABEL CEDULA NOMBRE PARTE_DERECHA_LABEL','nombre',4,'p_nombre','/Users/yo/Desktop/proyecto A&C/consultaNombre.py',133),
]
