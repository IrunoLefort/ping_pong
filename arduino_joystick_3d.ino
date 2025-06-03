int const pin_x = A0;
int const pin_y = A1;
int const pin_z = 4;

int x_value = 0;
int y_value = 0;
int z_value = 0;

void setup() {
  Serial.begin(9600);
  pinMode(pin_x, INPUT);
  pinMode(pin_y, INPUT);
  pinMode(pin_z, INPUT);
  digitalWrite(pin_z, HIGH);
}

void loop() {
  x_value = analogRead(pin_x);
  y_value = analogRead(pin_y);
  z_value = digitalRead(pin_z);

  Serial.print(x_value);
  Serial.print(',');
  Serial.print(y_value);
  Serial.print(',');
  Serial.println(z_value);
  delay(100);
}
