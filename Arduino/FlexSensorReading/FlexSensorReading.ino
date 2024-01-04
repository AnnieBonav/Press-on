int sensorPin = A0;
float highestADC = 0;
float lowestADC = 400;

int lowerLimit = 0;
int upperLimt = 0;
byte i = 1;

char num[10];
int m;
void setup() {
  Serial.begin(9600);
  pinMode(sensorPin, INPUT);
}

void loop() {
  int ADCRaw = analogRead(sensorPin);
  //m = sprintf(num, " %3d:  %5d    ", i,ADCRaw);
  //m = sprintf(num, "%4d", i, ADCRaw);
  //m = sprintf(num, "%4d", ADCRaw);
  //ADCRaw = map(ADCRaw, 0, 1023, 0, 100);
  //GetHighestADCRaw(ADCRaw);
  //GetLowestADCRaw(ADCRaw);
  //Serial.println(num);
  //Serial.println("%04d", ADCRaw);
  Serial.println(ADCRaw);
  delay(100);
}

void GetHighestADCRaw(float ADCRaw){
  if(ADCRaw > highestADC){
    highestADC = ADCRaw;
  }

  Serial.print("Min: ");
  Serial.print(lowestADC);
}

void GetLowestADCRaw(float ADCRaw){
  if(ADCRaw < lowestADC){
    lowestADC = ADCRaw;
  }

  Serial.print("Max: ");
  Serial.println(highestADC);
}
