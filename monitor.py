import cv2
import dlib
import numpy as np

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Threshold for EAR below which the eyes are considered closed
EAR_THRESHOLD = 0.25

# Initialize face detector and shape predictor (for facial landmarks)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

LEFT_EYE_INDICES = slice(36, 42)
RIGHT_EYE_INDICES = slice(42, 48)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Get video properties
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter object to save the output video
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape = np.array([(shape.part(i).x, shape.part(i).y) for i in range(68)])

        left_eye = shape[LEFT_EYE_INDICES]
        right_eye = shape[RIGHT_EYE_INDICES]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        ear = (left_ear + right_ear) / 2.0

        if ear < EAR_THRESHOLD:
            cv2.putText(frame, "Not Attentive", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Attentive", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Write the frame to the output video
    out.write(frame)

    cv2.imshow("Attentiveness Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Check if the window is closed
    if cv2.getWindowProperty("Attentiveness Detector", cv2.WND_PROP_VISIBLE) < 1:        
        break

cap.release()
out.release()
cv2.destroyAllWindows()


