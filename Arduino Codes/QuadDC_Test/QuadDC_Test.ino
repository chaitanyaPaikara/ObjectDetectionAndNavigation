#define RPM 30
#define TICKS_PER_ROTATION1 14040
#define TICKS_PER_ROTATION2 18720
char data[100];
int i = 0;

void testRun()
{
  delay(1000);
  Serial.println("Yo!!");
  delay(3000);
  Serial1.write("p2000\r");
  delay(3000);
  Serial1.write("p5000\r");
  delay(3000);
  Serial1.write("p6240\r");
  delay(3000);
  Serial1.write("p0\r");
}

void turnMotor(int angle, int side)
{
  int tpr = 0;
  if(side == 0)
  {
    tpr = TICKS_PER_ROTATION1;
  }
  else if(side == 1)
  {
    tpr = TICKS_PER_ROTATION2;
  }
  
  long ticks = (tpr/360.0)*angle;
  char cnt[20];
  String pCmd = 'P' + String(ticks) + '\r';
  
  int i = 0;
  
  Serial.print(ticks);
  
  for(i=0; i<pCmd.length(); i++)
  {
    cnt[i] = (char)pCmd[i];
    if(side == 0)
      Serial1.write(cnt[i]);
    else if(side == 1)
      Serial2.write(cnt[i]);
  }
}

void setup() {
  Serial.begin(38400);
  Serial1.begin(38400);
  Serial2.begin(38400);
  
  turnMotor(180, 0);
  turnMotor(180, 1);
  delay(5000);
  turnMotor(360, 0);
  turnMotor(360, 1);
  delay(5000);
  turnMotor(0, 0);
  turnMotor(0, 1);

 
  
}

void loop() {
  
}
