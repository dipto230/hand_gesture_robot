#include <Servo.h>

Servo servos[5];
int pins[5] = {7, 6, 5, 4, 3};

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
  servos[0].write(0);    // Pin 7: open
  servos[1].write(0);    // Pin 6: open
  servos[2].write(180);  // Pin 5: open
  servos[3].write(180);  // Pin 4: open
  servos[4].write(180);  // Pin 3: open
}

void foldAllFingers() {
  servos[0].write(180);  // Pin 7: fold
  servos[1].write(180);  // Pin 6: fold
  servos[2].write(0);    // Pin 5: fold
  servos[3].write(0);    // Pin 4: fold
  servos[4].write(0);    // Pin 3: fold
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    
    if (data.length() == 0) return;

    int values[5] = {0, 0, 0, 0, 0};
    int index = 0;
    int lastPos = 0;

    // Parse CSV data
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

    // Count open fingers
    int openCount = 0;
    for (int i = 0; i < 5; i++) {
      if (values[i] == 1) openCount++;
    }

    // All folded (0 open fingers)
    if (openCount == 0) {
      foldAllFingers();
    }
    // All open (5 open fingers)
    else if (openCount == 5) {
      openAllFingers();
    }
    // Individual finger control
    else {
      for (int i = 0; i < 5; i++) {
        if (i == 0 || i == 1) {
          // Pin 7, 6 (anticlockwise): 1=open(0°), 0=fold(180°)
          servos[i].write(values[i] == 1 ? 0 : 180);
        } else if (i == 3) {
          // Pin 4 (clockwise): 1=open(180°), 0=fold(0°)
          servos[i].write(values[i] == 1 ? 180 : 0);
        } else {
          // Pin 5, 3 (normal): 1=open(180°), 0=fold(0°)
          servos[i].write(values[i] == 1 ? 180 : 0);
        }
      }
    }
    
    Serial.print("OK:");
    for (int i = 0; i < 5; i++) {
      Serial.print(values[i]);
      if (i < 4) Serial.print(",");
    }
    Serial.println();
  }
}