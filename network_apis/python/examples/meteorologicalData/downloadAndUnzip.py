import quickstep as q
import urllib
import zipfile
import os
import csv
import StringIO

frequency="hourly"
type="WIND"
year=2016
tableName="wind"

print("Starting download")
filename=frequency+"_"+str(type)+"_"+str(year)+".zip"
urllib.urlretrieve("https://aqsdr1.epa.gov/aqsweb/aqstmp/airdata/"+filename,filename)
print("Download complete")

print("Starting unzip")
zip=zipfile.ZipFile(filename,"r")
zip.extractall()
zip.close()
os.remove(filename)
print("Completed unzip")

print("Starting load")
fullFileName=os.getcwd()+"/"+frequency+"_"+str(type)+"_"+str(year)+".csv"

if not any(x['name']==tableName for x in q.tables()):
    print("  Creating Table")
    f=open(fullFileName)
    headers = f.readline()
    headers = StringIO.StringIO(headers)
    headerObj = csv.reader(headers)
    createQuery = "CREATE TABLE "+tableName+" ("
    for row in headerObj:
        for headerName in row:
            headerName=headerName.replace(" ","_")
            createQuery = createQuery+""+headerName+" varchar(50),"
    createQuery=createQuery[:-1]+");"
    q.sql_to_text(createQuery)
    print("  Table Created")


query="COPY "+tableName+" FROM '"+fullFileName+"' WITH (DELIMITER ',');"
print(q.sql_to_text(query))
print("Completed Load")

#print(q.sql_to_text("SELECT * FROM temp;"))