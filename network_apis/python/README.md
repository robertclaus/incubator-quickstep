# Python API for Quickstep Database Access

## Getting Started
The python quickstep library gives easy access to the quickstep network command line interface.

### Prerequisites
* Python 2.7
* GRPC Library for Python (https://grpc.io/docs/quickstart/python.html)
* Pandas Library for Python
* protobuf functionality (bundled with grpc)
* Quickstep compiled for network CLI using cmake flag -ENABLE_NETWORK_CLI=true
* quickstep_cli_shell running with the commandline flag -mode=network

### Installing
Add the following files to your project:  
  
quickstep.py  
NetworkCli_pb2.py  
NetworkCli_pb2_grpc.py

### Configuration
Add "import quickstep as q" at the top of your project.  Set q.ip and q.port appropriately for your quickstep server.
By default it will assume python is running on the same machine using the default port.

### Examples
In the python/examples folder there are two example uses for the API.

1. Ancestors demonstrates loading data using a python script populate.py, followed by recursive calculations on that data in calculate.py
2. DataFromWeb demonstrates loading data using a web API.

## Development

### Additional setup
You will want to install the full grpc functionality if doing development.  
sudo apt-get install python-pip  
sudo python -m install --upgrade pip  
sudo python -m pip install grpcio  
sudo python -m pip install grpcio-tools  

To rebuild the pb2.py and grpc.py files you may need to have grpc regenerate them using this command:  
python -m grpc_tools.protoc -l[protos file folder path] --python_out=[where to place .py files] --grpc_python_out=[where to place grpc.py file] [specific protos file to generate from]
