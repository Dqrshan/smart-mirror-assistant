#include <LiquidCrystal.h>

// LCD Pins: RS, EN, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2); // Adjust dimensions if necessary
  lcd.print("Smart Mirror Ready");
}

void loop() {
  if (Serial.available()) {
    lcd.clear();
    String message = Serial.readStringUntil('\n');
    lcd.print(message);
  }
}
