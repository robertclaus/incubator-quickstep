var quickstep=require('./quickstep.js')

const express = require('express')
const app = express()
app.use(express.static(__dirname));

app.get('/',function(req,res){
  res.sendFile("index.html");
})

app.get('/genericTableQuery',function(req,res){
  quickstep.sql_to_table(req.query.queryString,function(result,error)
  {
    res.setHeader('Content-Type','application/json');
    res.send(JSON.stringify({'result':result,'error':error}));
  });
})

app.get('/genericQuery',function(req,res){
  quickstep.run_quickstep_message(req.query.queryString,function(result,error)
  {
    res.setHeader('Content-Type','application/json');
    res.send(JSON.stringify({'result':result,'error':error}));
  });
})


//Initialization Code

//Command line port
var port=8000;
process.argv.forEach(function(val, index){
  if(val.indexOf("port=")!=-1)
  {
    port=val.substring(val.indexOf("port=")+5);
    console.log("Command line port parameter: "+port);
  }
});
//Start server
app.listen(port,function(){
  console.log("Initializing Web Server on port "+port);
})
