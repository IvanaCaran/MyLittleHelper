import cv2

# IP-Adresse des Raspberry Pi (ersetze durch die tatsächliche IP)
#RPI_IP = "192.168.2.105"  # Ersetze dies mit der IP-Adresse deines Raspberry Pi #zuhause
RPI_IP = "192.168.50.54"  # Raspi in PSE1
#RPI_IP = "192.168.50.53"  #Turtlebot
STREAM_URL = f"http://{RPI_IP}:5050/stream" 

cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Fehler beim Verbinden mit dem Stream.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kein Frame erhalten.")
            break
        cv2.imshow('Live Stream', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()