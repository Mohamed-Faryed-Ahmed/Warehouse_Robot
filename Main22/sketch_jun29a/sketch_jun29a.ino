#include <Servo.h>

#define ON 1
#define OFF 0

#define dirPin_1   (22U) 
#define stepPin_1  (23U) 

#define MR_1 (31U)
#define MR_2 (33U)

#define ML_1 (35U)
#define ML_2 (37U)


#define echoPin 2
#define trigPin 3

Servo servo1; // create servo object to control a servo
Servo servo2;
Servo servo3;

bool action;

String inByte ;
String pos;
String data;
uint8_t size_in=0;
String node;

int pump_pin =30;

void setup() 
{
  servo1.attach(40); // attaches the servo on pin 9 to the servo object
  servo2.attach(42);
  servo3.attach(44);
  
  Serial.begin(9600);
  pinMode(stepPin_1, OUTPUT);
  pinMode(dirPin_1,  OUTPUT);
  pinMode(pump_pin, OUTPUT);
  pinMode(MR_1, OUTPUT);
  pinMode(MR_2, OUTPUT);
  pinMode(ML_1, OUTPUT);
  pinMode(ML_2, OUTPUT);
  pinMode(trigPin,OUTPUT);
  pinMode(echoPin,INPUT);
}

void loop() 
{
  servo1.write(0);
  servo2.write(0);
  servo3.write(180);
  
  if (Serial.available() > 0) 
  {
    while(true)
    {
      inByte = Serial.readStringUntil('\n');
      pos = Serial.readStringUntil('\n');
      size_in=sizeof(inByte);
      node=inByte[size_in -1];
      while(0 == Ultra())
      {
        Stop_move();
      }
      Move_strate();
      delay(800);
      if(inByte[3] =='L')
      {
        while(true)
        {
          /**************/
          data = Serial.readStringUntil('\n');
          Direction_move(data);
          if(data=="N")
          {
            while(0 == Ultra())
            {
               Stop_move();
            }
            Turn_right();
            delay(750);
          }
          else if(data=="M")
          {
            while(0 == Ultra())
            {
               Stop_move();
            }
            Move_strate();
            delay(800);
          }
          else if(data=="L")
          {
            while(0 == Ultra())
            {
               Stop_move();
            }
            Turn_left();
            delay(750);
            while(true)
            {
              data= Serial.readStringUntil('\n');
              Direction_move(data);
              if(data == node )
              {
                Stop_move();
                Pring(pos);
                break;
              }
              else
              {
                while(0 == Ultra())
                {
                  Stop_move();
                }
                Move_strate();
                delay(800);
              }
            }
            /////////////////////////////
          }
          else if(data =="S")
          {
            Stop_move();
            Recive();
            break;
          }
          /******************/
        }
      }
      else if(inByte[2] =='M')
      {
        while(true)
        {
          /**********/
          data = Serial.readStringUntil('\n');
          Direction_move(data);
          if(data=="N")
          {
            while(0 == Ultra())
            {
               Stop_move();
            }
            Turn_right();
            delay(750);
          }
          else if(data=="M")
          {
            while(0 == Ultra())
            {
               Stop_move();
            }
            Turn_left();
            delay(750);
            while(true)
            {
              data= Serial.readStringUntil('\n');
              Direction_move(data);
              if(data == node )
              {
                Stop_move();
                Pring(pos);
                break;
              }
              else
              {
                while(0 == Ultra())
                {
                  Stop_move();
                }
                Move_strate();
                delay(1000);
              }
            }
            /////////////////////////////
          }
          else if(data =="S")
          {
            Stop_move();
            Recive();
            break;
          }
          /*********/
        }
        ///////////////////////////
      }
      
      /////////////////////////
    }
    ///////////////////////
  }
  ///////////////////
}
/**********************************************************************************************
 *                         Function Move Definition                                           *
 **********************************************************************************************/
void Direction_move(String data)
{
  if(data == "L1")
  {
    while(0 == Ultra())
    {
      Stop_move();
    }
    Turn_right();
    delay(150);
    while(0 == Ultra())
    {
      Stop_move();
    }
    Move_strate();
    delay(500);
  }
  else if(data == "L2")
  {
    while(0 == Ultra())
    {
      Stop_move();
    }
    Turn_right();
    delay(300);
    while(0 == Ultra())
    {
      Stop_move();
    }
    Move_strate();
    delay(500);
  }
  else if(data == "R1")
  {
    while(0 == Ultra())
    {
      Stop_move();
    }
    Turn_left();
    delay(150);
    while(0 == Ultra())
    {
      Stop_move();
    }
    Move_strate();
    delay(500);
  }
  else if(data == "R2")
  {
    while(0 == Ultra())
    {
      Stop_move();
    }
    Turn_left();
    delay(300);
    while(0 == Ultra())
    {
      Stop_move();
    }
    Move_strate();
    delay(500);
  }
  else if(data == "C")
  {
    while(0 == Ultra())
    {
      Stop_move();
    }
    Move_strate();
    delay(500);
  }
  else if(data == "H")
  {
    while(0 == Ultra())
    {
      Stop_move();
    }
    Turn_left();
    delay(750);
  }
  else
  {
    Stop_move();
  }
  
}

void Turn_right()
{
  digitalWrite(MR_1,LOW);
  digitalWrite(MR_2,HIGH);

  digitalWrite(ML_1,LOW);
  digitalWrite(ML_2,HIGH);
}
void Turn_left()
{
  digitalWrite(MR_1,HIGH);
  digitalWrite(MR_2,LOW);

  digitalWrite(ML_1,HIGH);
  digitalWrite(ML_2,LOW);
}
void Move_strate()
{
  digitalWrite(MR_1,HIGH);
  digitalWrite(MR_2,LOW);

  digitalWrite(ML_1,LOW);
  digitalWrite(ML_2,HIGH);
}
void Stop_move()
{
  digitalWrite(MR_1,HIGH);
  digitalWrite(MR_2,HIGH);

  digitalWrite(ML_1,HIGH);
  digitalWrite(ML_2,HIGH);
}
void Pring(String pos)
{
  uint8_t place=0;
  if(pos =="P1")
  {
    place=3;
  }
  if(pos =="P2")
  {
    place=6;
  }
  if(pos =="P3")
  {
    place=8;
  }
  holdUp(place);
  Arm_Move(OFF);
  holdDown(place);
}
void Recive()
{
  Arm_Move(ON);
}
void Arm_Move(uint8_t on)
{
  /*pump motor*/
  pump(on);
  delay(500);
  for(int j=1;j<=4;j++)
  {
    for(int i=1;i<=45;i++)
    {
      if(j == 1)
      {
          servo1.write(0);
          servo2.write(i);
          servo3.write(180-i);
      }
      else if(j == 2)
      {
          servo1.write(i);
          servo2.write(45);
          servo3.write(135-i);
      }
      else if(j == 3)
      {
          servo1.write(45+i);
          servo2.write(45);
          servo3.write(90-i);
      }
      else if(j == 4)
      {
          servo1.write(90+i);
          servo2.write(45-i);
          servo3.write(45 + (i/2));
      }
      delay(30);
    }
  }
  servo3.write(70);
  /*pump motor*/
  on=on ^ 1;
  pump(on);
  delay(500);
    for(int j=1;j<=4;j++)
  {
    for(int i=1;i<=45;i++)
    {
      if(j == 1)
      {
          servo1.write(135 - i);
          servo2.write(i);
          servo3.write(70 - (i/2));
      }
      else if(j == 2)
      {
          servo1.write(90-i);
          servo2.write(45);
          servo3.write(45+i);
      }
      else if(j == 3)
      {
          servo1.write(45-i);
          servo2.write(45);
          servo3.write(90+i);
      }
      else if(j == 4)
      {
          servo1.write(0);
          servo2.write(45-i);
          servo3.write(135 + i);
      }
      delay(30);
    }
  }
  /*pump motor*/
  pump(OFF);
}
void pump(uint8_t on)
{
  if(on == ON)
  {
    digitalWrite(pump_pin,HIGH);
  }
  else
  {
    digitalWrite(pump_pin,LOW);
  }
}
/**********************************************************************************************
 *                    Function Plat Definition                                                *
 **********************************************************************************************/
 void holdDown(uint16_t place)/*2000 ~ 5cm*/
{
  digitalWrite(dirPin_1, HIGH); 
  // Spin the stepper motor 1 revolution slowly:
  for (uint16_t i = 0; i <(place * 2000); i++) 
  {
    // These four lines result in 1 step:
    digitalWrite(stepPin_1, HIGH);
    delay(1);
    digitalWrite(stepPin_1, LOW);
    delay(1);
  }
}

void holdUp(uint16_t place)
{
  digitalWrite(dirPin_1, LOW);
  // Spin the stepper motor 1 revolution slowly:
  for (uint16_t i = 0; i <(place*2000); i++) 
  {
    // These four lines result in 1 step:
    digitalWrite(stepPin_1, HIGH);
    delay(1);
    digitalWrite(stepPin_1, LOW);
    delay(1);
  }
}
/**********************************************************************************************************************************
 *                                                  uxlarty Func                                                                  *
 * ********************************************************************************************************************************/

 int Ultra()
{
  long dur;
  int  dis;
  
  digitalWrite(trigPin,LOW);
  digitalWrite(trigPin,LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin,LOW);
  
  dur = pulseIn(echoPin,HIGH);
  dis = (dur*0.03429/2);
  if(dis <= 20)
  {
    return 0;
  }
  else
  {
    return 1;
  }
}
