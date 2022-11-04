mkdir nlopt/build
cd nlopt/build
cmake ..
make
sudo make install
cd ../..

sudo apt install -y libnlopt-dev libgoogle-glog-dev

mkdir uav_trajectories/build
cd uav_trajectories/build
cmake ..
make 
cd ../..
