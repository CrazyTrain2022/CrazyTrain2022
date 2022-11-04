cd crazyswarm
source ros_ws/devel/setup.bash
rosservice call /cf1/land '{groupMask: 0, height: .05, duration: { secs: 3, nsecs: 5}'}
rosservice call /cf2/land '{groupMask: 0, height: .05, duration: { secs: 3, nsecs: 5}'}
