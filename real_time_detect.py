import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('path_to_your_trained_model.pt')  # Replace with the path to your .pt file

# Initialize webcam
cap = cv2.VideoCapture(0)  # Use '0' for default webcam, or change to a specific camera index

if not cap.isOpened():
    print("Error: Cannot access the webcam.")
    exit()

# Start the video feed and run inference
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Run YOLO inference
        results = model(frame)

        # Annotate the frame with detections
        for result in results:
            for box in result.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box[:4])  # Bounding box coordinates
                confidence = float(box[4])  # Confidence score
                label = int(result.boxes.cls[0])  # Class ID

                # Add a rectangle for the bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Add text for the label and confidence
                cv2.putText(
                    frame, f"Class: {label}, Conf: {confidence:.2f}",
                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2
                )

        # Display the frame
        cv2.imshow("Real-Time Detection", frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Detection stopped by user.")

# Release resources
cap.release()
cv2.destroyAllWindows()
