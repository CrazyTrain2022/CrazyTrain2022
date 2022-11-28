import numpy as np

print("Adding fig8")

#COMMENT: NEEDS COMMENTING

waypoints = np.genfromtxt("waypoints.csv", delimiter=',')
last_pos = waypoints[-1,:]

n = 8
for t in range(n+1):
    x = (1.5*np.cos(2*np.pi*(t/n)))
    y = (1.5*np.sin(2*(2*np.pi*(t/n)))/2)
    z = (last_pos[2])
    waypoints = np.append(waypoints,np.array([[x,y,z]]),axis=0)

np.savetxt('waypoints.csv', X=waypoints, delimiter=',', fmt='%10.2f')
