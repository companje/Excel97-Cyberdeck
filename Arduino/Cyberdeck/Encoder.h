#include "Arduino.h"
 
static int8_t states[] = {0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0};

class Encoder {
public:
  int pinA, pinB, prevA, prevB, index, value;
  
  //delta, prev, v;
  
  Encoder() { 
  }
 
  Encoder(int pinA, int pinB) : pinA(pinA), pinB(pinB) {
    pinMode(pinA, INPUT);
    pinMode(pinB, INPUT);
    digitalWrite(pinA, HIGH);
    digitalWrite(pinB, HIGH);
    prevA = 0;
    prevB = 0;
    value = 0;
  }
 
  void update() {
      
    int a = digitalRead(pinA);
    int b = digitalRead(pinB);
  
    int index = prevA+(a<<1)+(prevB<<2)+(b<<3);
    
    prevA = a;
    prevB = b;
    
    value+=states[index];
  }
};
