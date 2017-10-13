var grpc = require('grpc');
var quickstepGRPC = grpc.load("../../cli/NetworkCli.proto").quickstep;

var quickstep={
  ip:"localhost",
  port:"3000",

  sql_to_text:function(query,callback)
  {
    var client = new quickstepGRPC.NetworkCli(quickstep.ip+":"+quickstep.port,
                                         grpc.credentials.createInsecure());

    client.sendQuery({"query": query}, function(err, response) {
      if(response)
      {
        callback(response.query_result,response.error_result);
      }
      else {
        callback("","ERROR: No response received from quickstep database.");
      }
    });
  },

  sql_to_table:function(query,callback)
  {
    this.sql_to_text(query,function(result,error)
    {
      if(error.indexOf("ERROR")!=-1)
      {
        callback("",error);
        return;
      }

      if(!result || result[0]!="+")
      {
        return [];
      }

      var rows=result.split("\n");
      var columnNames=rows[1].split("|");
      columnNames=columnNames.map(Function.prototype.call,String.prototype.trim);

      var dataTable=[];
      console.log(result);
      for(var j=3;j<rows.length-3;j++)
      {
        var values=rows[j].split("|");
        dataTable[j-3]={};
        for(var k=1;k<columnNames.length-1;k++)
        {
          dataTable[j-3][columnNames[k].trim()]=values[k].trim();
        }
      }

      callback(dataTable,"");
    });
  },

  tables:function(callback)
  {
    this.sql_to_text("\\d",function(result,error)
    {
      if(error.indexOf("ERROR")!=-1)
      {
        callback("",error);
        return;
      }

      var rows=result.split("\n");
      var columnNames=["name","type","block"];
      var dataTable=[];
      console.log(result);
      for(var j=4;j<rows.length-2;j++)
      {
        var values=rows[j].split("|");
        dataTable[j-4]={};
        for(var k=0;k<columnNames.length;k++)
        {
          dataTable[j-4][columnNames[k].trim()]=values[k].trim();
        }
      }

      callback(dataTable,"");
    });
  },

  columns:function(table, callback)
  {
    this.sql_to_text("\\d "+table,function(result,error)
    {
      if(error.indexOf("ERROR")!=-1)
      {
        callback("",error);
        return;
      }

      var rows=result.split("\n");
      var columnNames=["name","type"];
      var dataTable=[];
      console.log(result);

      for(var j=3;j<rows.length-1;j++)
      {
        var values=rows[j].split("|");
        dataTable[j-3]={};
        for(var k=0;k<columnNames.length;k++)
        {
          dataTable[j-3][columnNames[k].trim()]=values[k].trim();
        }
      }

      callback(dataTable,"");
    });
  },

  rows:function(table,count="ALL",callback)
  {
    var limitString= count!="ALL" ? " LIMIT "+count : "";
    context=this;
    context.columns(table,function(columnData,error){
        if(error.indexOf("ERROR")!=-1)
        {
          callback("",error);
          return;
        }
        var sqlString="SELECT * FROM "+table+
          " ORDER BY "+columnData[0].name +
          limitString+";";
        context.sql_to_table(sqlString,function(rowData,error){
          if(error.indexOf("ERROR")!=-1)
          {
            callback("",error);
          }
          callback(rowData,"");
        });
    });
  }
};

module.exports=quickstep;
