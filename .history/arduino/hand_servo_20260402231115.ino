#include <Servo.h>

Servo servos[5];
int pins[5] = {7, , 6, 9, 10};

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 5; i++) {
    servos[i].attach(pins[i]);
  }
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');

    int values[5];
    int index = 0;

    for (int i = 0; i < data.length(); i++) {
      if (data[i] == ',') {
        values[index++] = data.substring(0, i).toInt();
        data = data.substring(i + 1);
        i = 0;
      }
    }
    values[index] = data.toInt();

    for (int i = 0; i < 5; i++) {
      if (values[i] == 1) {
        servos[i].write(180);
      } else {
        servos[i].write(0);
      }
    }
  }
}