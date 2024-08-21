import cv2
import dlib
import mediapipe as mp
import winsound

# Initialize dlib's face detector and facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Initialize Haar cascades for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize MediaPipe hands component
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe drawing utility
mp_drawing = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Could not read frame")
        continue

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using Haar cascades
    faces_haar = face_cascade.detectMultiScale(gray, 1.3, 5)
    face_detected = len(faces_haar) > 0

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces_haar:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Detect eyes using dlib
    faces_dlib = detector(gray)
    eyes_detected = False
    for face in faces_dlib:
        landmarks = predictor(gray, face)
        for i in range(36, 48):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            eyes_detected = True

    # Detect hands using MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    hands_detected = results.multi_hand_landmarks is not None

    # Draw hand landmarks
    if hands_detected:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Check if any of the three is not detected and ring a beep if so
    if not (face_detected and eyes_detected and hands_detected):
        winsound.Beep(1000, 200)

    # Display the image
    cv2.imshow('Face, Eyes, and Hands Detection', frame)

    # Break the loop if 'q' is pressed or window is closed
    if (cv2.waitKey(10) & 0xFF == ord('q')) or (cv2.getWindowProperty('Face, Eyes, and Hands Detection', cv2.WND_PROP_VISIBLE) < 1):
        break

# Release the webcam and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()

