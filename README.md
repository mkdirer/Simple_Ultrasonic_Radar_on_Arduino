# Mapping Space Project
The main goal of our project was to scan the terrain using ultrasonic waves and detect objects that are closer than 200 cm.

## Components used
1. Arduino UNO
2. ROHS Step Motor with ULN2003 driver
3. HC-SR04 ultrasonic distance sensor (2-200cm)
4. Plastic connector

## Languages/libraries used

- ArduinoIDE (Stepper.h library)

- Python (pyserial, threading, matplotlib, numpy, Ipython, and PySimpleGUI libraries)

The control of ROHS motor rotation and ultrasonic distance measurement were implemented in ArduinoIDE. Then, the angle and distance to the nearest object were added to the code. A Python program was written to receive data streamed from Arduino and continuously plot it using Python libraries. It also has the ability to save data in a txt file (in the format of angle: distance) or capture a radar image in png format.

![image](https://user-images.githubusercontent.com/83553257/225794018-4d863445-28a2-4ad5-a5fd-7d2882b2da66.png)
<p align="center">
  <img src="https://user-images.githubusercontent.com/83553257/225794063-2158d400-1641-48a2-a257-0190948e1845.png" width="15%" height="15%">
  <img src="https://user-images.githubusercontent.com/83553257/225794080-23ec59d5-8d32-4b40-b6e6-77700191b083.png" width="80%" height="80%">
</p>
