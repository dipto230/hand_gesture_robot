# 🖐️ Hand Gesture Controlled Robotic Hand

Control a robotic hand in real-time using your webcam and hand gestures.

## 🚀 Features

* Real-time hand tracking
* Finger detection (5 fingers)
* Live visual feedback
* Arduino servo control

## 🧰 Tech Stack

* Python (OpenCV, MediaPipe)
* Arduino (Servo control)
* Serial Communication

## 📦 Setup

### 1. Clone repo

```
git clone <your-repo-url>
cd hand-gesture-robot
```

### 2. Create virtual environment

```
python -m venv venv
```

### 3. Activate

Windows:

```
venv\Scripts\activate
```

Mac/Linux:

```
source venv/bin/activate
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

## ▶️ Run

1. Upload Arduino code
2. Connect Arduino
3. Update COM port in `main.py`
4. Run:

```
python src/main.py
```

## 🎯 Controls

* Open finger → Servo open
* Close finger → Servo close

## ⚠️ Notes

* Use external power for servos
* Ensure common ground
* Adjust angles if needed

## 📸 Output

Live webcam feed with finger status:

```
T I M R P: [1, 0, 1, 0, 1]
```

## 🔮 Future Improvements

* Gesture recognition (thumbs up 👍)
* Wireless control (ESP32)
* Smooth servo motion
