from ultralytics import YOLO
import numpy as np
import math
import cv2

# load yolov8m model
model = YOLO('/app/dnn_model/yolov8x.pt')


# load video
cap = cv2.VideoCapture('videos/Cafe.mp4')

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
size = (frame_width, frame_height)
print(size)

# create video writer
result = cv2.VideoWriter('track.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, size)


# init
count = 0
center_points_prev_frame = []
tracking_objects = {} 
track_id = 0



while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1720, 980))
    count += 1
    if not ret:
        break

    center_points_curr_frame = []
    
    # detect boxes w/ yolov8m
    detections = model(frame, conf=0.45, verbose=False)[0]
    boxes_data = detections.boxes.data.tolist()

    for data in boxes_data:
        xmin, ymin, xmax, ymax = data[0:4]
        confidence = data[4] 
        class_ids = data[5]
        class_info = model.names[class_ids]

        if class_ids == 0.0 or class_ids == 2.0 or class_ids == 4.0 or class_ids == 5.0 or class_ids == 7.0 or class_ids == 8.0:
            # calculate the center points off the corners
            cx = int((xmin + xmax) / 2)
            cy = int((ymin + ymax) / 2)
            center_points_curr_frame.append([cx, cy]) # append center points of each box

            # draw boxes
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
            class_info = model.names[class_ids]
                
            cv2.putText(frame, f"{class_info}: {confidence:.2f}", (int(xmin), int(ymin)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.95, (250, 250, 0), 2) # draws the name of the object and the confidence level next it
   
    # first two frames
    if count <= 2:
        for pt in center_points_curr_frame:
            for pt2 in center_points_prev_frame:
                distance = math.hypot(pt2[0]- pt[0], pt2[1] - pt[1])

                if distance < 45:
                    tracking_objects[track_id] = pt
                    track_id += 1
    
    else:
        tracking_objects_copy = tracking_objects.copy()
        center_points_curr_frame_copy = center_points_curr_frame.copy()


        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            for pt in center_points_curr_frame_copy:
                distance = math.hypot(pt2[0]- pt[0], pt2[1] - pt[1])

                # threashold 
                if distance < 45:
                    tracking_objects[object_id] = pt
                    object_exists = True
                    if pt in center_points_curr_frame:
                        center_points_curr_frame.remove(pt)
                    continue

            # remove ids that are lost
            if not object_exists:
                tracking_objects.pop(object_id)

        # add new id's
        for pt in center_points_curr_frame:
            tracking_objects[track_id] = pt
            track_id += 1

    # label boxes with ids
    for object_id, pt in tracking_objects.items():
        cv2.circle(frame, pt, 5, (0, 0, 5),  -1)
        cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2) # draw a circle in center, place frame #

    # show frame
    result.write(frame)
    cv2.imshow("Frame", frame)


    # copy curr to prev
    # for first two frames 
    center_points_prev_frame = center_points_curr_frame.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows() # always do this

    
