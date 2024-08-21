from ultralytics import YOLO
import numpy as np
import math
import cv2


cap = cv2.VideoCapture('/app/droneranger/videos/Cafe.mp4')
model = YOLO('/app/OD/dnn_model/yolov8x.pt')

person = 0


while cap.isOpened():


    # Read a frame from the video
    success, frame = cap.read()
    
    if success:
        frame = cv2.resize(frame, (1920, 1080))
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, verbose=False) #, persist=True)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        # annotated_frame = cv2.resize(frame, (1920, 1080))
        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

'''
    if success:
        # Run YOLOv8 inference on the frame
        results = model.predict(frame, stream=True, conf=0.5)
        if results[0].boxes.cls[0].item() == 0.0:
            person += 1
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
  
        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)
  
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break
'''