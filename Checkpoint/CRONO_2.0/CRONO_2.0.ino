#define RESTART asm("jmp 0x0000")
#include "SevSeg.h"

SevSeg sevseg;
const byte interruptPin = 2;
volatile int cont=0;
volatile int delai=0;
static int tiempo1;
static int deciSeconds = 0;

void setup()
{
  Serial.begin(9600);
  byte numDigits = 4;   
  byte digitPins[] = {6, 5, 4, 3};
  byte segmentPins[] = {7, 8, 9, 10, 11, 12, 13};

  sevseg.begin(N_TRANSISTORS, numDigits, digitPins, segmentPins);
  sevseg.setBrightness(30);

  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), pulso, LOW);
}

void loop()
{ 
  if(cont==0)
  {
    if(deciSeconds==0)
    {
      sevseg.setNumber(deciSeconds,4);
      sevseg.refreshDisplay(); // Must run repeatedly
    }
    else
      fin();   
  }
  else
  { 
    static unsigned long timer = millis();
    if (millis() >= timer)
    {
      deciSeconds++; // 100 milliSeconds is equal to 1 deciSecond
      timer += 100;
      if(deciSeconds-delai==30)
        attachInterrupt(digitalPinToInterrupt(interruptPin), pulso, LOW);
      Serial.println(deciSeconds);
      if (deciSeconds%1000 == 600)
        deciSeconds+=400;
      sevseg.setNumber(deciSeconds,4);
    }
    sevseg.refreshDisplay(); // Must run repeatedly
   
  }
}

void pulso()
{
  detachInterrupt(digitalPinToInterrupt(interruptPin));  
  cont++ ;
  delai=deciSeconds;
  if(cont==2)
  {
    tiempo1=deciSeconds;
    deciSeconds=0;
    delai=0;
  }
  else if(cont==3)
    cont=0;
}
 
 void fin()
 {
  int i=0;
      while(true)
      {
        if(i<400)
        {
          sevseg.setNumber(deciSeconds,4);
          sevseg.refreshDisplay(); // Must run repeatedly
        }
        else
        {
          sevseg.setNumber(tiempo1,4);
          sevseg.refreshDisplay(); // Must run repeatedly
        }
        i++;
        if(i==800)
          RESTART;
          
      }
} 

