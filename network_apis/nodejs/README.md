# Python API for Quickstep Database Access

## Getting Started
The node.js quickstep library gives easy access to the quickstep network command line interface.

### Prerequisites
* Node
* Node Express Library (for the example only)
* GRPC Library for Node (https://grpc.io/docs/quickstart/node.html)
* protobuf functionality (bundled with grpc)
* Quickstep compiled for network CLI using cmake flag -ENABLE_NETWORK_CLI=true
* quickstep_cli_shell running with the commandline flag -mode=network

### Installing
Add the following file to your project:  
quickstep.js

### Configuration
Add "var q=require('./quickstep.js')" at the top of your project.  Set q.ip and q.port appropriately for your quickstep server.  By default it will assume node is running on the same machine using the default port.

### Examples
The example demonstrates a simple webpage that connects to the quickstep database.  
In general SQL should not be passed from the client, but in this case it is a proof of concept client-server-database example.
