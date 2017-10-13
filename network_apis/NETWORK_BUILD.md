# Building Quickstep for Network Traffic

### Install Dependencies (mostly for GRPC and Protobuf)
sudo apt-get install build-essential autoconf libtool  
sudo apt-get install libgflags-dev libgtest-dev  
sudo apt-get install clang libc++-dev  
sudo apt-get install pkg-config  
sudo apt install git  
sudo apt install cmake  


### Install GRPC (https://github.com/grpc/grpc/blob/master/INSTALL.md)
git clone -b $(curl -L https://grpc.io/release) https://github.com/grpc/grpc  
cd grpc  
git submodule update --init  
make  
sudo make install  


### Install Protobuf for GRPC (https://grpc.io/docs/quickstart/cpp.html)
cd grpc/third_party/protobuf  
./autogen.sh  
./configure  
make  
sudo make install  


### Build Quickstep (https://github.com/apache/incubator-quickstep)
git clone https://git-wip-us.apache.org/repos/asf/incubator-quickstep.git quickstep  
cd quickstep  
git submodule init  
git submodule update  
cd third_party  
./download_and_patch_prerequisites.sh  
cd ../build  


### Prevent warnings from stopping build
Go into the text file quickstep/CMakeLists.txt and comment out the block for COMPILER_HAS_WERROR warnings.  The -Werror flag it sets makes all warnings errors, and some compilers will stop on errors like "this variable may not have been initialized", which a consumer of the project can't fix anyways.


### Build Quickstep Continued (only step that should take more than 10 minutes to run)
cmake -D CMAKE_BUILD_TYPE=Release -D ENABLE_NETWORK_CLI=true  
make -j3


### Running Quickstep
To run quickstep locally, run the following in the quickstep/build folder:  
./quickstep_cli_shell -mode=local  

To run it in network server mode instead (so that clients can connect using GRPC) start it with the mode flag set to network:  
./quickstep_cli_shell -mode=network  


### Running the Quickstep Example Network Client
In a separate terminal from the quickstep shell running in network mode (see above) run the following from the quickstep/build folder:  
./quickstep_client  

Here you can write out SQL queries the same way you would in the local CLI.  Note that you can add multiple lines and then execute them using the EOF character (sent using Ctrl+D in the Ubuntu terminal).

