import sys
sys.path.append("../..")
import quickstep as q
import time as t

try:
    q.sql_to_table("CREATE TABLE numberExamples (num Integer);")
except ValueError:
    print("Table already exists")
    #q.sql_to_table("DROP TABLE numberExamples;")
    #q.sql_to_table("CREATE TABLE numberExamples (num Integer);")

start=t.time()

for x in range(0,200):
    q.sql_to_table("INSERT INTO numberExamples VALUES (" + str(x) + ");")
    if x%10==0:
        print("Insert: "+str(x)+" at time: "+str(t.time()-start))

df=q.sql_to_table("SELECT * FROM numberExamples;")
print(df)
print("Total took: "+str(t.time()-start))