#include <Adafruit_CircuitPlayground.h>

int score = 255;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  CircuitPlayground.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  //analogWrite(5, 100);
  //get score from serial
  Serial.print(score);
  if (Serial.available()) {
    score = Serial.read();
  }
  if (score != 255)
    CircuitPlayground.playTone(440, 50);
  delay(score);
}
