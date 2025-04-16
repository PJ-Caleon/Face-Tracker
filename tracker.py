import cv2
import serial
import time

# Initialize serial communication with the servo motor
port = serial.Serial('COM4', 460800, timeout=1)  # Adjust to your port
time.sleep(2)  # Allow time for the connection to stabilize

# Initialize OpenCV video capture and face detector
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# Updated mapping of face center x positions to servo angles
angle_mapping = {
    "right": (230, 180),
    "r1": (248, 162),
    "r2": (266, 144),
    "r3": (284, 126),
    "r4": (302, 108),
    "center": (320, 90),
    "l1": (340, 72),
    "l2": (360, 54),
    "l3": (380, 36),
    "l4": (400, 18),
    "left": (420, 0)
}

def determine_position(face_center_x):
    """
    Determine the servo angle based on the face center x position.
    """
    angle = None

    # Check the face center x against the mapping
    if face_center_x <= angle_mapping["right"][0]:
        angle = angle_mapping["right"][1]  # 180 degrees
        print("Position: Right")
    elif face_center_x <= angle_mapping["r1"][0]:
        angle = angle_mapping["r1"][1]  # 162 degrees
        print("Position: R1")
    elif face_center_x <= angle_mapping["r2"][0]:
        angle = angle_mapping["r2"][1]  # 144 degrees
        print("Position: R2")
    elif face_center_x <= angle_mapping["r3"][0]:
        angle = angle_mapping["r3"][1]  # 126 degrees
        print("Position: R3")
    elif face_center_x <= angle_mapping["r4"][0]:
        angle = angle_mapping["r4"][1]  # 108 degrees
        print("Position: R4")
    elif face_center_x <= angle_mapping["center"][0]:
        angle = angle_mapping["center"][1]  # 90 degrees
        print("Position: Center")
    elif face_center_x <= angle_mapping["l1"][0]:
        angle = angle_mapping["l1"][1]  # 72 degrees
        print("Position: L1")
    elif face_center_x <= angle_mapping["l2"][0]:
        angle = angle_mapping["l2"][1]  # 54 degrees
        print("Position: L2")
    elif face_center_x <= angle_mapping["l3"][0]:
        angle = angle_mapping["l3"][1]  # 36 degrees
        print("Position: L3")
    elif face_center_x <= angle_mapping["l4"][0]:
        angle = angle_mapping["l4"][1]  # 18 degrees
        print("Position: L4")
    elif face_center_x <= angle_mapping["left"][0]:
        angle = angle_mapping["left"][1]  # 0 degrees
        print("Position: Left")
    
    # Send the angle to the servo via serial if determined
    if angle is not None:
        print(f"Face Center X: {face_center_x}, Sending Angle: {angle}a")  # Debugging print
        port.write(f"{angle}a".encode())

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(40, 40))

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            # Draw a rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Calculate the center X position of the face
            face_center_x = x + (w//2)

            # Determine and update the servo position based on face center x
            determine_position(face_center_x)
    else:
        print("No face detected.")  # Debugging print

    # Display the video feed
    cv2.imshow('Video', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
port.close()  # Close the serial port when done
