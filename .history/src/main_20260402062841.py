import cv2
import mediapipe as mp
import serial
import time
import traceback
from utils import get_finger_status

PORT = 'COM3'
BAUD = 9600

arduino = None

# 🔌 Arduino connect
try:
    arduino = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)
    print(f"[INFO] ✅ Arduino connected on {PORT}")
except Exception as e:
    print("[ERROR] ❌ Arduino connection failed!")
    print(e)

# 🎥 Camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(3, 640)
cap.set(4, 480)

if not cap.isOpened():
    print("[ERROR] ❌ Camera not detected!")
    exit()

# 🤖 MediaPipe setup
try:
    mp_hands = mp.solutions.hands
except AttributeError:
    print("[ERROR] ❌ Mediapipe broken! Reinstall it.")
    exit()

hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

mp_draw = mp.solutions.drawing_utils

print("[INFO] 🚀 System started. Press ESC to exit.")

frame_count = 0

while True:
    try:
        success, img = cap.read()

        if not success:
            print("[WARNING] ⚠️ Frame not captured")
            continue

        # 🔥 Reduce CPU load
        frame_count += 1
        if frame_count % 2 != 0:
            continue

        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        finger_status = [0, 0, 0, 0, 0]

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

                try:
                    finger_status = get_finger_status(handLms.landmark)
                except Exception as e:
                    print("[ERROR] ❌ Finger detection failed!")
                    print(e)
                    continue

                # 🖥️ Display
                text = f"T I M R P: {finger_status}"
                cv2.putText(img, text, (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

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

        key = cv2.waitKey(1)
        if key == 27:
            print("[INFO] 👋 Exiting...")
            break

        time.sleep(0.02)

    except Exception as e:
        print("[CRITICAL ERROR] 🚨 Crash detected!")
        traceback.print_exc()
        break

# 🧹 Cleanup
cap.release()
cv2.destroyAllWindows()

if arduino:
    arduino.close()
    print("[INFO] 🔌 Arduino disconnected")