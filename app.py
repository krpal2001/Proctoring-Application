import cv2

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize variables to store previous head positions
prev_heads = []

# Capture video from webcam (change the parameter to the video file path if you want to use a video)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces and track movement
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Calculate the center of the frame
        frame_center_x, frame_center_y = frame.shape[1] // 2, frame.shape[0] // 2

        # Set an initial value for movement
        movement = "center"

        # Check if the face is approximately in the center of the frame
        center_threshold = 50  # Adjust this threshold as needed
        if frame_center_x - center_threshold < x + w // 2 < frame_center_x + center_threshold:
            movement = "center"
        else:
            # Check if this head was previously detected
            if len(prev_heads) == 0:
                prev_heads.append((x, y))
            else:
                # Calculate the change in head position
                prev_x, prev_y = prev_heads[0]
                movement = "left" if x < prev_x else "right"
                prev_heads[0] = (x, y)

        # Display the direction of head movement
        cv2.putText(frame, f"Movement: {movement}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow('Head Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close the display window
cap.release()
cv2.destroyAllWindows()
