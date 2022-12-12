// Includes the stepper library
#include <Stepper.h>

#define STEP_COUNT 32

Stepper stepper(STEP_COUNT, 8, 10, 9, 11);

// Defines Tirg and Echo pins of the Ultrasonic Sensor
const int trigPin = 3;
const int echoPin = 4;

// Variables for the duration and the distance
long duration;
int distance;

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600);
  Serial.setTimeout(50);
  stepper.setSpeed(300);
}

//komnedy: zczytuj ciągle, wyłącz wyłacz/odczyt (samo obracanie), wyłacz ciągły odczyt ciągle obracanie w przedziale 15 do 165 stopni, obróc w prawo 90 stopni, obróc w lewo o -90 stopni wraz z odczytem.

void loop() {
  if(Serial.available()){
    String input = Serial.readString();
    char* arr = strtok(input.c_str(), ",");
    int mode = atoi(arr);
    arr = strtok(nullptr, ",");
    int angle = atoi(arr);

    if (mode == 1){
      stepper.step(angle);
    }
    while (mode == 2){
      float step = 5.7;
      float check_angle = 0;
      int exit = 0;
      while(check_angle <= angle){
        stepper.step(step);
        Serial.println(String(check_angle) + "," + calculateDistance());
        if(Serial.available()){
          exit = 1;
          break;
        }
        check_angle += step;
      }
      check_angle = angle;
      if(exit == 1){ break; }
      while (check_angle >= 0){
        stepper.step(-step);
        Serial.println(String(check_angle) + "," + calculateDistance());
        if(Serial.available()){
          exit = 1;
          break;
        }
        check_angle -= step;
      }
      if(exit == 1){ break; }
    }
  }
}

// Function for calculating the distance measured by the Ultrasonic sensor
int calculateDistance(){ 
  
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance= duration*0.034/2;
  return distance;
}
