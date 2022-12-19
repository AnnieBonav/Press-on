int LIGHT_OUTPUT = 13;
int AN_OUTPUT = 11;
int DIG_INPUT = 2;

int potenciometerValue;
int angle;

int red_light_pin= 11;
int green_light_pin = 10;
int blue_light_pin = 9;

void setup() {
  //pinMode(LIGHT_OUTPUT, OUTPUT);
  //pinMode(AN_OUTPUT, OUTPUT);
  pinMode(DIG_INPUT, INPUT);
  Serial.begin(9600);

  pinMode(red_light_pin, OUTPUT);
  pinMode(green_light_pin, OUTPUT);
  pinMode(blue_light_pin, OUTPUT);
}

void loop() {
  //turnLightOn();
  //getInputPotenciometer();
  pressButton();
  RGB_color(255, 255, 0); // Red
}

void RGB_color(int red_light_value, int green_light_value, int blue_light_value)
 {
  analogWrite(red_light_pin, red_light_value);
  analogWrite(green_light_pin, green_light_value);
  analogWrite(blue_light_pin, blue_light_value);
}

void pressButton(){
  int pressed = digitalRead(DIG_INPUT);
  if(pressed == HIGH){
    Serial.println("Pressed");
  }
}

void printPotputDelay(){
  potenciometerValue = analogRead(A0);
  angle = map(potenciometerValue, 0, 1023, 0, 255);
  Serial.print(potenciometerValue);
  Serial.println();
  delay(1000);
}

void getInputPotenciometer(){
  potenciometerValue = analogRead(A0);
  int brightness = map(potenciometerValue, 0, 1023, 0, 255);
  analogWrite(AN_OUTPUT, brightness);
  Serial.print(brightness);
  Serial.println();
  delay(200);

}

void controlLedPotenciometer(){
  
}


void turnLightOn(){
  digitalWrite(LIGHT_OUTPUT, HIGH);
  delay(1000);
  digitalWrite(LIGHT_OUTPUT, LOW);
  delay(1000);
  Serial.print("I entered the function");
  Serial.println();
}
