#include <Servo.h>

Servo servos[5];
int pins[5] = {7, 6, 5, 4, 3};

void setup() {
  Serial.begin(9600);
  delay(100);

  for (int i = 0; i < 5; i++) {
    servos[i].attach(pins[i]);
    servos[i].write(0);
  }
  
  Serial.println("READY");
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

    for (int i = 0; i < 5; i++) {
      if (values[i] == 1) {
        servos[i].write(180);
      } else {
        servos[i].write(0);
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