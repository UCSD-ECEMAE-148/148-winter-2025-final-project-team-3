# <div align="center">Autonomous Stock Relief</div>
![image](https://github.com/user-attachments/assets/6a336c9e-8648-4a46-ac29-695cd053a5bd)
### <div align="center"> MAE 148 Final Project </div>
#### <div align="center"> Team 3 Winter 2025 </div>

## Table of Contents
  <ol>
    <li><a href="#team-members">Team Members</a></li>
    <li><a href="#abstract">Abstract</a></li>
    <li><a href="#what-we-promised">Promises and Stretch Goals</a></li>
    <li><a href="#accomplishments">Accomplishments</a></li>
    <li><a href="#challenges">Challenges</a></li>
    <li><a href="#mechanical-design">Mechanical Design</a></li>
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
We succesfully utilized the Point One Nav GNSS in order to get global positions and navigate between warehouses. The model we have running on the OAK-D Lite detects and identifies AprilTags via DepthAI SDK's preset April Tag library
<hr>

## Challenges
We faced many challenges that we did not expect to encounter while trying to complete our project. The first of which

<hr>


## Mechanical Designs
| Part | CAD Model |
|------|--------------|
| Electronics Mounting Plate | <img width="634" alt="Electronics Plate" src="Images/Electronics Plate.jpg"> |
| Camera Mount | <img width="634" alt="Camera Mount" src="Images/Camera Mount Assembly.png"> |
| GPS Mount | <img width="634" alt="GPS Mount" src="Images/GPS mount.jpg"> |
| Hinge Arm | <img width="634" alt="Lidar Mount" src="Images/Hinge Arm.jpg"> |
| Hinge and GPS stand | <img width="634" alt="Lidar Mount" src="Images/Hinge Stand .jpg"> |
| Magnetic Lock | <img width="634" alt="Lidar Mount" src="Images/Magnetic Lock.jpg"> |
| Jetson case | <img width="634" alt="Lidar Mount" src="Images/Magnetic Lock.jpg"> |
| New Chassis Assembly | <img width="634" alt="Jetson Case" src="Images/Chassis Assembly.jpg"> |

