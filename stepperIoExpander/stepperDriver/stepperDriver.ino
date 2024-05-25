#include <AccelStepper.h>

// Define stepper motor connections and interface type for the first motor
#define STEP_PIN1 5
#define DIR_PIN1 2
#define ENA_PIN1 8 // Optional, if you use the enable pin

// Define stepper motor connections and interface type for the second motor
#define STEP_PIN2 6
#define DIR_PIN2 3
#define ENA_PIN2 9 // Optional, if you use the enable pin

// Create instances of the AccelStepper class
AccelStepper stepper1(AccelStepper::DRIVER, STEP_PIN1, DIR_PIN1);
AccelStepper stepper2(AccelStepper::DRIVER, STEP_PIN2, DIR_PIN2);

void setup() {
  // Set the maximum speed and acceleration for the stepper motors
  stepper1.setMaxSpeed(1000); // Maximum speed in steps per second
  stepper1.setAcceleration(500); // Acceleration in steps per second^2

  stepper2.setMaxSpeed(1000); // Maximum speed in steps per second
  stepper2.setAcceleration(500); // Acceleration in steps per second^2

  // Initialize serial communication
  Serial.begin(9600);
  Serial.println("Enter positions in steps for both motors in the format: position1,position2");

  // Initialize enable pins if used
  pinMode(ENA_PIN1, OUTPUT);
  digitalWrite(ENA_PIN1, LOW); // Enable the driver (LOW might be the active state, check your driver documentation)

  pinMode(ENA_PIN2, OUTPUT);
  digitalWrite(ENA_PIN2, LOW); // Enable the driver (LOW might be the active state, check your driver documentation)
}

void loop() {
  // Check if there is any input from the serial monitor
  if (Serial.available() > 0) {
    String input = readSerialLine(); // Read the input line
    int commaIndex = input.indexOf(','); // Find the comma separating the two positions
    if (commaIndex > 0) {
      long position1 = input.substring(0, commaIndex).toInt(); // Get the first position
      long position2 = input.substring(commaIndex + 1).toInt(); // Get the second position

      stepper1.moveTo(position1); // Move the first stepper to the new position
      stepper2.moveTo(position2); // Move the second stepper to the new position

      // Move the steppers to the new positions with acceleration/deceleration
      while (stepper1.distanceToGo() != 0 || stepper2.distanceToGo() != 0) {
        stepper1.run();
        stepper2.run();
      }

      // Print the new positions
      Serial.print("Moved to positions: ");
      Serial.print(position1);
      Serial.print(", ");
      Serial.println(position2);
      Serial.println("Enter new positions in steps:");
    } else {
      Serial.println("Invalid input format. Please enter positions in the format: position1,position2");
    }
  }
}

// Function to read a line of input from the serial monitor
String readSerialLine() {
  String input = "";
  while (true) {
    if (Serial.available() > 0) {
      char ch = Serial.read();
      if (ch == '\n') {
        break;
      } else {
        input += ch;
      }
    }
  }
  return input;
}
