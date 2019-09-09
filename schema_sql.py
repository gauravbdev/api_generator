pg_schema_cols_sql = """
SELECT lower(c.table_name) table_name, 
        lower(c.column_name) column_name,
                  c.udt_name datatype, t.table_type,
                  case when k.constraint_name is null then 0 
                        else 1 end is_pk
          FROM information_schema.tables t join
                  information_schema.columns c
                   on t.table_name = c.table_name
			and t.table_schema = c.table_schema
                   left join information_schema.key_column_usage k
                          on c.table_name = k.table_name
                         and c.column_name = k.column_name
                         and c.table_schema = k.table_schema
                         and RIGHT(constraint_name, 4) = 'pkey'
         WHERE c.table_schema = '{table_schema}'
                  AND t.table_type = 'BASE TABLE'
          ORDER BY  c.table_name, c.ordinal_position

 """


pg_schema_tables_sql = """
SELECT lower(t.table_name) table_name,
	case when c.table_name is null then 0
		else 1 end has_pk,
	case when kc.table_name is null then 1
		else 0 end insert_pk
FROM information_schema.tables t LEFT JOIN
	(select table_name
	from information_schema.table_constraints c
	where c.constraint_type = 'PRIMARY KEY' 
        and c.table_schema = '{table_schema}'
	group by table_name) c on t.table_name = c.table_name
	LEFT JOIN
	(select kc.table_name
	from information_schema.key_column_usage kc
		join information_schema.columns c
			on kc.constraint_schema = c.table_schema
			and kc.column_name = c.column_name
			and kc.table_name = c.table_name
	where  RIGHT(constraint_name, 4) = 'pkey'
		and c.table_schema = '{table_schema}'
		and column_default like 'nextval%'
	group by kc.table_name) kc on t.table_name = kc.table_name
WHERE t.table_schema = '{table_schema}'
	AND TABLE_TYPE = 'BASE TABLE'
ORDER BY t.table_name
"""


