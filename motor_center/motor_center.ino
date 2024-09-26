#include <Servo.h>


Servo servo_x;
Servo servo_y;

void setup()
{
  servo_x.attach(12);
  servo_y.attach(13);
}

void loop()
{
  servo_x.write(90);
  servo_y.write(90);
  delay(10);
}
