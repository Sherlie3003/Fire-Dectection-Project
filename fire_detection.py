import cv2
import numpy as np
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ========== EMAIL FUNCTION ==========
def send_alert():
    sender_email = "sherlieaishwarya81@gmail.com"
    receiver_email = "sherlieaishwarya81@gmail.com"
    password = "dekdbvmdrrehjnfe"

    now = datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")

    message = MIMEText(f"🔥 FIRE DETECTED!\nTime: {time_string}")
    message["Subject"] = "URGENT: Fire Alert"
    message["From"] = sender_email
    message["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.send_message(message)
    server.quit()

# Prevent multiple emails
alert_sent = False

cap = cv2.VideoCapture("fire.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (800, 500))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_fire1 = np.array([0, 120, 70])
    upper_fire1 = np.array([10, 255, 255])

    lower_fire2 = np.array([170, 120, 70])
    upper_fire2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_fire1, upper_fire1)
    mask2 = cv2.inRange(hsv, lower_fire2, upper_fire2)

    mask = mask1 + mask2

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    fire_detected = False

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 800:
            fire_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)

    if fire_detected:
        cv2.putText(frame, "FIRE DETECTED!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 3)

        if not alert_sent:
            send_alert()
            alert_sent = True

    cv2.imshow("Advanced Fire Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()