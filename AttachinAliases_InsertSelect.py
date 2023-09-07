from sqlglot import parse_one, expressions

query = """
insert into trg_table (
  col_name1,
  col_name2,
  col_name3
)
select
  1,
 '2' as cars,
  3 bicicles
from dual
"""

parsed = parse_one(query)

i = 0
aliases = []
inserts = []

for insert in parsed.find_all(expressions.Insert):
  inserts.append(insert)

for al in inserts[0].this.expressions:
  aliases.append(al.alias_or_name)

for col in parsed.expression.expressions:
  i = i + 1
  col.replace(expressions.alias_(col, aliases[i-1]))


print ("------------------")

print((parsed.sql(pretty = True)))
