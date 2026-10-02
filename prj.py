import cv2
import dlib
import argparse
from pathlib import Path

import dlib
import numpy as np

from scipy.spatial import distance as dist
from playsound import playsound


def eye_aspect_ratio(eye):

    # ... (same as your eye_aspect_ratio function)

    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Compute the euclidean distance between the horizontal eye landmark
    C = dist.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    return ear


def lip_distance(shape):

    # ... (same as your lip_distance function)

    upper_lip = shape[50:53]
    lower_lip = shape[58:61]

    if len(upper_lip) >= 3 and len(lower_lip) >= 3:

        avg_upper_lip = np.mean(upper_lip, axis=0)
        avg_lower_lip = np.mean(lower_lip, axis=0)

        distance = dist.euclidean(avg_upper_lip, avg_lower_lip)

        return distance

    else:
        return 0


parser = argparse.ArgumentParser(description="Detect drowsiness and yawning from a webcam.")
parser.add_argument(
    "--predictor",
    type=Path,
    default=Path("shape_predictor_68_face_landmarks.dat"),
    help="Path to the dlib 68-point facial landmark model.",
)
parser.add_argument(
    "--alert-sound",
    type=Path,
    default=Path("alert.wav"),
    help="Path to the alert sound WAV file.",
)
args = parser.parse_args()

# Load face detector and facial landmarks predictor
detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor(
    str(args.predictor)
)


# Constants for drowsiness detection
EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 20


# Constants for yawn detection
yawn_count = 8  # Initialize yawn_count
yawn_threshold = 35

alert_sound = str(args.alert_sound)


# Initialize the alarm status
ALARM_ON = False

COUNTER = 0  # Initialize COUNTER


# Open the webcam
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:

        shape = predictor(gray, face)

        shape = np.array(
            [(shape.part(i).x, shape.part(i).y) for i in range(68)]
        )

        left_eye = shape[42:48]
        right_eye = shape[36:42]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        avg_ear = (left_ear + right_ear) / 2.0


        # Drowsiness Detection
        if avg_ear < EYE_AR_THRESH:

            COUNTER += 1

            if COUNTER >= EYE_AR_CONSEC_FRAMES:

                if not ALARM_ON:

                    ALARM_ON = True

                    playsound(alert_sound)  # Play alert sound

                    cv2.putText(
                        frame,
                        "DROWSINESS ALERT!",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )

        else:

            COUNTER = 0
            ALARM_ON = False


        cv2.putText(
            frame,
            f"EAR: {avg_ear:.2f}",
            (300, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


        # Yawn Detection
        distance = lip_distance(shape)

        if distance > yawn_threshold:

            yawn_count += 1

            cv2.putText(
                frame,
                "Yawn Alert",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            playsound(alert_sound)  # Play alert sound


    # Display frame with annotations
    cv2.imshow("Drowsiness and Yawn Detection", frame)


    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()

cv2.destroyAllWindows()