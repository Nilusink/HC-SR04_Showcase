#include <Arduino.h>

#define VCC 4
#define trig 5
#define echo 6
#define GND 7

long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement


void setup() {
  Serial.begin(9600);
  pinMode(VCC, OUTPUT); digitalWrite(VCC, 1);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  pinMode(GND, INPUT);
}


void loop() {
  // Clears the trigPin condition
  digitalWrite(trig, LOW);
  delayMicroseconds(2);

  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echo, HIGH);

  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

  // Displays the distance on the Serial Monitor
  Serial.print(duration); Serial.print("\t"); Serial.println(distance);
  delay(20);
}
