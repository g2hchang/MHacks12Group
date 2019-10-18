#include <Wire.h>

int moistureValue = 0;
int moistureValueTimeAvg = 0; // , temperatureValue, airQualityValue,
int averageOver = 20;
int moisturePin = A0;
int idValue = 1;
unsigned long timeMeasured = millis();
unsigned int slaveAddrAir = 0x5B;
unsigned int hardwareAddrAir = 0x81;
unsigned int statusAddrAir = 0x00;
unsigned int measurementModeAddrAir = 0x01;
unsigned int algoResAddrAir = 0x02;
unsigned int airMeasurementHigh = 0; // c02
unsigned int airMeasurementLow = 0; // voc

void writeI2CAir(int slaveAddr, int dataRegAddr, int valueWrite) {
  Wire.beginTransmission(byte(slaveAddr));
  Wire.write(byte(dataRegAddr));
  Wire.write(byte(valueWrite));
  Wire.endTransmission();
}

void readI2CAir(int slaveAddr, int dataRegAddr, int numBytes) {
  Serial.print("Read val0: ");
  Wire.beginTransmission(byte(slaveAddr));
  Serial.print("Read val1: ");
  Wire.write(byte(dataRegAddr));
  Serial.print("Read val2: ");
  Wire.endTransmission();
  Serial.print("Read val3: ");
  Wire.requestFrom(byte(slaveAddr), numBytes);

  if (numBytes <= Wire.available()) {
    if (numBytes == 2) {
      airMeasurementHigh = Wire.read();
      airMeasurementHigh <<= 8;
      airMeasurementHigh |= Wire.read();
    } else if (numBytes == 4) {
      airMeasurementHigh = Wire.read();
      airMeasurementHigh <<= 8;
      airMeasurementHigh |= Wire.read();
      airMeasurementHigh <<= 8;
      airMeasurementLow |= Wire.read();
      airMeasurementLow <<= 8;
      airMeasurementLow |= Wire.read();
    } else {
      int tmp = numBytes;
      int tmpVal = 0;
      Serial.print("Read val: ");
      while (tmp > 0) {
        tmpVal = Wire.read();
        Serial.print("Read val: ");
        Serial.print(tmpVal);
        Serial.print(", ");
        --tmp;
      }
      Serial.println("");
    }
  }
  delay(100);
}

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  delay(1000);
  readI2CAir(slaveAddrAir, measurementModeAddrAir, 1);
  writeI2CAir(slaveAddrAir, measurementModeAddrAir, byte(0x1));
  delay(1000);
  Serial.begin(9600);
}



void loop() {
  // put your main code here, to run repeatedly:
  moistureValue = analogRead(moisturePin);
  moistureValueTimeAvg = (moistureValueTimeAvg * 0.9 + moistureValue * 0.1);
  timeMeasured = millis();
  Serial.print("ID value: ");
  Serial.print(idValue);
  Serial.print(", time in millis: ");
  Serial.print(timeMeasured);
  Serial.print(", moisture value: ");
  Serial.print(moistureValue);
  Serial.print(", moisture value time average: ");
  Serial.print(moistureValueTimeAvg);
  readI2CAir(slaveAddrAir, algoResAddrAir, 4);
  Serial.print(", air co2: ");
  Serial.print(airMeasurementHigh);
  Serial.print(", air voc: ");
  Serial.println(airMeasurementLow);
  //delay(10);

}
