
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSleftTIMESDIVIDEleftCONCATCOLON COMMA COMMENT CONCAT DIVIDE END EQUALS FUNC ID INPUT LBRACKET LPAREN MINUS MULTILINE_COMMENT NUMBER PLUS PRINT RANDOM RBRACKET RPAREN SEMICOLON STRING TIMESstatements : statements statement\n                  | statementstatement : ID EQUALS expression SEMICOLONstatement : ID EQUALS STRING SEMICOLONstatement : PRINT LPAREN STRING RPAREN SEMICOLONstatement : PRINT LPAREN expression RPAREN SEMICOLONstatement : expression SEMICOLONexpression : expression PLUS expression\n                  | expression MINUS expression\n                  | expression TIMES expression\n                  | expression DIVIDE expressionexpression : expression CONCAT expressionexpression : LPAREN expression RPARENexpression : STRINGexpression : NUMBERexpression : ID'
    
_lr_action_items = {'ID':([0,1,2,7,9,10,11,12,13,14,15,16,17,30,31,34,35,],[3,3,-2,19,-1,19,-7,19,19,19,19,19,19,-3,-4,-5,-6,]),'PRINT':([0,1,2,9,11,30,31,34,35,],[6,6,-2,-1,-7,-3,-4,-5,-6,]),'LPAREN':([0,1,2,6,7,9,10,11,12,13,14,15,16,17,30,31,34,35,],[7,7,-2,17,7,-1,7,-7,7,7,7,7,7,7,-3,-4,-5,-6,]),'STRING':([0,1,2,7,9,10,11,12,13,14,15,16,17,30,31,34,35,],[5,5,-2,5,-1,21,-7,5,5,5,5,5,27,-3,-4,-5,-6,]),'NUMBER':([0,1,2,7,9,10,11,12,13,14,15,16,17,30,31,34,35,],[8,8,-2,8,-1,8,-7,8,8,8,8,8,8,-3,-4,-5,-6,]),'$end':([1,2,9,11,30,31,34,35,],[0,-2,-1,-7,-3,-4,-5,-6,]),'EQUALS':([3,],[10,]),'SEMICOLON':([3,4,5,8,19,20,21,22,23,24,25,26,29,32,33,],[-16,11,-14,-15,-16,30,31,-8,-9,-10,-11,-12,-13,34,35,]),'PLUS':([3,4,5,8,18,19,20,21,22,23,24,25,26,27,28,29,],[-16,12,-14,-15,12,-16,12,-14,-8,-9,-10,-11,-12,-14,12,-13,]),'MINUS':([3,4,5,8,18,19,20,21,22,23,24,25,26,27,28,29,],[-16,13,-14,-15,13,-16,13,-14,-8,-9,-10,-11,-12,-14,13,-13,]),'TIMES':([3,4,5,8,18,19,20,21,22,23,24,25,26,27,28,29,],[-16,14,-14,-15,14,-16,14,-14,14,14,-10,-11,-12,-14,14,-13,]),'DIVIDE':([3,4,5,8,18,19,20,21,22,23,24,25,26,27,28,29,],[-16,15,-14,-15,15,-16,15,-14,15,15,-10,-11,-12,-14,15,-13,]),'CONCAT':([3,4,5,8,18,19,20,21,22,23,24,25,26,27,28,29,],[-16,16,-14,-15,16,-16,16,-14,16,16,16,16,-12,-14,16,-13,]),'RPAREN':([5,8,18,19,22,23,24,25,26,27,28,29,],[-14,-15,29,-16,-8,-9,-10,-11,-12,32,33,-13,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statements':([0,],[1,]),'statement':([0,1,],[2,9,]),'expression':([0,1,7,10,12,13,14,15,16,17,],[4,4,18,20,22,23,24,25,26,28,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statements","S'",1,None,None,None),
  ('statements -> statements statement','statements',2,'p_statements','cparser.py',22),
  ('statements -> statement','statements',1,'p_statements','cparser.py',23),
  ('statement -> ID EQUALS expression SEMICOLON','statement',4,'p_statement_assign','cparser.py',27),
  ('statement -> ID EQUALS STRING SEMICOLON','statement',4,'p_statement_assign_string','cparser.py',35),
  ('statement -> PRINT LPAREN STRING RPAREN SEMICOLON','statement',5,'p_statement_print_string','cparser.py',39),
  ('statement -> PRINT LPAREN expression RPAREN SEMICOLON','statement',5,'p_statement_print_expr','cparser.py',43),
  ('statement -> expression SEMICOLON','statement',2,'p_statement_expr','cparser.py',47),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','cparser.py',51),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','cparser.py',52),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','cparser.py',53),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','cparser.py',54),
  ('expression -> expression CONCAT expression','expression',3,'p_expression_concat','cparser.py',65),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','cparser.py',74),
  ('expression -> STRING','expression',1,'p_expression_string','cparser.py',78),
  ('expression -> NUMBER','expression',1,'p_expression_number','cparser.py',82),
  ('expression -> ID','expression',1,'p_expression_id','cparser.py',86),
]
