/*
Microcontrollers proyect
Ana Bonavides Aguilar
cc211010
*/
int sensorPin = A0;

int flex500gPin = A0;
int flex10kgPin = A1;

String flex1label = "500g";
String flex2label = "10kg";

float highestADC = 0;
float lowestADC = 400;

bool label = true;

float percent = 0.05;
float threshhold = 1024*percent;

int freq = 1000;

int flex1data, flex2data;

int lowerLimit = 0;
int upperLimt = 0;

long int pastTime = 0;
long int currentTime = 0;
long int totalTime = 0;

int PWMPin = 6; // LED is attached to this Pin
float VCC = 3.3; // Arduino is powered with 5V VCC
float R2 = 12000; // 10K resistor is
float sensorMinResistance = 16000; // Value of the Sensor when its flat
float sensorMaxResistance = 17500; // Value of the Sensor when its bent at 90*

int maxADCRaw = 0;
int minADCRaw = 400;

void setup() {
  Serial.begin(9600); // Initialize the serial with 9600 baud
  pinMode(flex500gPin, INPUT);
  pinMode(flex10kgPin, INPUT);
  pastTime = millis();
}

void loop() {
  totalTime = millis();
  currentTime = totalTime - currentTime;

  flex1data = analogRead(flex500gPin);

  Serial.print(flex1data);
  Serial.print(",");
  Serial.println(currentTime);
  delay(100);
}

void OldLoop() {
  int ADCRaw = analogRead(sensorPin);
  GetHighestADCRaw(ADCRaw);
  GetLowestADCRaw(ADCRaw);
  //float ADCVoltage = (ADCRaw * VCC) / 1023; // get the voltage e.g (512 * 5) / 1023 = 2.5V
  //float Resistance = R2 * (VCC / ADCVoltage - 1);
  //float ReadValue = map(Resistance, sensorMinResistance, sensorMaxResistance, 0, 255);
  //analogWrite(PWMPin, ReadValue);
  Serial.println(ADCRaw);
  //Serial.println(ReadValue);
  Serial.print("Min: ");
  Serial.print(minADCRaw);
  Serial.print("Max: ");
  Serial.println(maxADCRaw);

  delay(100);
}
void GetHighestADCRaw(float ADCRaw){
  if(ADCRaw > maxADCRaw){
    maxADCRaw = ADCRaw;
    //Serial.println(maxADCRaw);
  }
}

void GetLowestADCRaw(float ADCRaw){
  if(ADCRaw < minADCRaw){
    minADCRaw = ADCRaw;
    //Serial.println(minADCRaw);
  }
}
