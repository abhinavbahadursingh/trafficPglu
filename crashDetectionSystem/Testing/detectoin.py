import cv2
from ultralytics import YOLO


#load yolo model

model= YOLO("yolo11n.pt")


class_list=model.names
videoPath=r"E:\makeForLkoTrafficCrash\test_videos\test (16).mp4"
cap=cv2.VideoCapture(videoPath)

while cap.isOpened():
    ret,frame=cap.read()
    if not ret or frame is None:
        break

    # Run YOLO tracking on the frame
    results = model.track(frame, persist=True)

    if results and results[0].boxes is not None and results[0].boxes.data is not None:
                # Get the detected boxes, their class indices, and track IDs
                boxes = results[0].boxes.xyxy.cpu().numpy()
                track_ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.id is not None else []
                class_indices = results[0].boxes.cls.cpu().numpy() if results[0].boxes.cls is not None else []
                confidences = results[0].boxes.conf.cpu().numpy() if results[0].boxes.conf is not None else []



                # Loop through each detected object
                for i in range(len(track_ids)):
                    if i >= len(boxes) or i >= len(class_indices):
                        continue  # Safety check

                    x1, y1, x2, y2 = map(int, boxes[i])

                    cx = (x1 + x2) // 2  # Calculate the center point
                    cy = (y1 + y2) // 2

                    # Get the class name using the class index
                    class_name = class_list[class_indices[i]]

                    # Draw a dot at the center and display the tracking ID and class name
                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                    cv2.putText(frame, f"ID: {track_ids[i]} {class_name}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("YOLO Object Tracking & Counting", frame)
    # manager.run_all()
    # fireBase_Queue.stop_worker()
    # Exit loop if 'ESC' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

    # Release resources
cap.release()
cv2.destroyAllWindows()