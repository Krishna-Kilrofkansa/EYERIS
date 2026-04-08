----------------------------------------------------------------
Instructions
----------------------------------------------------------------
----------------------------------------------------------------
1. ASSEMBLY — STEP BY STEP
----------------------------------------------------------------

Step 1: Build the Chassis
  - Attach both DC motors to the chassis frame.
  - Fix the wheels onto the motors.
  - Mount the battery pack securely at the base.

Step 2: Attach the Motor Driver
  - Connect the DC motors to the L298N motor driver outputs.
  - Wire the driver's control pins to the Arduino
    as shown in Section 2.

Step 3: Mount the Ultrasonic Sensor
  - Place the HC-SR04 at the front of the robot, facing forward.
  - This sensor detects obstacles in the robot's path.
  - Connect: TRIG --> A5 and ECHO --> A4 on the Arduino.

Step 4: Mount the Servo and Camera
  - Fix the SG90 servo on the top or front of the chassis.
  - Attach the camera on top of the servo so it rotates with it.
  - Connect the servo signal wire to Arduino Pin 10.

Step 5: Place the Raspberry Pi
  - Mount the Raspberry Pi securely on the chassis.
  - Connect the camera to the Pi.
  - Connect a USB cable from the Pi to the Arduino
    for serial communication.

----------------------------------------------------------------
2. HOW TO RUN THE SYSTEM
----------------------------------------------------------------

Step 1 — Upload Code to Arduino
  1. Open the Arduino IDE.
  2. Paste in the .ino code.
  3. Select Board: Arduino UNO.
  4. Select the correct port:
       - Windows : COM*
       - Linux   : ttyACM*
  5. Click Upload.

Step 2 — Run the Raspberry Pi Script
  Open a terminal on the Raspberry Pi and run:

      python3 brain.py

Step 3 — What Happens Next
  - The Pi activates the camera and starts detecting humans.
  - It calculates the person's position and sends angles
    to the Arduino over the USB serial connection.
  - The Arduino receives the angle, moves the servo,
    and begins navigating autonomously.


----------------------------------------------------------------
3. SYSTEM WORKFLOW (FULL PIPELINE)
----------------------------------------------------------------

  [1] Camera captures live video
          |
          v
  [2] Raspberry Pi runs MediaPipe AI
      --> Detects a human in the frame
          |
          v
  [3] Head/nose position is calculated
      --> Determines the horizontal tracking angle
          |
          v
  [4] Angle is sent to Arduino via serial
      --> Command: ser.write(f"{angle}\n".encode())
          |
          v
  [5] Arduino receives the angle
      --> Rotates servo to keep human in frame
          |
          v
  [6] Arduino reads ultrasonic sensor
      --> Checks for obstacles
          |
          v
  [7] Robot moves safely and autonomously


----------------------------------------------------------------
4. FINAL OUTPUT — FEATURES ACHIEVED
----------------------------------------------------------------

  Human Detection
    Uses MediaPipe AI to identify people in real time
    through the camera feed.

  Real-Time Tracking
    The servo motor rotates the camera to follow the
    detected person's head position continuously.

  Autonomous Navigation
    The robot moves on its own while avoiding obstacles
    detected by the ultrasonic sensor.

  Privacy Enforcement
    The robot maintains a controlled distance and only
    tracks within defined boundaries.


================================================================
                         END OF GUIDE
================================================================