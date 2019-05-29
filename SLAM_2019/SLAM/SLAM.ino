#include <Wire.h>
#include <Servo.h>
#define outputA 16
#define outputB 17
#define outputC 18
#define outputD 19
#define SLAVE_ADDRESS 0x04
#include <Timer.h>
Timer t;
double erg = 0.0;
double maximum;
byte Array[4];
byte Arr[6];
int A[4];
int p = 0;
int s;
double si = 0.0;
int W = 0;
int i = 0;
int Turn;
int counter = 0;
int aState;
int aLastState;
int bcounter = 0;
int bState;
int bLastState;

Servo tServo;

double kp = 2;
double ki = 5;
double kd = 1;
unsigned long currentTime, previousTime;
double elapsedTime;
double error;
double lastError;
double input, output, setPoint;
double cumError, rateError;
long interrupt;
int d = 2;
int k = 87;
int b = k - 45;
/*
  int HallOa = 16;
  int HallTa = 17;
  int HallOb = 18;
  int HallTb = 19;
*/
int dira = 4;
int dirb = 7;
int Speeda = 5;
int Speedb = 6;
int Aspeed = 60;
int Bspeed = 60;
int Entfg;
int Winkel;

volatile int Counta = 0;
volatile int Countb = 0;

void setup() {
  Serial.begin(38400);

  tServo.attach(23);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(7, OUTPUT);

  // Reads the initial state of the outputA
  aLastState = digitalRead(outputA);
  bLastState = digitalRead(outputC);
  t.every(600, reset);

  pinMode (outputA, INPUT_PULLUP);
  pinMode (outputB, INPUT_PULLUP);
  pinMode (outputC, INPUT_PULLUP);
  pinMode (outputD, INPUT_PULLUP);

  Wire.begin(SLAVE_ADDRESS);

  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  attachInterrupt(digitalPinToInterrupt(outputA), Reada, CHANGE);
  attachInterrupt(digitalPinToInterrupt(outputB), Reada, CHANGE);
  attachInterrupt(digitalPinToInterrupt(outputC), Readb, CHANGE);
  attachInterrupt(digitalPinToInterrupt(outputD), Readb, CHANGE);
  
      Array[0] = 0;
      Array[1] = 0;
      Array[2] = 0;
      Array[3] = 0;
}

void reset() {
  counter = 0;
  bcounter = 0;
}

void loop() {
  //A[3]=(analogRead(9));
  switch (p) {

    case 1:

      s = 1;
      Array[1] = 0;
      Array[0] = 0;
      tServo.write(b);
      erg = 0.0;
      for (int i = 0; i <= 99; i++) {
        erg = erg + analogRead(9);
      }
      erg = erg / 100.0;
      while (erg > 255.0) {
        erg = erg - 255.0;
        Array[1] = Array[1] + 1;
      }
      Array[0] = erg;
      Array[2] = b;
      b++;
      if (b == k + 46) {
        b = k - 45;
      }
      p = 0;
      break;

    case 2:
      s = 2;
      digitalWrite(dira, LOW);
      digitalWrite(dirb, LOW);
      analogWrite(Speeda, A[1]); // links
      analogWrite(Speedb, A[2]); // rechts
      /*while (Entfg > Counta or Entfg > Countb) {
        Array[0] = 0;
        }
        if (Counta >= Entfg and Countb >= Entfg) {
        Array[0] = ((Counta / 2) + (Countb / 2) / 28);
        p = 0;
        }*/
      p = 0;
      break;

    case 3:
      s = 3;
      Counta = 0;
      Countb = 0;
      Entfg = 335;
      digitalWrite(dira, HIGH);
      digitalWrite(dirb, LOW);
      analogWrite(Speeda, 90);
      analogWrite(Speedb, 90);
      while (Counta < Entfg || Countb < Entfg) {
        Entfg = 335;
      }
      p = 0;
      break;

    case 4:
      s = 4;
      digitalWrite(dira, LOW);
      digitalWrite(dirb, LOW);
      analogWrite(Speeda, 0);
      analogWrite(Speedb, 0);
      //Serial.println(s);
      p = 0;
      break;
    case 5:
      Counta = 0;
      Countb = 0;
      Array[1] = 0;
      Array[0] = 0;
      Array[2] = 0;
      Array[3] = 0;
      p = 0;
   case 6:
      s = 6;
      Counta = 0;
      Countb = 0;
      Entfg = A[3];
      digitalWrite(dira, A[1]);
      digitalWrite(dirb, A[2]);
      analogWrite(Speeda, 90);
      analogWrite(Speedb, 90);
      while (Counta < Entfg || Countb < Entfg) {
        Entfg = A[3];
      }
      p = 0;
      break;
    case 7:
      s = 7;
      Counta = 0;
      Countb = 0;
      Entfg = A[3]*2;
      digitalWrite(dira, A[1]);
      digitalWrite(dirb, A[2]);
      analogWrite(Speeda, 90);
      analogWrite(Speedb, 90);
      while (Counta < Entfg || Countb < Entfg) {
        Entfg = A[3]*2;
      }
      p = 0;
      break;
     case 8:
      s = 8;
      
      Counta = 0;
      Countb = 0;
      digitalWrite(dira, HIGH);
      digitalWrite(dirb, LOW);
      analogWrite(Speeda, 90);
      analogWrite(Speedb, 90);
      Array[0] = 0;
      Array[1] = 0;
      Entfg = 335/90*A[1];
      digitalWrite(dira, HIGH);
      digitalWrite(dirb, LOW);
      analogWrite(Speeda, 90);
      analogWrite(Speedb, 90);
      while (Counta < Entfg || Countb < Entfg) {
        Entfg = 335/90*A[1];
      }
      p = 0;
     break;

     case 9:
      s = 9;
      Counta = 0;
      Countb = 0;
      Entfg = 335;
      digitalWrite(dira, LOW);
      digitalWrite(dirb, HIGH);
      analogWrite(Speeda, 90);
      analogWrite(Speedb, 90);
      while (Counta < Entfg || Countb < Entfg) {
        Entfg = 335;
      }
      p = 0;
      break;

      case 10:
        s = 10;
        digitalWrite(dira, HIGH);
        digitalWrite(dirb, HIGH);
        analogWrite(Speeda, A[1]); // links
        analogWrite(Speedb, A[2]); // rechts
      /*while (Entfg > Counta or Entfg > Countb) {
        Array[0] = 0;
        }
        if (Counta >= Entfg and Countb >= Entfg) {
        Array[0] = ((Counta / 2) + (Countb / 2) / 28);
        p = 0;
        }*/
      p = 0;
      break;

      case 12:
        s = 12;
        Counta = 0;
        Countb = 0;
        Entfg = (A[1]*335)/90;
        digitalWrite(dira, HIGH);
        digitalWrite(dirb, LOW);
        analogWrite(Speeda, 90);
        analogWrite(Speedb, 90);
        while (Counta < Entfg || Countb < Entfg) {
          Entfg =(A[1]*335)/90;
        }
      p = 0;
      break;

      case 13:
      s = 13;
        Counta = 0;
        Countb = 0;
        Entfg =(A[1]*335)/90;
        digitalWrite(dira, LOW);
        digitalWrite(dirb, HIGH);
        analogWrite(Speeda, 90);
        analogWrite(Speedb, 90);
        while (Counta < Entfg || Countb < Entfg) {
         Entfg =(A[1]*335)/90;
        }
      p = 0;
      break;

      case 11:
        s = 11;
        encoder_read();
        digitalWrite(dira, LOW);
        digitalWrite(dirb, LOW);
      
        analogWrite(Speeda, Aspeed ); // links
        analogWrite(Speedb, Bspeed); // rechts
        int diff = abs(counter - bcounter);
        //double out = PID(diff);
        if ((abs(counter) < abs(bcounter))) {
          Aspeed =100;
      
        }
        else if (abs(counter) > abs(bcounter)) {
          Bspeed = 95; 
      
        } else {
          Aspeed = 90;
          Bspeed = 85;
        }
        t.update();

  }
}

void receiveData(int byteCount) {
  while (Wire.available()) {
    byte ar = Wire.read();
    A[i] = ar;
    i++;
  }
  i = 0;
  p = A[0];
}

void sendData() {
      //Array[1] = 0;
      //Array[0] = 0;
      //Array[2] = 0;
      //Array[3] = analogRead(9);
      Wire.write(analogRead(9));
      //delay(100);
  }

void Reada () {
  Counta++;
  if (s != 2) {
    if (Counta >= Entfg) {
      analogWrite(Speeda, 0);
    }
  }
}


void Readb () {
  Countb++;
  if (s != 2 and s != 8) {
    if (Countb >= Entfg) {
      analogWrite(Speedb, 0);
    }
  }
}

void encoder_read() {
  aState = digitalRead(outputA); // Reads the "current" state of the outputA
  // If the previous and the current state of the outputA are different, that means a Pulse has occured
  if (aState != aLastState) {
    // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
    if (digitalRead(outputB) != aState) {
      counter --;
    } else {
      counter ++;
    }
    //Serial.print(abs(counter));
    //Serial.print(" , ");
    //Serial.println(abs(bcounter));
  }
  aLastState = aState;
  bState = digitalRead(outputC); // Reads the "current" state of the outputA
  // If the previous and the current state of the outputA are different, that means a Pulse has occured
  if (bState != bLastState) {
    // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
    if (digitalRead(outputD) != bState) {
      bcounter ++;
    } else {
      bcounter --;
    }
    //Serial.print(abs(counter));
    //Serial.print(" , ");
    //Serial.println(abs(bcounter));
  }

  bLastState = bState; // Updates the previous state of the outputA with the current state
}
