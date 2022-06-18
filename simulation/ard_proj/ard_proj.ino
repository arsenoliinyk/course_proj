int buzzer = 37;
int led_green = 22;
int led_red = 23;


void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:..
  pinMode(buzzer, OUTPUT);
  pinMode(led_green, OUTPUT);
  pinMode(led_red, OUTPUT);

  
  digitalWrite(led_green, LOW);
  digitalWrite(led_red, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0)
  {
    String inBytes = Serial.readStringUntil('\n');
    if (inBytes == "start_led_green")digitalWrite(led_green, HIGH);
    if (inBytes == "end_led_green")digitalWrite(led_green, LOW);
    if (inBytes == "start_led_red")digitalWrite(led_red, HIGH);
    if (inBytes == "end_led_red")digitalWrite(led_red, LOW);
    if(inBytes == "buzz"){
      tone(buzzer, 1000);
      delay(1000);
      noTone(buzzer);
      }
    }
  }
