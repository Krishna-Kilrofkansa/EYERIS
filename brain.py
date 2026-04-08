import cv2
import mediapipe as mp
import serial
import time
from datetime import datetime

# ==================== CONFIG ====================
SERIAL_PORT     = '/dev/ttyACM0'      # As you requested
BAUD_RATE       = 9600
CENTER_ANGLE    = 90
TRACKING_GAIN   = 0.065
CAMERA_INDEX    = 0

# Video Recording
OUTPUT_VIDEO_NAME = "socio_cognitive_footage.mp4"
FPS = 20.0
# ===============================================

# Connect to Arduino with better error handling
ser = None
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2.5)
    ser.write(f"{CENTER_ANGLE}\n".encode())
    print(f"✔ Connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    print(f"✘ Could not connect to Arduino: {e}")
    print("Continuing without servo control...")
    ser = None

# MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    min_detection_confidence=0.55,
    min_tracking_confidence=0.55,
    model_complexity=1
)

cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("✘ Cannot open camera")
    exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Video Writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_VIDEO_NAME, fourcc, FPS, (640, 480))
print(f"🎥 Recording started → Saving as '{OUTPUT_VIDEO_NAME}'")

current_angle = CENTER_ANGLE
print("\n=== Socio Cognitive Footage Recorder Started ===")
print("Press 'q' to stop recording and quit\n")

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Frame capture failed.")
        break

    frame_count += 1

    # MediaPipe processing
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb.flags.writeable = False
    results = pose.process(rgb)
    rgb.flags.writeable = True
    frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

    person_detected = False
    nose_x = None

    if results.pose_landmarks:
        person_detected = True
        lm = results.pose_landmarks.landmark
        h, w, _ = frame.shape
        nose_x = int(lm[mp_pose.PoseLandmark.NOSE].x * w)

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # === Tracking Logic with safe serial write ===
    if ser and person_detected and nose_x is not None:
        try:
            center_x = w // 2
            error = center_x - nose_x
            delta = int(error * TRACKING_GAIN)
            current_angle += delta
            current_angle = max(0, min(180, current_angle))
            ser.write(f"{current_angle}\n".encode())
            status = "TRACKING"
            color = (0, 255, 0)
        except Exception as e:
            print(f"Serial write error: {e}")
            status = "TRACKING (serial error)"
            color = (0, 165, 255)
    else:
        if ser:
            try:
                if current_angle != CENTER_ANGLE:
                    current_angle = CENTER_ANGLE
                    ser.write(f"{current_angle}\n".encode())
            except:
                pass
        status = "CENTER (no person)"
        color = (0, 165, 255)

    # On-screen info
    cv2.putText(frame, f"Status: {status}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    cv2.putText(frame, "Socio Cognitive Footage Recording", (10, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(frame, f"Frame: {frame_count}", (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Write to video file
    out.write(frame)

    cv2.imshow("Socio Cognitive Footage", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Recording stopped by user.")
        break

# Cleanup
cap.release()
out.release()
cv2.destroyAllWindows()

if ser:
    try:
        ser.write(f"{CENTER_ANGLE}\n".encode())
        ser.close()
    except:
        pass

print(f"Recording successfully saved as '{OUTPUT_VIDEO_NAME}'")
print(f"Total frames recorded: {frame_count}")
print("Stopped cleanly.")