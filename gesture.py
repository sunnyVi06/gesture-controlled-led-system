import cv2
import mediapipe as mp
import serial
import time

# CHANGE COM PORT
arduino = serial.Serial('COM12', 9600)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    count = 0

    for tip, pip in zip(tips, pips):
        if hand_landmarks[tip].y < hand_landmarks[pip].y:
            count += 1

    # Thumb logic
    if hand_landmarks[4].x < hand_landmarks[3].x:
        count += 1

    return count

prev_fingers = -1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    fingers = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            fingers = count_fingers(hand_landmarks.landmark)

            if fingers != prev_fingers:
                if 1 <= fingers <= 5:
                    arduino.write(str(fingers).encode())
                else:
                    arduino.write(b'0')

                prev_fingers = fingers

    cv2.putText(frame, f"Fingers: {fingers}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("5 LED Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
