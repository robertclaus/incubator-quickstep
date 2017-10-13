import quickstep as q
import urllib2

try:
    q.sql_to_table("CREATE TABLE person (firstName varchar(15), lastName varchar(15));")
except ValueError: #Table already exists, so drop and create for example
    q.sql_to_table("DROP TABLE person;")
    q.sql_to_table("CREATE TABLE person (firstName varchar(15), lastName varchar(15));")

nameCount=50
#Returns a list of names according to get parameters, which we then store to quickstep.
page=urllib2.urlopen("http://names.drycodes.com/"+str(nameCount)+"?nameOptions=boy_names")

names=page.readline()[1:-1].split(',')

sqlString="";

#Could also build the INSERT dynamically to reduce network overhead.
for name in names:
    name=name[1:-1].split('_')
    sqlString=sqlString+"INSERT INTO person VALUES ('"+name[0]+"','"+name[1]+"'); "

q.sql_to_table(sqlString)

df=q.sql_to_table("SELECT * FROM person;")
print(df)