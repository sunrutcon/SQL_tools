# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 14:13:20 2023

@author: hragsl

Parsiraj CASE when blok i kreiraj excel tablicu iz njega
 1. parsiraj Case when i kreiraj AST
 2. idi kroz AST rekurzivno i kreiraj listu sa then vrijednostima i expressionima
   - gledamo koje kolone i vrijednosti daju određeni output (then vrijednost)
 3. na temelju kolona i vriejdnosti koje mogu poprimiti, radimo produkt, kako bi dobili sve moguće kombinacije
 4. kreiramo pandas data frame tablicu 
 5. ispisujemo tu tablicu na disk u xlsx format
"""

# https://github.com/tobymao/sqlglot

from sqlglot import parse_one
from sqlglot import expressions
import itertools

#print(repr(parse_one("SELECT a + 1 AS z")))


queryes = [
## 0
"""
  CASE
    WHEN code1 = '5540c-1' THEN 'CSH-DOM-EX1'
    when code2 in ('5540c2','5540c3') then 'WIR-DOM-EX2'
    when amo in (1,2) and code2 in ('5540c2','5540c3') and aa = 'asd' then 'WIR-DOM-EX2'
    else '*n.a.*'
  END
""",
## 1
"""
  CASE
    WHEN code1 = '5540c-1' THEN
      case WHEN code2 = '5540c-2' THEN 'CSH-DOM-EX1' end
    else '*n.a.*'
  END
""",
## 2
"""
  CASE
    WHEN code1 = '5540c-1' THEN
      'CSH-DOM-EX1'
    else '*n.a.*'
  END
""",
## 3 
"""
CASE
  WHEN trim(SIP_TURNOVER_TYPE_DEF.code) IN ('5540c', '5540cs')
  AND trim(SIP_TURNOVER_DEF.amo_type) IN ('100', '102', '623') THEN 'CSH-DOM-EX1'
  WHEN trim(SIP_TURNOVER_TYPE_DEF.code) IN ('5511c', '5511cs')
  AND trim(SIP_PAYMENT_ORDER_DEF.source_code) = 'AD' THEN 'CSH-DOM-EX2'
  WHEN trim(SIP_TURNOVER_TYPE_DEF.code) IN ('1123d', '1123ds', '1144d', '1144ds') THEN 'CSH-DOM-EX3'
END
""",
## 4
"""
CASE
  WHEN trim(SIP_TURNOVER_TYPE_DEF.code) IN ('5540c', '5540cs')
  AND trim(SIP_TURNOVER_DEF.amo_type) IN ('100', '102', '623') THEN 'CSH-DOM-EX'
  WHEN trim(SIP_TURNOVER_TYPE_DEF.code) IN ('1123d', '1123ds', '1144d', '1144ds') THEN 'CSH-DOM-EX'
  WHEN trim(SIP_TURNOVER_TYPE_DEF.code) IN ('5078c', '5078d', '5099c', '5099d') THEN 
    CASE
      WHEN SIP_PAYMENT_ORDER_DEF.pay_ord_id IS NOT NULL THEN 'OTH-DOM-CL'
      ELSE 'OTH-DOM-EX'
    END
END
""",
]

query = queryes[8]

file_name_sufix = 'SDA'

print (" ==== start ==== ")
pores = parse_one(query)
repr_pores = repr(pores)

#w = pores.walk(bfs=False)

#print(repr(w))

print(repr(pores))

#i = 0;

#steps = []
#cases = []

#quote_strings = False

print()
print("--- sql: ---")
print()


class_list_expr = (expressions.Expression)

node_list = []
col_list = []
col_comb = []
col_list1 = []

col_list_helper = []

col_list1_hist = []

kolone = []

def parse_node(p_node, p_depth_max):
  global col_list
  node_list.append([p_node.alias_or_name, p_node])
  if p_node.depth > p_depth_max:
    return
  elif not isinstance(p_node, expressions.Expression):
    print(' '*2*p_node.depth + str(type(p_node)) + ' [depth=unknown]')
  else:
    print(' '*2*p_node.depth + str(type(p_node)) + ' [depth=' + str(p_node.depth) + ']'+ ' ## <' + p_node.alias_or_name + '> ##')
    #if isinstance(p_node, expressions.If) and p_node.depth == 1:
    #  col_list.clear()
    #### TEHN value ####
    if isinstance(p_node, expressions.Literal) and (isinstance(p_node.parent, expressions.If) or isinstance(p_node.parent, expressions.Case)):
      col_list.append([p_node.depth, p_node.alias_or_name])
      col_comb.append(col_list.copy())
      col_list1 = [c for c in col_list if c[0]<p_node.depth]
      col_list1_hist.append(col_list1.copy())
      col_list = col_list1.copy()
      #col_list.clear()
    #if isinstance(p_node, expressions.Identifier) and isinstance(p_node.parent, expressions.Column):
    #  col_list.append(p_node.alias_or_name)
    #### IS ####
    if isinstance(p_node, expressions.Is) and isinstance(p_node.left, expressions.Column) and isinstance(p_node.right, expressions.Null):
      if isinstance(p_node.parent, expressions.Not):
        col_list.append([p_node.depth, p_node.left.alias_or_name, ['NOT NULL']])
      else:
        col_list.append([p_node.depth, p_node.left.alias_or_name, ['NULL']])
    #### EQ ####
    if isinstance(p_node, expressions.EQ) and isinstance(p_node.left, expressions.Expression) and isinstance(p_node.right, expressions.Literal):
      col_list.append([p_node.depth, p_node.left.sql(), [p_node.right.alias_or_name]])
    ### EQ + trim ###
    #if isinstance(p_node, expressions.EQ) and isinstance(p_node.left, expressions.Trim) and isinstance(p_node.right, expressions.Literal):
    #  col_list.append([p_node.depth, p_node.left.this.alias_or_name, [p_node.right.alias_or_name]])
    #### IN ####
    #if isinstance(p_node, expressions.In) and isinstance(p_node.this, expressions.Column) and isinstance(p_node.expressions, list):
    if isinstance(p_node, expressions.In) and isinstance(p_node.expressions, list):
      val_list = []
      for e in p_node.expressions:
        #col_list.append([e.depth, p_node.this.this.alias_or_name, e.alias_or_name ])
        val_list.append(e.alias_or_name)
      #if p_node.this.this is not None: # očekujemo da je this.this = Column
      #  col_list.append([e.depth, p_node.this.this.alias_or_name, val_list ])
      #else: # ako nije this.this = Column, onda uzmi exproession ili nađi kolonu
        #kolone.clear()
        #for col in p_node.this.find_all(expressions.Column):
        #  kolone.append(col.alias_or_name)
      # idemo na p_node.this.sql() jer ne mora nužno to bit kolona, može biti izraz npr trim(kolona) pa uzimamo cijeli izraz
      # time smo se riješili gornje if-else logike i provjere da li je to kolona
      col_list.append([e.depth, p_node.this.sql(), val_list ])
      #print('--test--')
    for key in p_node.args.keys():
      arg_node = p_node.args.get(key)
      if isinstance(arg_node, class_list_expr):
        #print(type(p_node.args.get(key)))
        parse_node(arg_node, p_depth_max )
      if isinstance(arg_node, list):
        for an in arg_node:
          if isinstance(an, class_list_expr):
            parse_node(an, p_depth_max )
          else:
            print(type(an))
    # if isinstance(p_node, expressions.Literal) and isinstance(p_node.parent, expressions.If):
    #   print(p_node.alias_or_name)

parse_node(pores,10)

print()
print('-- res ---')
print()

"""
for lii in col_comb:
  print (lii[-1][1])
  for cv in lii[:-1]:
    print ("  " + str(cv[1:]))
"""

coco = []

for cc in col_comb:
  c = []
  c.append(cc[-1][1])
  #coco.append(c)
  kv_dic = {}
  for kv in cc[:-1]:
    kv_dic[kv[1]] = kv[2]
  coco.append([cc[-1][1], kv_dic])

coco1 = []

for ko in coco:
  print (ko[0])
  ttc = ko[0]
  col_names = []
  col_vals = []
  col_prod = []
  for koky in ko[1].keys():
    col_names.append(koky)
    print("  " + koky + " : " + str(ko[1].get(koky)))
    col_vals.append(ko[1].get(koky))
  col_prod = list(itertools.product(*col_vals))
  coco1.append([ttc, col_names, col_prod])

pd_rows = []

for c_row in coco1: # idemo po svim txn_type_codeovima 
  if c_row[0] != '*n.a.*':
    for cn in range(len(c_row[2])): # idemo po svim kombinacijama vrijednosti
      col_names = c_row[1]
      col_values = c_row[2][cn]
      pd_row = {'TXN_TYPE_CODE': c_row[0]}
      for v in range(len(c_row[1])): # idemo po svim kolonama vrijednosti 
        pd_row[col_names[v]] = col_values[v]
      pd_rows.append(pd_row)

import pandas as pd


df = pd.DataFrame(pd_rows)

df.to_excel("path/to/directory/" + file_name_sufix + "_" + str(id(pores)) + ".xlsx")

