import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance
import winsound
import time
import csv

# -------------------------
# winsound  Alarm Setup
# -------------------------

def alarm():
    winsound.Beep(2500,1000)

# -------------------------
# CSV Log Setup
# -------------------------
with open("alert_logs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "Alert"])

def log_alert(alert):
    with open("alert_logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%H:%M:%S"), alert])

# -------------------------
# Face Mesh
# -------------------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Eye landmarks
LEFT_EYE = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]

# Mouth landmarks
UPPER_LIP = 13
LOWER_LIP = 14

EAR_THRESHOLD = 0.25
YAWN_THRESHOLD = 20
DROWSY_FRAMES = 20

blink_count = 0
drowsy_score = 0

# -------------------------
# EAR Function
# -------------------------
def eye_aspect_ratio(points):

    A = distance.euclidean(points[1], points[5])
    B = distance.euclidean(points[2], points[4])
    C = distance.euclidean(points[0], points[3])

    ear = (A + B) / (2.0 * C)

    return ear

# -------------------------
# Webcam
# -------------------------
cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        for face in results.multi_face_landmarks:

            h, w, _ = frame.shape

            left_eye = []
            right_eye = []

            # Left Eye
            for idx in LEFT_EYE:

                x = int(face.landmark[idx].x * w)
                y = int(face.landmark[idx].y * h)

                left_eye.append((x, y))

                cv2.circle(frame, (x, y), 2, (0,255,0), -1)

            # Right Eye
            for idx in RIGHT_EYE:

                x = int(face.landmark[idx].x * w)
                y = int(face.landmark[idx].y * h)

                right_eye.append((x, y))

                cv2.circle(frame, (x, y), 2, (0,255,0), -1)

            leftEAR = eye_aspect_ratio(left_eye)
            rightEAR = eye_aspect_ratio(right_eye)

            EAR = (leftEAR + rightEAR) / 2

            # Blink Detection
            if EAR < EAR_THRESHOLD:
                blink_count += 1

            # Drowsiness Score
            if EAR < EAR_THRESHOLD:
                drowsy_score += 1
            else:
                drowsy_score = 0

            # Alarm
            if drowsy_score > DROWSY_FRAMES:

                cv2.putText(
                    frame,
                    "DROWSINESS ALERT!",
                    (50,100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3
                )

                alarm()

                log_alert("Eye Closure Detected")

            # -------------------
            # Yawn Detection
            # -------------------
            upper = face.landmark[UPPER_LIP]
            lower = face.landmark[LOWER_LIP]

            upper_y = int(upper.y * h)
            lower_y = int(lower.y * h)

            mouth_distance = abs(lower_y - upper_y)

            if mouth_distance > YAWN_THRESHOLD:

                cv2.putText(
                    frame,
                    "YAWNING!",
                    (50,150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,0,0),
                    3
                )

                log_alert("Yawn Detected")

            # -------------------
            # Display
            # -------------------
            cv2.putText(
                frame,
                f"Blinks: {blink_count}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2
            )

            cv2.putText(
                frame,
                f"Drowsy Score: {drowsy_score}",
                (20,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,255),
                2
            )

            cv2.putText(
                frame,
                f"EAR: {EAR:.2f}",
                (20,120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255,255,0),
                2
            )

    cv2.imshow("Driver Drowsiness Detection", frame)

    key = cv2.waitKey(1)

    if key == 27:   # ESC key
        break

cap.release()
cv2.destroyAllWindows()