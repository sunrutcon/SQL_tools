# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 00:46:38 2023

@author: hragsl

Uzima SQL upit i traži alias TXN_TYPE_CODE i sql koji se nalazi ispod tog aliasa
 - nakon toga traži alias load_job_id i njegovu vrijednost te to kači kao komentar poviše ovog prvog
 - na taj način smo napravili kontrolu da case when paše jobu, kako nebi greškom uzeli neki drugi sql

"""

from sqlglot import parse_one, exp

query = """
SELECT
  'COM' AS COST_CNT_APPLICATION_ID,
  (
    CASE
      WHEN trim(TURNOVER_TYPE_DEF.code) IN ('3145c', '3145d') THEN 'FCR-DOM-CL'
      WHEN trim(TURNOVER_TYPE_DEF.code) = '3805c' THEN 'WIR-INT-EX'
      ELSE NULL
    END
  ) AS TXN_TYPE_CODE,
  'ENTITY_JOB_NAME' AS LOAD_JOB_ID
FROM TURNOVER_TYPE_DEF 
WHERE
  (
    TURNOVER_TYPE_DEF.ban_rel_type IN ('016', '017')
    AND TURNOVER_TYPE_DEF.amo_type IN ('900', '902', '904')
  )
"""

comment_expression_alias = 'LOAD_JOB_ID'
target_expression_alias = 'TXN_TYPE_CODE'

parsed = parse_one(query)

repr_parsed = repr(parsed)

#print(parsed.sql())

projs = []

# find all projections in select statements (a and c)
for select in parse_one(query).find_all(exp.Select):
    for projection in select.expressions:
      if projection.alias_or_name == comment_expression_alias:
        projs.append(projection.sql())
      if projection.alias_or_name == target_expression_alias:
        print(projection.alias_or_name + " id:" + str(id(projection)))
        projs.append('-- ' + str(id(projection)) + '\n' + projection.sql(pretty=True))
        # projs.append(projection)

case_when = '-- ' + projs[1] + '\n' + projs[0]
