#include <Servo.h>

Servo neck;  // Declare the servo object
int servoPin = D8;
int xPos = 0;

void setup() {
  Serial.begin(460800);
  neck.attach(servoPin);  // Attach the servo to pin D8
  Serial.println("Servo ready");
}

void loop() {
  // Existing code for servo control
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('a');  // Read data until 'a'
    xPos = data.toInt();  // Convert the received data to an integer

    // Map the amplified input (0-180) to the servo’s physical range (0-90)
    int scaledPos = map(2 * xPos, 0, 180, 0, 90);

    neck.write(scaledPos);  // Move the servo to the scaled position
    Serial.println("Servo moved to: " + String(scaledPos));
  }
}
