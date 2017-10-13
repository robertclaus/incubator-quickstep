import quickstep as q

relationships= [{'parent': "Bob", 'child': "LittleBob"},
                {'parent': "LittleBob", 'child': "LittlestBob"},
                {'parent': "Henry", 'child': "LittleHenry"},
                {'parent': "Greg", 'child': "LittleGreg"},
                ]
try:
    q.sql_to_table("CREATE TABLE parentChildRelationship (parent varchar(15), child varchar(15));")
except ValueError:
    q.sql_to_table("DROP TABLE parentChildRelationship;")
    q.sql_to_table("CREATE TABLE parentChildRelationship (parent varchar(15), child varchar(15));")

for relation in relationships:
    q.sql_to_table("INSERT INTO parentChildRelationship VALUES ('" + relation['parent'] + "','" + relation['child'] + "');")

df=q.sql_to_table("SELECT * FROM parentChildRelationship;")
print(df)