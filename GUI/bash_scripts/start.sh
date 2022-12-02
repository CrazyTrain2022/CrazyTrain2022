cd crazyswarm
source ros_ws/devel/setup.bash
roscore &
cd src/crazyswarm/launch
roslaunch hover_swarm.launch &
cd ../Qualisys_node/mocap_qualisys/launch
