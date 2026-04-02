#include <Servo.h>

Servo thumb, indexF, middle, ring, pinky;

int thumbPin = 2;
int indexPin = 4;
int middlePin = 7;
int ringPin = 8;
int pinkyPin = 11;

void setup() {
  Serial.begin(9600);

  thumb.attach(thumbPin);
  indexF.attach(indexPin);
  middle.attach(middlePin);
  ring.attach(ringPin);
  pinky.attach(pinkyPin);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');

    int f1, f2, f3, f4, f5;
    sscanf(data.c_str(), "%d,%d,%d,%d,%d", &f1, &f2, &f3, &f4, &f5);

    moveServo(thumb, f1);
    moveServo(indexF, f2);
    moveServo(middle, f3);
    moveServo(ring, f4);
    moveServo(pinky, f5);
  }
}

void moveServo(Servo servo, int state) {
  servo.write(state ? 0 : 90);
}