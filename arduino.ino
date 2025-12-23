char data;

int leds[] = {8, 9, 10, 11, 12};

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 5; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);
  }
}

void loop() {
  if (Serial.available()) {
    data = Serial.read();

    // Turn all OFF first
    for (int i = 0; i < 5; i++) {
      digitalWrite(leds[i], LOW);
    }

    if (data >= '1' && data <= '5') {
      int index = data - '1';
      digitalWrite(leds[index], HIGH);
    }
  }
}
