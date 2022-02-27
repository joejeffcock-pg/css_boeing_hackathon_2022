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
    CircuitPlayground.playTone(440, 50);
    delay(score);
  }
  if (digitalRead(19) == HIGH){
    CircuitPlayground.setPixelColor(9, 255, 0, 0);
    if (!pressed)
      Serial.write(true);
    pressed = true;
  } else {
    pressed = false;
    CircuitPlayground.clearPixels();
  }
}
