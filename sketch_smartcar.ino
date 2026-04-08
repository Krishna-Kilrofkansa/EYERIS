#include <Servo.h>

// ---------------- MOTOR PINS ----------------
#define ENA 6
#define IN3 9
#define IN4 11
#define ENB 5
#define IN1 7
#define IN2 8

// ---------------- ULTRASONIC + SERVO ----------------
#define ECHO A4
#define TRIG A5
#define SERVO_PIN 10   // IMPORTANT: match your RasPi system (pin 10 in doc)

#define OBSTACLE_DISTANCE 20

Servo scanServo;

// Serial input buffer
String inputString = "";
bool stringComplete = false;

// ---------------------------------------------------
void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  scanServo.attach(SERVO_PIN);
  scanServo.write(90); // center

  inputString.reserve(10);
}

// ---------------------------------------------------
void loop() {

  // ===== SERIAL SERVO CONTROL (FROM RASPBERRY PI) =====
  if (stringComplete) {
    int angle = inputString.toInt();

    if (angle >= 0 && angle <= 180) {
      scanServo.write(angle);   // Pi controls servo
    }

    inputString = "";
    stringComplete = false;
  }

  // ===== OBSTACLE AVOIDANCE (AUTONOMOUS MOVEMENT) =====
  long frontDist = getDistance();

  if (frontDist < OBSTACLE_DISTANCE) {
    avoidObstacle();
  } else {
    moveForward(120);
  }
}

// ---------------- SERIAL EVENT ----------------
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

// ---------------- MOVEMENT FUNCTIONS ----------------
void moveForward(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);
}

void moveBackward(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void pivotLeft(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
}

void pivotRight(int speed) {
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
}

void stopCar() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

// ---------------- DISTANCE FUNCTION ----------------
long getDistance() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  long duration = pulseIn(ECHO, HIGH, 25000);
  if (duration == 0) return 999;

  return duration * 0.034 / 2;
}

// ---------------- OBSTACLE AVOIDANCE ----------------
void avoidObstacle() {
  stopCar();
  delay(200);

  moveBackward(120);
  delay(400);

  stopCar();
  delay(150);

  // NOTE: we DO NOT rotate servo here anymore
  // because Raspberry Pi is controlling it

  // Simple random decision (or fixed)
  pivotRight(150);
  delay(600);

  stopCar();
  delay(150);
}