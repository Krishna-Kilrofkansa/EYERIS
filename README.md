# EYERIS
Human Avoidance Privacy Robot
================================================================
     EYE-RIS ROBOT — COMPLETE GUIDE
================================================================


----------------------------------------------------------------
1. REQUIREMENTS
----------------------------------------------------------------

HARDWARE COMPONENTS
-------------------
- Arduino UNO
- Raspberry Pi (3 or 4)
- L298N Motor Driver
- Smart Car Chassis
- 2 x DC Motors + Wheels
- SG90 Servo Motor
- HC-SR04 Ultrasonic Sensor
- USB Camera or Pi Camera
- Jumper Wires
- Battery Pack (7.4V to 12V recommended)


SOFTWARE — Raspberry Pi
-----------------------
- Python
- OpenCV
- MediaPipe
- PySerial


SOFTWARE — Arduino
------------------
- Arduino IDE
- Servo Library (comes pre-installed with the IDE)


----------------------------------------------------------------
2. WIRING AND CONNECTIONS
----------------------------------------------------------------

NOTE: Double-check every pin before powering on.


Motor Driver (L298N) --> Arduino
--------------------------------
  L298N Pin       Arduino Pin
  ---------       -----------
  ENA             6
  IN1             7
  IN2             8
  ENB             5
  IN3             9
  IN4             11


Ultrasonic Sensor (HC-SR04) --> Arduino
----------------------------------------
  Sensor Pin      Arduino Pin
  ----------      -----------
  TRIG            A5
  ECHO            A4


Servo Motor (SG90) --> Arduino
-------------------------------
  Servo Wire      Arduino
  ----------      -------
  Signal          Pin 10
  VCC             5V
  GND             GND


Raspberry Pi <--> Arduino Communication
----------------------------------------
  Method          : USB Cable (Serial)
  Port            : /dev/ttyACM0
  Baud Rate       : 9600


## working video : 
Link 1: https://youtu.be/ZN1fjCswqGU

Link 2: https://youtu.be/Ve5OYI2lFI0
