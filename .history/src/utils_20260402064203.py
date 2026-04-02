def get_finger_status(landmarks):
    finger_status = []

    tips_ids = [4, 8, 12, 16, 20]

    # 👉 Thumb (more stable)
    if (landmarks[4].x < landmarks[3].x and abs(landmarks[4].x - landmarks[3].x) > 0.03):
        finger_status.append(1)
    else:
        finger_status.append(0)

    # 👉 Other fingers (better threshold tuning)
    for i in range(1, 5):
        tip = landmarks[tips_ids[i]]
        lower = landmarks[tips_ids[i] - 2]

        if (lower.y - tip.y) > 0.035:   # tuned
            finger_status.append(1)
        else:
            finger_status.append(0)

    return finger_status