int mov_x = 0, mov_y = 0;
String inputString = "";         // a string to hold incoming data
String x_str = "", y_str = "";
boolean stringComplete = false;  // whether the string is complete
int ack = 101;

void _parse()
{
  int len = inputString.length();
  int i=0, j=0, k=0;
  
  for(i=0; inputString[i] != ' '; i++)
  {
    x_str += inputString[i];  
  }
  i++;
  x_str[i] = '\0';
  
  for(j=0; inputString[i] != '\n'; i++,j++)
  {
    y_str += inputString[i];  
  }
  i++;
  j++;
  y_str[j] = '\0';
  
  mov_x = x_str.toInt();
  mov_y = y_str.toInt();
}

void _print()
{
      Serial.print("\t Coordinates from PI ");
      Serial.print("\t Mov_X : "); Serial.print(mov_x);
      Serial.print("\t Mov_Y : "); Serial.println(mov_y);  
}

void reInit(){
  inputString = "";
  x_str = "";
  y_str = "";
  stringComplete = false;
}

void sendAck(){
    Serial.println(ack);
}

void handlePiData(){
  if (stringComplete) {
    _parse();
    //_print();
    sendAck();
    reInit();    
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(38400);
  inputString.reserve(10);
  x_str.reserve(4);
  y_str.reserve(4);
}

void loop() {
  // put your main code here, to run repeatedly:
  handlePiData();
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}
