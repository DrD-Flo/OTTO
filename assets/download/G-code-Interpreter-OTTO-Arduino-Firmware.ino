/**
 * Author David Florian
 * Simplified G-code interpreter 
 * 
 * If you decide not to implement optional features you must
 * comment out the correspondin

 * g blocks of code
 */

#include <TMCStepper.h>

//**** ARDUINO PINS *****

//***** X-Axis *****
#define X_EN_PIN           22 // Enable
#define X_STEP_PIN         23 // Step
#define X_DIR_PIN          24 // Direction
#define X_CS_PIN           25 // Chip select
#define X_LIMIT            41 // Limit Switch

//***** Y-Axis *****
#define Y_EN_PIN           26 // Enable
#define Y_STEP_PIN         27 // Step
#define Y_DIR_PIN          29 // Direction
#define Y1_CS_PIN          28 // Chip select
#define Y2_CS_PIN          30 // Chip select
#define Y_LIMIT            42 // Limit Switch

//***** Z-Axis *****
#define Z_EN_PIN           31 // Enable
#define Z_STEP_PIN         32 // Step
#define Z_DIR_PIN          33 // Direction
#define Z_CS_PIN           34 // Chip select
#define Z_LIMIT            45 // Limit Switch

//***** P-Axis *****
#define P_EN_PIN           35 // Enable
#define P_STEP_PIN         36 // Step
#define P_DIR_PIN          37 // Direction
#define P_CS_PIN           38 // Chip select

//***** Floating Head *****
#define FLOATING_HEAD      47 // Floating Head Switch

//***** Tip Sensors *****
#define X_LASER            44 // Yellow 
#define Y_LASER            40 // Black

//***** Optional LEDs ******
#define LED_SKIRT          5
#define LED_Pipette        4

//***** Optional Buttons *****
#define PLAY_PAUSE_BUTTON  50
#define PLAY_PAUSE_LED     2 // The LEDs in the button can be turned on and off
#define ALERT_BUTTON       46
#define ALERT_BUTTON_LED   3 // The LEDs in the button can be turned on and off

         

//**** STEPPER DRIVERS *****

//***** Configuring TMC2660 Stepper drivers *****
#define R_SENSE 0.1f // Match to your driver
                     // SilentStepStick series use 0.11
                     // UltiMachine Einsy and Archim2 boards use 0.2
                     // Panucatt BSD2660 uses 0.1
                     // Watterott TMC5160 uses 0.075

TMC2660Stepper driverX = TMC2660Stepper(X_CS_PIN, R_SENSE); 
TMC2660Stepper driverY1 = TMC2660Stepper(Y1_CS_PIN, R_SENSE);
TMC2660Stepper driverY2 = TMC2660Stepper(Y2_CS_PIN, R_SENSE); 
TMC2660Stepper driverZ = TMC2660Stepper(Z_CS_PIN, R_SENSE); 
TMC2660Stepper driverP = TMC2660Stepper(P_CS_PIN, R_SENSE); 

//***** Configuring Step/Dir Pins with AccelStepper *****

#include <AccelStepper.h>
#include <MultiStepper.h>

AccelStepper stepperX(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);
AccelStepper stepperY(AccelStepper::DRIVER, Y_STEP_PIN, Y_DIR_PIN);
AccelStepper stepperZ(AccelStepper::DRIVER, Z_STEP_PIN, Z_DIR_PIN);
AccelStepper stepperP(AccelStepper::DRIVER, P_STEP_PIN, P_DIR_PIN);

//***** OPTIONAL LEDs CONFIGURATION *****
#include <Adafruit_NeoPixel.h> //These are WS2812 LEDs AKA Neopixels
int skirt_leds_num = 14; //Number of LEDs per strip
int pipette_leds_num = 8;

Adafruit_NeoPixel skirt_leds = Adafruit_NeoPixel(skirt_leds_num, LED_SKIRT, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pipette_leds = Adafruit_NeoPixel(pipette_leds_num, LED_Pipette, NEO_GRB + NEO_KHZ800);


int changeDirection = 1;


// ***** Variables for Serial Communication with Computer *****

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

// variables to hold the parsed data
char mode[6];
int integerFromPC = 0;
float floatFromPC = 0.0;
boolean newData = false;


//***** Limit Switches *****
//variables to hold the limit switch states
boolean homeX;
boolean homeY;
boolean homeZ;
boolean homeP;

//***** STEP PER MM *****
//Its important that these values are correct
//so that the digital coordinate system = matches real world 
//Total step per revolution = full steps/rev * microsteps
//200 full steps * 16 microsteps = 3200 digital steps
int x_steps_mm = 80;
int y_steps_mm = 400;
int z_steps_mm = 400;
int p_steps_mm = 157.5; 


// variables to hold location data
double locX_in_mm;
double locY_in_mm;
double locZ_in_mm;
double locP_in_mm;

int locX_in_steps;
int locY_in_steps;
int locZ_in_steps;
int locP_in_steps;

// variables to hold LED data

int ledR;
int ledG;
int ledB;

void setup() {
    SPI.begin();
    Serial.begin(9600);
    while(!Serial);

    
    // Outputs for Chip Select (or SS) SPI Communication
    pinMode(X_CS_PIN, OUTPUT);
    pinMode(Y1_CS_PIN, OUTPUT);
    pinMode(Y2_CS_PIN, OUTPUT);
    pinMode(Z_CS_PIN, OUTPUT);
    pinMode(P_CS_PIN, OUTPUT);
    
    digitalWrite(X_CS_PIN, HIGH);
    digitalWrite(Y1_CS_PIN, HIGH);
    digitalWrite(Y2_CS_PIN, HIGH);
    digitalWrite(Z_CS_PIN, HIGH);
    digitalWrite(P_CS_PIN, HIGH);

    //***** Setting up Drivers *****
    
    // X-axis Driver
    driverX.begin();             // Initiate pins and registeries
    driverX.rms_current(1000);    // Set stepper current to 600mA. 
    driverX.microsteps(16);
    delay(100);

    // Y-axis Driver 1
    driverY1.begin();             // Initiate pins and registeries
    driverY1.rms_current(1000);    // Set stepper current to 600mA. 
    driverY1.microsteps(16);
    delay(100);

    // Y-axis Driver 2
    driverY2.begin();             // Initiate pins and registeries
    driverY2.rms_current(1000);    // Set stepper current to 600mA. 
    driverY2.microsteps(16);
    delay(100);

    // Z-axis Driver 
    driverZ.begin();             // Initiate pins and registeries
    driverZ.rms_current(400);    // Set stepper current to 600mA. 
    driverZ.microsteps(16);
    delay(100);

    // P-axis Driver 
    driverP.begin();             // Initiate pins and registeries
    driverP.rms_current(400);    // Set stepper current to 600mA. 
    driverP.microsteps(4);
    delay(100);

    //***** Setting up Switches, Sensors, and Buttons *****
    pinMode(X_LIMIT, INPUT); 
    pinMode(Y_LIMIT, INPUT); 
    pinMode(Z_LIMIT, INPUT); 
    pinMode(FLOATING_HEAD, INPUT); 
    pinMode(X_LASER, INPUT); 
    pinMode(Y_LASER, INPUT); 
    pinMode(PLAY_PAUSE_BUTTON, INPUT);
    pinMode(PLAY_PAUSE_LED, OUTPUT);
    digitalWrite(PLAY_PAUSE_LED, LOW);
    pinMode(ALERT_BUTTON, INPUT);
    pinMode(ALERT_BUTTON_LED, OUTPUT);
    digitalWrite(ALERT_BUTTON_LED, LOW);
    
    stepperX.setMaxSpeed(15000); // 100mm/s @ 160 steps/mm
    stepperX.setAcceleration(10000); // 2000mm/s^2
    stepperX.setEnablePin(X_EN_PIN);
    stepperX.setPinsInverted(false, false, true); // (directionInvert, stepInvert, enableInvert)
    stepperX.enableOutputs();

    stepperY.setMaxSpeed(12000); // 100mm/s @ 80 steps/mm
    stepperY.setAcceleration(8000); // 2000mm/s^2
    stepperY.setEnablePin(Y_EN_PIN);
    stepperY.setPinsInverted(false, false, true); // (directionInvert, stepInvert, enableInvert)
    stepperY.enableOutputs();

    stepperZ.setMaxSpeed(12000); // 100mm/s @ 80 steps/mm
    stepperZ.setAcceleration(7000); // 2000mm/s^2
    stepperZ.setEnablePin(Z_EN_PIN);
    stepperZ.setPinsInverted(false, false, true); // (directionInvert, stepInvert, enableInvert)
    stepperZ.enableOutputs();

    stepperP.setMaxSpeed(5000); // 100mm/s @ 80 steps/mm
    stepperP.setAcceleration(1000); // 2000mm/s^2
    stepperP.setEnablePin(P_EN_PIN);
    stepperP.setPinsInverted(true, false, true); // (directionInvert, stepInvert, enableInvert)
    stepperP.enableOutputs();

    //***** Turn on LEDs *****
    skirt_leds.begin();
    for(int i=0;i<skirt_leds_num;i++){
    // skirt_leds.Color takes RGB values, from 0,0,0 up to 255,255,255
    skirt_leds.setPixelColor(i, skirt_leds.Color(50,50,50)); // red

    skirt_leds.show(); // This sends the updated pixel color to the hardware.
    }
    pipette_leds.begin();
    for(int i=0;i<pipette_leds_num;i++){
    // skirt_leds.Color takes RGB values, from 0,0,0 up to 255,255,255
    pipette_leds.setPixelColor(i, pipette_leds.Color(100,100,100)); // red

    pipette_leds.show(); // This sends the updated pixel color to the hardware.
    }
}

void loop() {
  recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        coordinateMove();
        newData = false;
    }
}

//============

void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
      rc = Serial.read();

      if (recvInProgress == true) {
          if (rc != endMarker) {
              receivedChars[ndx] = rc;
              ndx++;
              if (ndx >= numChars) {
                  ndx = numChars - 1;
              }
          }
          else {
              receivedChars[ndx] = '\0'; // terminate the string
              recvInProgress = false;
              ndx = 0;
              newData = true;
          }
      }

      else if (rc == startMarker) {
          recvInProgress = true;
      }
  }
}

//============

void parseData() {      // split the data into its parts

    //***** Poll the current location of the stepper motors *****
    locX_in_mm = stepperX.currentPosition() / x_steps_mm;
    locY_in_mm = stepperY.currentPosition() / y_steps_mm;
    locZ_in_mm = stepperZ.currentPosition() / z_steps_mm;
    locP_in_mm = stepperP.currentPosition() / p_steps_mm;
    
    char * strtokIndx; // this is used by strtok() as an index
    strtokIndx = strtok(tempChars," ");
    strcpy(mode, strtokIndx);
    strtokIndx = strtok(NULL," ");
    while (strtokIndx != NULL){
      if (strtokIndx[0] == 'X'){
      memmove(strtokIndx, strtokIndx+1, strlen(strtokIndx));
        locX_in_mm = atof(strtokIndx); 
      }
      if (strtokIndx[0] == 'Y'){
      memmove(strtokIndx, strtokIndx+1, strlen(strtokIndx));
        locY_in_mm = atof(strtokIndx); 
      }
      if (strtokIndx[0] == 'Z'){
      memmove(strtokIndx, strtokIndx+1, strlen(strtokIndx));
        locZ_in_mm = atof(strtokIndx); 
      }
      if (strtokIndx[0] == 'P'){
      memmove(strtokIndx, strtokIndx+1, strlen(strtokIndx));
        locP_in_mm = atof(strtokIndx); 
      }
      if (strtokIndx[0] == 'E'){
      memmove(strtokIndx, strtokIndx+1, strlen(strtokIndx));
        locP_in_mm = atof(strtokIndx); 
      }
      if (strtokIndx[0] == 'R'){
      memmove(strtokIndx, strtokIndx+1, strlen(strtokIndx));
        ledR = atoi(strtokIndx); 
      }
       if (strtokIndx[0] == 'U' || strtokIndx[0] == 'G'){
      memmove(strtokIndx, strtokIndx+1, strlen(strtokIndx));
        ledG = atoi(strtokIndx); 
      }
       if (strtokIndx[0] == 'B'){
      memmove(strtokIndx, strtokIndx+1, strlen(strtokIndx));
        ledB = atoi(strtokIndx); 
      }
      
    strtokIndx = strtok (NULL, " ");
    }
    
    //***** mm to steps conversions *****
    locX_in_steps = locX_in_mm * x_steps_mm;
    locY_in_steps = locY_in_mm * y_steps_mm;
    locZ_in_steps = locZ_in_mm * z_steps_mm;
    locP_in_steps = locP_in_mm * p_steps_mm;

}

//============

void coordinateMove(){
  stepperX.setMaxSpeed(2000);
  stepperX.setAcceleration(1000);
  stepperY.setMaxSpeed(2000);
  stepperY.setAcceleration(1000);
  stepperZ.setMaxSpeed(2000);
  stepperZ.setAcceleration(1000);
  if (strcmp(mode, "G1") == 0){
    
    stepperX.moveTo(locX_in_steps);
    stepperY.moveTo(locY_in_steps);
    stepperZ.moveTo(locZ_in_steps);
    stepperP.moveTo(locP_in_steps);

    stepperX.setMaxSpeed(10000);
    stepperX.setAcceleration(3000);
    stepperY.setMaxSpeed(10000);
    stepperY.setAcceleration(4000);
    stepperZ.setMaxSpeed(10000);
    stepperZ.setAcceleration(6000);
    stepperP.setMaxSpeed(12000);
    stepperP.setAcceleration(6000);
    
    while(stepperX.targetPosition() != stepperX.currentPosition() or stepperY.targetPosition() != stepperY.currentPosition() or stepperZ.targetPosition() != stepperZ.currentPosition() or stepperP.targetPosition() != stepperP.currentPosition()){
        stepperX.run();
        stepperY.run();
        stepperZ.run();
        stepperP.run();
        delay(0.001);
        }
    Serial.println("<ok>");
  }
  
  //***** M150 - Change LED Color *****
  else if (strcmp(mode, "M150") == 0){
    for(int i=0;i<skirt_leds_num;i++){
      // skirt_leds.Color takes RGB values, from 0,0,0 up to 255,255,255
      skirt_leds.setPixelColor(i, skirt_leds.Color(ledR,ledG,ledB)); // red
      skirt_leds.show(); // This sends the updated pixel color to the hardware.
    }  
    for(int i=0;i<pipette_leds_num;i++){
      // skirt_leds.Color takes RGB values, from 0,0,0 up to 255,255,255
      pipette_leds.setPixelColor(i, pipette_leds.Color(ledR,ledG,ledB)); // red
      pipette_leds.show(); // This sends the updated pixel color to the hardware.
    }
    Serial.println("<ok>");
  }

  //***** M1001 - Laser/Mechanical probing of tip *****
  else if (strcmp(mode, "M1001") == 0){
    //Speeds and accelerations for tip probe move
    stepperX.setMaxSpeed(5000);
    stepperX.setAcceleration(2000);
    stepperY.setMaxSpeed(5000);
    stepperY.setAcceleration(2000);
    stepperZ.setMaxSpeed(5000);
    stepperZ.setAcceleration(500);
    
    boolean boolX = false;
    boolean tipcheckX = false;
    boolean tipcheckY = false;
    int coordX = stepperX.currentPosition();
    int coordY = stepperY.currentPosition();
    int coordXafter;
    int coordYafter;
    int laserXmove = coordX - 1600; //Take the current X position and move 1600 steps (20mm) in the -X direction
    int laserYmove = coordY + 8000; //Take the current Y position and move 8000 steps (20mm) in the +Y direction
  
    //Move in the -X direction until laser tripped
    stepperX.moveTo(laserXmove);
    Serial.println(stepperX.distanceToGo());
    while (boolX == false && stepperX.distanceToGo()!=0) {
    stepperX.run();
        if (digitalRead(X_LASER) != 0){
          delay(10);
          if (digitalRead(X_LASER) != 0){
            boolX= true;
            stepperX.setSpeed(0);
            coordXafter = stepperX.currentPosition();
            stepperX.move(400); //Move 5mm in the X+ direction. Now the pipette tip will be aligned with the tip that was used during the calibration on the motion controller screen.
            tipcheckX = true;
          }
        }
    }
    if (tipcheckX == false){
      stepperX.move(1600);
    }
    
    //Move back to the X starting point
    while(stepperX.targetPosition() != stepperX.currentPosition()){
      stepperX.run();
    }
  
    //Move up 10mm because the Y laser is higher
    stepperZ.move(4000);
    while(stepperZ.targetPosition() != stepperZ.currentPosition()){
        stepperZ.run();
    } 
  
     boolean boolY = false;
     stepperY.moveTo(laserYmove); 
      while (boolY == false && stepperY.distanceToGo()!=0) {
      stepperY.run();
          if (digitalRead(Y_LASER) != 0){
            delay(10);
            if (digitalRead(Y_LASER) != 0){
              boolY= true;
              stepperY.setSpeed(0);
              Serial.println(stepperY.distanceToGo());
              coordYafter = stepperY.currentPosition();
              stepperY.move(-2000); //Move 5mm in the Y- direction. Now the pipette tip will be aligned with the tip that was used during the calibration on the motion controller screen.
              tipcheckY = true;
            }
          }
      }

      if (tipcheckY == false){
      stepperY.move(-8000);
    }
      
      stepperZ.move(-4000);
      while(stepperY.targetPosition() != stepperY.currentPosition() or stepperZ.targetPosition() != stepperZ.currentPosition()){
        stepperY.run();
        stepperZ.run();
      }

      if (tipcheckY == false || tipcheckX == false){
        Serial.println("<no>");
      }
      else{
        Serial.println("<ok>");
      }
      
    }

  //***** G28 - Homing Cycle *****
  // For this code to work as written the limit switches must be located at
  // X - Maximum
  // Y - Maximum
  // Z - Maximum 
  else if (strcmp(mode, "G28") == 0){
    stepperX.setMaxSpeed(3000);
    stepperX.setAcceleration(1000);
    stepperY.setMaxSpeed(5000);
    stepperY.setAcceleration(5000);
    stepperZ.setMaxSpeed(2000);
    stepperZ.setAcceleration(1000);
     // Z-Axis Homing
    int initial_homing = stepperZ.currentPosition();
    homeZ = false;
    while (homeZ == false){
      initial_homing++;  
      stepperZ.moveTo(initial_homing);
      stepperZ.run(); 
      if (digitalRead(Z_LIMIT) != 0) {
        delay(1);
        if (digitalRead(Z_LIMIT) !=0){
          homeZ = true;
        }
      }
    }
    stepperZ.setMaxSpeed(100.0);      
    initial_homing=0;
    while (digitalRead(Z_LIMIT) == 1) { 
      initial_homing--;
      stepperZ.move(initial_homing);  
      stepperZ.runSpeed();
    }
    stepperZ.setCurrentPosition(0);
  
   // X-Axis Homing
   initial_homing = stepperX.currentPosition();
   homeX = false;
   while (homeX == false){
      initial_homing++;  
      stepperX.moveTo(initial_homing);
      stepperX.run(); 
      if (digitalRead(X_LIMIT) != 0) {
        delay(1);
        if (digitalRead(X_LIMIT) !=0){
          homeX = true;
        }
      
      }
    }
    stepperX.setMaxSpeed(100.0); 
    initial_homing=0;
    while (digitalRead(X_LIMIT) == 1) { 
      initial_homing--;
      stepperX.moveTo(initial_homing);  
      stepperX.run();
    }
    stepperX.setCurrentPosition(0);
  
  // Y-Axis Homing 
    initial_homing=stepperY.currentPosition();
    homeY = false;
    while (homeY == false){
      initial_homing++;  
      stepperY.moveTo(initial_homing);
      stepperY.run(); 
      if (digitalRead(Y_LIMIT) != 0) {
        delay(1);
        if (digitalRead(Y_LIMIT) !=0){
          homeY = true;
        }
      }
    }
    stepperY.setMaxSpeed(100.0);      
    initial_homing=0;
    while (digitalRead(Y_LIMIT) == 1) { 
      initial_homing--;
      stepperY.moveTo(initial_homing);  
      stepperY.run();
    }
    
    stepperY.setCurrentPosition(0);
    stepperY.setMaxSpeed(1000.0);      
  
  
    stepperX.setCurrentPosition(26400);
    stepperY.setCurrentPosition(144000);
    stepperZ.setCurrentPosition(0);
    stepperP.setCurrentPosition(0);
    stepperX.setMaxSpeed(10000);
    stepperX.setAcceleration(5000);
    stepperY.setMaxSpeed(10000);
    stepperY.setAcceleration(1500);
    stepperZ.setMaxSpeed(10000);
    stepperZ.setAcceleration(5000);
    Serial.println("<OK Homed>");
  }

    //########Grab Tip#########
  else if (strcmp(mode, "G38") == 0){
    //Move down until Floating head limit switch is triggered
    //The limit switch trig is debounced (50ms)

    int tipStatus = 0;
    int tipStepCount = stepperZ.currentPosition();
    int positionBeforeTip = stepperZ.currentPosition();
   
    stepperZ.setMaxSpeed(6000);
    stepperZ.setAcceleration(2000);
    
    while (tipStatus == 0){
      if (digitalRead(FLOATING_HEAD) != 0){
        
        stepperZ.setSpeed(0);
        stepperZ.moveTo(stepperZ.currentPosition());
       
        tipStatus = 1; 
      }
      else {
        tipStepCount--; 
        stepperZ.moveTo(tipStepCount);
      }
      stepperZ.run(); 
    }
    
    stepperZ.moveTo(positionBeforeTip);
    
    while(stepperZ.targetPosition() != stepperZ.currentPosition()){
      stepperZ.run();
      }
      Serial.println("<ok>");      
  }
}


  
 
