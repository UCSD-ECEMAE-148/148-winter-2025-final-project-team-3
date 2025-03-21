# <div align="center">Autonomous Stock Relief</div>
![image](https://github.com/user-attachments/assets/6a336c9e-8648-4a46-ac29-695cd053a5bd)
### <div align="center"> MAE 148 Final Project </div>
#### <div align="center"> Team 3 Winter 2025 </div>
<p align = center>
  <img width="800" alt="Electronics Plate" src="Images/ECE148_Car.jpg">
</p>



## Table of Contents
  <ol>
    <li><a href="#team-members">Team Members</a></li>
    <li><a href="#abstract">Abstract</a></li>
    <li><a href="#what-we-promised">Promises and Stretch Goals</a></li>
    <li><a href="#accomplishments">Accomplishments</a></li>
    <li><a href="#challenges">Challenges</a></li>
    <li><a href="#Potential-Improvements">Potential Improvements</a></li>
    <li><a href="#Demonstrations">Demonstrations</a></li>
    <li><a href="#Robot-Design">Robot Design</a></li>
      <ul>
        <li><a href="#Mechanical-Designs">Mechanical Designs</a></li>
        <li><a href="#Electrical-System-Diagram">Electrical System Diagram</a></li>
      </ul>
  </ol>
<hr>

## Team Members
Anton John Del Mar - ECE ML & Controls - Class of 2025

Tigran Grigoryan - MAE Controls & Robotics - Class of 2027

Kanishk Mehta - MAE Aerospace - Class of 2026

Juan Sanchez - MAE Aerospace - Class of 2026
<hr>

## Abstract
The goal of our project was to create a bot that would be able to navigate between different warehouses and transport supply from overflowing warehouses to one's with less stock. To navigate between the warehouses the idea was the employ GNSS and once inside the warehouse, the bot would utilize a model running on the OAK-D Lite in order to identify boxes and pick them up with a grabbing mechanism in order to transport.
<hr>

## Promises and Stretch Goals
Promised
* Integrate GNSS, OAK-D model, and Grabber Mechanism into the ROS2 system.

Stretch Goals
* Create a "A*" algorithm in order to find the shortest distance between two warehouses and take that route.
* Integrate lidar into ROS2 system in an effort for obstacle avoidance, following a global path until reaching an obstacle and using lidar to follow a local path avoiding the obstacle and getting back onto the global path.
<hr>

## Accomplishments
- We first were able to succesfully create a custom circuit that used an Arduino Pro Micro to control a relay to turn on and off our electromagnet. Later we were able to use Python's serial library to allow our Jetson to interface with the circuit and turn on the electromagnet when needed. <br>
- We created a new custom electronics board with a new camera mount and electromagnet mount. <br>
- We succesfully utilized ROS2 and DepthAI's April Tag library in order to allow our OAK-D camera to detect april tags. We calculate how far the April Tag is and how off-center it is as well to determine how much to turn and drive. Using the /drive topic we can control speed and steering angle. With initial testing we found our robot would turn too much in proportion to the error. We created a PID class to help fine tune our robots self-alignment with April Tags. In the end we sucessfully completed the task of autonomously driving up to and algining ourself to a box marked with an April Tag, then pick it up for transportation! <br>
- We succesfully utilized the PointOneNav GNSS in ROS2 order to get global positions and navigate between warehouses. Using Python's pymap3d library we can convert global coordinates into relative coordinates. For navigation we set an origin and the coordinate of a warehouse, then simply use y = mx + b to determine the path by creating a straight line to the warehouse. We can now use cross track error and the determinant of two vectors to see how we deviate from the line and see which side we are on, then use our PID class to realign ourselves onto the path. In the end we were able to succesfully navigate to a warehouse autonomously using GNSS! <br>
<hr>

## Challenges
- Our electronics mount broke during the race, causing us to have to redesign a base and reintegrate our electronics.
- We initially made our own electromagnet, however could not integrate it with the relay circuit, causing us to have to use a store bought one.
- The first camera mount we created was too high and since it was adujustable the angle could change and require us to recallibrate our April Tag detection. We thus created a new short, fixed camera mount that also could hold our electromagnet.
- It took one week to debug and get our GPS to work. We tried two different repositories for the PointOneNav, tried different Docker containers, tried uninstalling and reinstalling the fusion-engine-driver, we tried other GPS modules, we even tried to use the Ublox, all to no avail. After one week of trieless debugging and suffering, it turns out it really was just our module. Our module simply did not work with the fusion-engine-driver in ROS2, but our TA Winston had a module that did and he let us use his.
- A lot of restless coding, debugging, and testing, trying to integrate our autonomous system fully in ROS2. 
- Issues with our Docker container caused us to lose some code and have to rewrite it.
- Jetson SD card was corrupted the day before our final presentation, and we could not save our Docker conatiner. Causing us to have to reflash our SD card, reinstall and setup everything such as pulling and setting up the Docker image, and also having to rewrite a lot of missing code.
- Created our own topic and message interface for our GPS and April Tag nodes, but then our VESC stopped working, preventing us from testing the interface.

<hr>

## Potential Improvements
- Create a new camera mount such that the camera is a bit farther back, because since the camera was in the front it could not see the April Tag if it was too close.
- Design a different electromagnet grabber, our design required the boxes to be on a little pallet. Maybe have the electromagnet pick up boxes from above like a crane.
- Integrate a better circuit design using perf boards or even a PCB rather than just connecting everything with wires and electrical tape. 
- Complete testing the custom topic and interface to fully integrate the April Tag and GPS nodes. 

<hr>

## Demonstrations

### Section 1: [Title of Demonstration]
**Description:**  
Write your description here.

<iframe width="560" height="315" src="EMBED_URL_FROM_FILE" frameborder="0" allowfullscreen></iframe>



### Section 2: [Title of Demonstration]
**Description:**  
Write your description here.

<iframe width="560" height="315" src="EMBED_URL_FROM_FILE" frameborder="0" allowfullscreen></iframe>



### Section 3: [Title of Demonstration]
**Description:**  
Write your description here.

<iframe width="560" height="315" src="EMBED_URL_FROM_FILE" frameborder="0" allowfullscreen></iframe>



## Robot Design

### Mechanical Designs
| Part | CAD Model |
|------|--------------|
| Electronics Mounting Plate | <img width="500" alt="Electronics Plate" src="Images/Electronics Plate.jpg"><br>[🔗 CAD File](CAD%20Files/New%20Chassis/Electronics%20plate%20v13.f3d) |
| Camera Mount | <img width="500" alt="Camera Mount" src="Images/Camera Mount Assembly .png"><br>[🔗 CAD File](CAD%20Files/New%20Chassis/Camera%20Mount/Camera%20Mount%20assembly%20v5.f3z) |
| GPS Mount | <img width="500" alt="GPS Mount" src="Images/GPS mount.jpg"><br>[🔗 CAD File](CAD%20Files/New%20Chassis/Gps%20mount%20v2.f3d) |
| Hinge Arm | <img width="400" alt="Hinge Arm" src="Images/Hinge Arm.jpg"><br>[🔗 CAD File](CAD%20Files/New%20Chassis/Hinge%20arm%20v8.f3d) |
| Hinge and GPS stand | <img width="400" alt="Hinge and GPS stand" src="Images/Hinge Stand .jpg"><br>[🔗 CAD File](CAD%20Files/New%20Chassis/GPS+hinge%20stand%20v8.f3d) |
| Magnetic Lock | <img width="500" alt="Magnetic Lock" src="Images/Magnetic Lock.jpg"><br>[🔗 CAD File](CAD%20Files/New%20Chassis/Magnetic%20Lock%20v7.f3d) |
| Jetson Case Top | <img width="500" alt="Jetson Case" src="Images/Jetson Case Top.jpg"><br>[🔗 CAD File](CAD%20Files/New%20Chassis/Jetson%20Top%20V1.SLDPRT) |
| Jetson Case Bottom | <img width="500" alt="Jetson Case" src="Images/Jetson Case Bottom.jpg"><br>[🔗 CAD File](CAD%20Files/New%20Chassis/Jetson%20Bottom%20V1.SLDPRT) |
| Camera and ElectroMagnet Stand | <img width="500" alt="Jetson Case" src="Images/Camera and EM Stand.jpg"><br>[🔗 CAD File](CAD%20Files/New%20Chassis/Camera%20and%20EM%20Stand.SLDPRT) |
| New Chassis Assembly | <img width="500" alt="New Chassis Assembly" src="Images/Chassis Assembly.jpg"><br>[🔗 CAD File](CAD%20Files/New%20Chassis/Assemply%20v7.f3z) |


### Electrical System Diagram
| Comprehensive Wiring Diagram |
|------|
| <img width="700" alt="Comprehensive Wiring Diagram" src="Images/Wiring Diagram.png"> |




