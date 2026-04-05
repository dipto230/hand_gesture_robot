import cv2
import mediapipe as mp
import serial
import time
import traceback
import os
import shutil
from utils import get_finger_status

# 🧹 Clear cache and terminal on startup
try:
    os.system('cls')  # Clear terminal (Windows)
except:
    os.system('clear')  # Clear terminal (Linux/Mac)

# Remove __pycache__ directories
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        pycache_path = os.path.join(root, '__pycache__')
        try:
            shutil.rmtree(pycache_path)
            print(f"[INFO] 🧹 Cleared cache: {pycache_path}")
        except:
            pass

PORT = 'COM7'
BAUD = 9600

arduino = None
serial_error_count = 0

def connect_arduino():
    """Reconnect to Arduino with error handling"""
    global arduino
    try:
        if arduino:
            try:
                arduino.close()
            except:
                pass
        
        arduino = serial.Serial(PORT, BAUD, timeout=2)
        time.sleep(2)
        
        # Wait for READY signal
        max_attempts = 10
        while max_attempts > 0:
            if arduino.in_waiting:
                response = arduino.readline().decode().strip()
                if response == "READY":
                    print(f"[INFO] ✅ Arduino connected on {PORT}")
                    return True
            time.sleep(0.1)
            max_attempts -= 1
        
        print(f"[INFO] ✅ Arduino connected on {PORT} (no response)")
        return True
    except Exception as e:
        arduino = None
        print(f"[ERROR] ❌ Arduino connection failed: {e}")
        return False

# 🔌 Initial Arduino connect
connect_arduino()

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
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

print("[INFO] 🚀 System started. Press ESC to exit.")

# 🔥 Stability variables
prev_finger = [0, 0, 0, 0, 0]
stable_count = 0
stable_output = [0, 0, 0, 0, 0]

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

                # 🔥 Stability filter
                if finger_status == prev_finger:
                    stable_count += 1
                else:
                    stable_count = 0

                prev_finger = finger_status.copy()

                if stable_count > 3:
                    stable_output = finger_status.copy()

                    print("[STABLE] 👉", stable_output)

                    # 📤 Send to Arduino with retry
                    if arduino:
                        try:
                            data = ','.join(map(str, stable_output)) + '\n'
                            print(f"[DEBUG] Sending: {data.strip()}")
                            arduino.write(data.encode())
                            arduino.flush()
                            time.sleep(0.05)
                            serial_error_count = 0
                        except Exception as e:
                            serial_error_count += 1
                            print(f"[ERROR] ❌ Serial write failed! (attempt {serial_error_count})")
                            print(f"     {type(e).__name__}: {e}")
                            
                            # Auto-reconnect after 3 failures
                            if serial_error_count >= 3:
                                print("[INFO] 🔄 Attempting to reconnect Arduino...")
                                if connect_arduino():
                                    serial_error_count = 0
                    elif serial_error_count == 0:
                        # Try to connect if arduino was None
                        print("[INFO] ⚠️  Arduino not connected. Attempting to reconnect...")
                        connect_arduino()

                # 🖥️ Display
                text = f"T I M R P: {stable_output}"
                cv2.putText(img, text, (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

        cv2.imshow("Hand Gesture Control", img)

        key = cv2.waitKey(1)
        if key == 27:
            print("[INFO] 👋 Exiting...")
            break

        time.sleep(0.1)

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