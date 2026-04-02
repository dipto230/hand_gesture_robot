import cv2
import mediapipe as mp
import serial
import time
import traceback
from utils import get_finger_status

PORT = 'COM3'   # 🔁 Change this
BAUD = 9600

arduino = None

# 🔌 Connect Arduino
try:
    arduino = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)
    print(f"[INFO] ✅ Arduino connected on {PORT}")
except Exception as e:
    print("[ERROR] ❌ Arduino connection failed!")
    print(e)

# 🎥 Camera setup
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[ERROR] ❌ Camera not detected!")
    exit()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

print("[INFO] 🚀 System started. Press ESC to exit.")

while True:
    try:
        success, img = cap.read()

        if not success:
            print("[WARNING] ⚠️ Frame not captured")
            continue

        img = cv2.flip(img, 1)
        h, w, c = img.shape

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        finger_status = [0, 0, 0, 0, 0]

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:

                # 🔵 Draw landmarks
                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

                # 🟩 Bounding Box
                x_list = []
                y_list = []

                for lm in handLms.landmark:
                    x_list.append(int(lm.x * w))
                    y_list.append(int(lm.y * h))

                xmin, xmax = min(x_list), max(x_list)
                ymin, ymax = min(y_list), max(y_list)

                cv2.rectangle(img, (xmin-20, ymin-20),
                              (xmax+20, ymax+20),
                              (0, 255, 0), 2)

                # 🏷️ Label
                cv2.putText(img, "Hand", (xmin, ymin-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 255, 0), 2)

                # ✋ Finger detection
                try:
                    finger_status = get_finger_status(handLms.landmark)
                except Exception as e:
                    print("[ERROR] ❌ Finger detection failed!")
                    print(e)
                    continue

                # 🖥️ Display finger status
                text = f"T I M R P: {finger_status}"
                cv2.putText(img, text, (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0), 2)

                print("[DATA] 👉", finger_status)

                # 📤 Send to Arduino
                if arduino:
                    try:
                        data = ','.join(map(str, finger_status)) + '\n'
                        arduino.write(data.encode())
                    except Exception as e:
                        print("[ERROR] ❌ Serial write failed!")
                        print(e)

        cv2.imshow("Hand Gesture Control", img)

        if cv2.waitKey(1) & 0xFF == 27:
            print("[INFO] 👋 Exiting...")
            break

    except Exception as e:
        print("[CRITICAL ERROR] 🚨 Something crashed!")
        traceback.print_exc()
        break

# 🧹 Cleanup
cap.release()
cv2.destroyAllWindows()

if arduino:
    arduino.close()
    print("[INFO] 🔌 Arduino disconnected")