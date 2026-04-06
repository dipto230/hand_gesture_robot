#include <Servo.h>

Servo servos[5];
int pins[5] = {7, 6, 5, 4, 3};

void setup() {
  Serial.begin(9600);
  delay(100);

  for (int i = 0; i < 5; i++) {
    servos[i].attach(pins[i]);
  }
  

  openAllFingers();
  
  Serial.println("READY");
}

void openAllFingers() {
  servos[0].write(0);    
  servos[1].write(0);    
  servos[2].write(180);  
  servos[3].write(180);  
  servos[4].write(180);  
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
      if (i == 0 || i == 1) {
   
        servos[i].write(values[i] == 1 ? 0 : 180);
      } else if (i == 3) {
     
        servos[i].write(values[i] == 1 ? 180 : 0);
      } else {
    
        servos[i].write(values[i] == 1 ? 180 : 0);
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