#include <Adafruit_CircuitPlayground.h>

int score = 255;
bool pressed = false;
bool buttonstate = false;
bool last_buttonstate = false;

void setup() {
  // put your setup code here, to run once:

  // use a SoftwareSerialTX on Pin 2
  Serial.begin(9600);
  pinMode(4, INPUT_PULLUP);
  pinMode(19, INPUT_PULLUP);
  CircuitPlayground.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  //analogWrite(5, 100);
  //get score from serial
  while (Serial.available()) {
    score = Serial.read();
  }
  if (score != 255){
    CircuitPlayground.playTone(700, 50);
    delay(score);
  }
  if (digitalRead(19) == HIGH){
      CircuitPlayground.setPixelColor(0, CircuitPlayground.colorWheel(25 * 0));
      delay(50);
      CircuitPlayground.setPixelColor(1, CircuitPlayground.colorWheel(25 * 1));
      delay(50);
      CircuitPlayground.setPixelColor(2, CircuitPlayground.colorWheel(25 * 2));
      delay(50);
      CircuitPlayground.setPixelColor(3, CircuitPlayground.colorWheel(25 * 3));
      delay(50);
      CircuitPlayground.setPixelColor(4, CircuitPlayground.colorWheel(25 * 4));
      delay(50);
      CircuitPlayground.setPixelColor(5, CircuitPlayground.colorWheel(25 * 5));
      delay(50);
      CircuitPlayground.setPixelColor(6, CircuitPlayground.colorWheel(25 * 6));
      delay(50);
      CircuitPlayground.setPixelColor(7, CircuitPlayground.colorWheel(25 * 7));
      delay(50);
      CircuitPlayground.setPixelColor(8, CircuitPlayground.colorWheel(25 * 8));
      delay(50);
      CircuitPlayground.setPixelColor(9, CircuitPlayground.colorWheel(25 * 9));
      delay(50);
    if (!pressed)
      Serial.write(true);
    pressed = true;
  } else {
    pressed = false;
    CircuitPlayground.clearPixels();
  }
}
