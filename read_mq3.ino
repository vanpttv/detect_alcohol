#define sensorDigital 2
#define LED 3
#define sensorAnalog A0
#define btn 2
int sum_analog, ave_analog;
int analog;
 
void setup() {
  pinMode(sensorDigital, INPUT);
  pinMode(btn, INPUT);
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
  while (!Serial) {
  }
  Serial.println("Raspberry");
//  char received = Serial.read();
//  Serial.print(received);
  }
void loop() {
  bool digital = digitalRead(sensorDigital);
  
//  if (Serial.available() > 0) {
    //String data = Serial.readStringUntil('\n');
    int btn_state=digitalRead(btn);
    if(btn_state==LOW){
//      Serial.print("Analog value : ");
      ave_analog=read_ave(20);
      Serial.println(ave_analog);
      digitalWrite(LED, HIGH);
//      Serial.print("Digital value :");
//      Serial.println(digital);
      delay(100);
    }
    else {
      digitalWrite(LED, LOW);
    }   
//  }
}

int read_ave(uint8_t solan)
{
  sum_analog=0;
  for(int i=0; i<solan; i++){
    analog = analogRead(sensorAnalog);
    sum_analog=sum_analog+analog;
  }
  int tb=sum_analog/1.023/solan;
  return tb;
}


