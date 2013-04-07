//
//
// gloCube.ino - Firmware for Glow Cube 
// March 2013 - James Sutton
// www.jsutton.co.uk/wordpress/?p=190
//

#include <SerialCommand.h>

//Variables

SerialCommand sCmd;

// LED Pin assignments
// LED 1
int led1red =  24;
int led1green =  25;
int led1blue =  26;
// LED 2
int led2red =  1;
int led2green =  0;
int led2blue =  27;
// LED 3
int led3red =  16;
int led3green =  15;
int led3blue =  14;

// Other variables
int rValues[3] = {0,0,0};
int gValues[3] = {0,0,0};
int bValues[3] = {0,0,0};

int flashDelay = 500;

void setup()   {                
  pinMode(led1red, OUTPUT);
  pinMode(led1green, OUTPUT);
  pinMode(led1blue, OUTPUT);
  pinMode(led2red, OUTPUT);
  pinMode(led2green, OUTPUT);
  pinMode(led2blue, OUTPUT);
  pinMode(led3red, OUTPUT);
  pinMode(led3green, OUTPUT);
  pinMode(led3blue, OUTPUT);
  Serial.begin(9600); // USB is always 12 Mbit/sec

  // Set up SerialCommand Stuff
  sCmd.addCommand("F", LED_fade);
  sCmd.addCommand("L", LED_flash);
  sCmd.setDefaultHandler(unrecognized);
  Serial.println("Ready");
}

void loop()                     
{
  sCmd.readSerial();     // We don't do much, just process serial commands
}

// Processes the Fade command
void LED_fade() {
 Serial.println("Fading LED..");
 char *arg;
 int ledID;
 int ledR;
 int ledG;
 int ledB;
 
 arg = sCmd.next();
 if (arg != NULL) {
  ledID = atoi(arg); 
 } else {
  Serial.println("Missing Arguments"); 
 }
 
 arg = sCmd.next();
 if (arg != NULL) {
  ledR = atoi(arg); 
 } else {
  Serial.println("Missing Arguments"); 
 }
 
 arg = sCmd.next();
 if (arg != NULL) {
  ledG = atoi(arg); 
 } else {
  Serial.println("Missing Arguments"); 
 }
 
 arg = sCmd.next();
 if (arg != NULL) {
  ledB = atoi(arg); 
 } else {
  Serial.println("Missing Arguments"); 
 }
 
 ledFadeTo(ledID,ledR,ledG,ledB);
 
 
}


// Flashes All LEDs the same colour five times before returning to original colours
void LED_flash() {
 Serial.println("Flashing LEDs...");
 int flashNo;
 int ledR;
 int ledG;
 int ledB;
  char *arg;
 
  arg = sCmd.next();
 if (arg != NULL) {
  flashNo = atoi(arg); 
 } else {
  Serial.println("Missing Arguments"); 
 }
 
 arg = sCmd.next();
 if (arg != NULL) {
  ledR = atoi(arg); 
 } else {
  Serial.println("Missing Arguments"); 
 }
 
 arg = sCmd.next();
 if (arg != NULL) {
  ledG = atoi(arg); 
 } else {
  Serial.println("Missing Arguments"); 
 }
 
 arg = sCmd.next();
 if (arg != NULL) {
  ledB = atoi(arg); 
 } else {
  Serial.println("Missing Arguments"); 
 }
 
 for(int i = 0; i < flashNo; i++){
   //
   setLED(0, ledR, ledG, ledB);
   setLED(1, ledR, ledG, ledB);
   setLED(2, ledR, ledG, ledB);
   delay(flashDelay);
 setLED(0, rValues[0], gValues[0], bValues[0]);
 setLED(1, rValues[1], gValues[1], bValues[1]);
 setLED(2, rValues[2], gValues[2], bValues[2]);
   delay(flashDelay);
 }
 setLED(0, rValues[0], gValues[0], bValues[0]);
 setLED(1, rValues[1], gValues[1], bValues[1]);
 setLED(2, rValues[2], gValues[2], bValues[2]);


}

// This gets set as the default handler, and gets called when no other command matches.
void unrecognized(const char *command) {
  Serial.println("What?");
}


// Fades an LED to a specific RGB value
void ledFadeTo(int led, int r, int g, int b){
 Serial.print("Fading led: ");
 Serial.print(led);
 Serial.print(" to r:");
 Serial.print(r);
 Serial.print(" g:");
 Serial.print(g);
 Serial.print(" b:");
 Serial.println(b);
 
 int fadeComplete = 0;
 
 // Set Fade amounts
 int fadeR = 1;
 int fadeG = 1;
 int fadeB = 1;
 
 if(rValues[led] > r){
   fadeR = -fadeR;
 }
 
 if(gValues[led] > g){
   fadeG = -fadeG;
 }
 
 if(bValues[led] > b){
   fadeB = -fadeB;
 }
 
 while(fadeComplete == 0){
      if(rValues[led] == r){
     fadeR = 0;
   }
   
   if(gValues[led] == g){
     fadeG = 0;
   }
   
   if(bValues[led] == b){
     fadeB = 0;
   }
   rValues[led] = rValues[led] + fadeR;
   gValues[led] = gValues[led] + fadeG;
   bValues[led] = bValues[led] + fadeB;
   setLED(led, rValues[led], gValues[led], bValues[led]);

   if(rValues[led] == r && gValues[led] == g && bValues[led] == b){
     fadeComplete = 1;
   }
   delay(20);
 }
 
 
 }

// Set LED  Intensities  
void setLED(int led, int r, int g, int b){
  if(led == 0){
    analogWrite(led1red, r);
    analogWrite(led1green, g);
    analogWrite(led1blue, b);
  }
  
  if(led == 1){
    analogWrite(led2red, r);
    analogWrite(led2green, g);
    analogWrite(led2blue, b);
  }
  
  if(led == 2){
    analogWrite(led3red, r);
    analogWrite(led3green, g);
    analogWrite(led3blue, b);
  }
  
} 

