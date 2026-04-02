def get_finger_status(landmarks):
    finger_status = []

    tips_ids = [4, 8, 12, 16, 20]

    # Thumb (special case)
    if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x:
        finger_status.append(1)
    else:
        finger_status.append(0)

    # Other fingers
    for i in range(1, 5):
        if landmarks[tips_ids[i]].y < landmarks[tips_ids[i] - 2].y:
            finger_status.append(1)
        else:
            finger_status.append(0)

    return finger_status