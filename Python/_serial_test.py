import serial

# Configureer de seriële poort (vervang 'COM3' door jouw poort en pas baudrate aan indien nodig)
ser = serial.Serial('COM3', 115200)

while True:
    # Lees een regel van de seriële poort
    line = ser.readline().decode('utf-8').strip()
    print(line)
