#include <Servo.h>

Servo servos[5];
int pins[5] = {7, 6, 5, 4, 3};
int lastState[5] = {0, 0, 0, 0, 0}; // Track previous state

void setup() {
  Serial.begin(9600);
  delay(100);

  for (int i = 0; i < 5; i++) {
    servos[i].attach(pins[i]);
  }
  
  // Start with all servos OPEN
  openAllFingers();
  
  Serial.println("READY");
}

void openAllFingers() {
  // Pin 7, 6 (anticlockwise): 0° = open
  servos[0].write(0);
  servos[1].write(0);
  
  // Pin 5 (normal): 180° = open
  servos[2].write(180);
  
  // Pin 4 (clockwise): 180° = open
  servos[3].write(180);
  
  // Pin 3 (normal): 180° = open
  servos[4].write(180);
}

void foldAllFingers() {
  // Pin 7, 6 (anticlockwise): 180° = fold
  servos[0].write(180);
  servos[1].write(180);
  
  // Pin 5 (normal): 0° = fold
  servos[2].write(0);
  
  // Pin 4 (clockwise): 0° = fold
  servos[3].write(0);
  
  // Pin 3 (normal): 0° = fold
  servos[4].write(0);
}

void controlFinger(int index, int state) {
  int targetAngle;
  
  if (index == 0 || index == 1) {
    // Pin 7, 6 (anticlockwise): 1=open(0°), 0=fold(180°)
    targetAngle = state == 1 ? 0 : 180;
  } else if (index == 3) {
    // Pin 4 (clockwise): 1=open(180°), 0=fold(0°)
    targetAngle = state == 1 ? 180 : 0;
  } else {
    // Pin 5, 3 (normal): 1=open(180°), 0=fold(0°)
    targetAngle = state == 1 ? 180 : 0;
  }
  
  // Slow smooth movement for pin 4, normal for others
  if (index == 3) {
    moveServoSmooth(index, targetAngle, 50);
  } else {
    servos[index].write(targetAngle);
  }
}

void moveServoSmooth(int servoIndex, int targetAngle, int stepDelay) {
  int currentAngle = servos[servoIndex].read();
  
  // Make sure we're moving in the right direction
  if (currentAngle < targetAngle) {
    for (int i = currentAngle; i <= targetAngle; i++) {
      servos[servoIndex].write(i);
      delay(stepDelay);
    }
  } else {
    for (int i = currentAngle; i >= targetAngle; i--) {
      servos[servoIndex].write(i);
      delay(stepDelay);
    }
  }
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    
    if (data.length() == 0) return;

    int values[5] = {0, 0, 0, 0, 0};
    int index = 0;
    int lastPos = 0;

    for (int i = 0; i <= data.length(); i++) {
      if (i == data.length() || data[i] == ',') {
        String token = data.substring(lastPos, i);
        if (index < 5) {
          values[index] = token.toInt();
        }
        lastPos = i + 1;
        index++;
      }
    }

    // Count open and closed fingers
    int openCount = 0;
    for (int i = 0; i < 5; i++) {
      if (values[i] == 1) openCount++;
    }

    // All folded (0 open fingers)
    if (openCount == 0) {
      Serial.println("FOLD_ALL");
      foldAllFingers();
    }
    // All open (5 open fingers)
    else if (openCount == 5) {
      Serial.println("OPEN_ALL");
      openAllFingers();
    }
    // Individual fingers control
    else {
      // Only update fingers that changed
      for (int i = 0; i < 5; i++) {
        if (values[i] != lastState[i]) {
          controlFinger(i, values[i]);
          delay(50); // Small delay between servo updates
        }
      }
    }

    // Update last state
    for (int i = 0; i < 5; i++) {
      lastState[i] = values[i];
    }
    
    Serial.print("OK:");
    for (int i = 0; i < 5; i++) {
      Serial.print(values[i]);
      if (i < 4) Serial.print(",");
    }
    Serial.println();
  }
}