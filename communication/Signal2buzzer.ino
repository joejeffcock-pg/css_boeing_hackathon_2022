#include <Adafruit_CircuitPlayground.h>

int score = 10;

void setup() {
  // put your setup code here, to run once:
  CircuitPlayground.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  //analogWrite(5, 100);
  //get score from serial
  while (score>0) {
    CircuitPlayground.playTone(440, 1000/score);
    CircuitPlayground.playTone(0, 1000/score);
    }
}
