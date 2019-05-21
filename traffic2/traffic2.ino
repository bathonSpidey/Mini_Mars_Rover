int GREEN = 3;
//int YELLOW = 4;
int RED = 4;
int DELAY_GREEN = 1000;
int DELAY_YELLOW = 1000;
int DELAY_RED = 2000;

// basic functions
void setup()
{
  // setup LED modes
  // we're specifying that we're going to send information to this LED
  pinMode(GREEN, OUTPUT);
  //pinMode(YELLOW, OUTPUT);
  pinMode(RED, OUTPUT);
}

void loop()
{
  // High turns things on
  // Low turns things off
  digitalWrite(RED, LOW);
  digitalWrite(GREEN, HIGH);
  //digitalWrite(YELLOW, LOW);
  delay(2000);
  digitalWrite(GREEN, LOW);
  delay(500);
  digitalWrite(GREEN, HIGH);
  delay(500);
  digitalWrite(GREEN, LOW);
  delay(500);
  digitalWrite(GREEN, HIGH);
  delay(500);
  digitalWrite(GREEN, LOW);
  // how long we want the green led on
  
  //digitalWrite(GREEN, LOW);
  //digitalWrite(YELLOW, HIGH);
  //digitalWrite(RED, LOW);
  // how long we want the yellow led on
  //delay(DELAY_YELLOW);

  digitalWrite(RED, HIGH);
  //digitalWrite(YELLOW, LOW);
  delay(4000);
  digitalWrite(RED, LOW);
  delay(500);
  digitalWrite(RED, HIGH);
  delay(500);
  digitalWrite(RED, LOW);
  delay(500);
  digitalWrite(RED, HIGH);
  // how long we want the red led on
  delay(500);
}
