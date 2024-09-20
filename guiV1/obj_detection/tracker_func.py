from ultralytics import YOLO
import face_recognition as fr
import numpy as np
import math
import cv2
import os


class stream:
    def __init__(self):
        self.cap = cv2.VideoCapture('/app/droneranger/videos/Cafe.mp4') #AirPortVideo1
        #self.cap = cv2.VideoCapture('/app/droneranger/videos/face_test_2.mp4') #AirPortVideo1
        # get incoming frame width
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        # set size of frame
        self.size = (frame_width, frame_height)
        
    def next_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (1920, 1080))
        return ret, frame

    def frame_size(self):
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        return frame_width, frame_height

    def frame_release(self):
        self.cap.release()
        
class tracker:
    red = (0, 0, 255)
    green = (25, 255, 25)
    
    def __init__(self, person, car, truck, plane, boat,
                 th_person, th_car, th_truck, th_plane, th_boat,
                 cnt_th_people, cnt_th_car, cnt_th_truck, 
                 cnt_th_plane, cnt_th_boat):

        # load yolov8m model
        self.model = YOLO('/app/OD/dnn_model/yolov8x.pt')
        # load the pre-trained model and weights
        self.net = cv2.dnn.readNetFromCaffe('/app/droneranger/face_recg_models/deploy.prototxt', '/app/droneranger/face_recg_models/res10_300x300_ssd_iter_140000_fp16.caffemodel')
        self.base_directory = '/app/droneranger/authorized_users/'
        self.authorized_users = ["Obama", "Trump", "Biden", "Alexis"]
        known_face_names, known_face_encodings = self.face_encodings()
        self.known_face_names = known_face_names
        self.known_face_encodings = known_face_encodings

        # load video
        self.stream = stream()
        frame_width, frame_height = self.stream.frame_size()
        self.frame_width = frame_width
        self.frame_height = frame_height
        # set size of frame
        self.size = (frame_width, frame_height)
        # set variables pass from gui to model
        self.person = person
        self.car = car
        self.truck = truck
        self.plane = plane
        self.boat = boat
        self.th_person = th_person
        self.th_car = th_car
        self.th_truck = th_truck
        self.th_plane = th_plane
        self.th_boat = th_boat
        self.count = 0
        self.center_points_prev_frame = []
        self.tracking_objects = {} 
        self.track_id = 0
        self.cnt_people = 0
        self.cnt_cars = 0
        self.cnt_trucks = 0
        self.cnt_planes = 0
        self.cnt_boats = 0
        self.cnt_th_people = cnt_th_people
        self.cnt_th_car = cnt_th_car
        self.cnt_th_planes = cnt_th_plane
        self.cnt_th_truck = cnt_th_truck
        self.cnt_th_boat = cnt_th_boat
        self.color=self.red
        
    def tracker_save(self):
        # create video writer
        self.result = cv2.VideoWriter('track.mp4', 
                                      cv2.VideoWriter_fourcc(*'mp4v'), 
                                      1, self.size)
    
    def print_message(self, frame, input):
        if self.color==self.red:
            self.color=self.green
        else:
            self.color=self.red 
        cv2.putText(frame, input, (1400, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, self.color, 6)
    
    def preprocess_image(self, image_path):
        # load image using face_recognition
        image = fr.load_image_file(image_path)

        # detect faces
        face_locations = fr.face_locations(image)

        if len(face_locations) == 1:
            top, right, bottom, left = face_locations[0]
            face_image = image[top:bottom, left:right]
            # convert to RGB if greyscale
            face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            return face_image
        else:
            return None  # or handle multiple/no faces found

    def face_encodings(self):
        # load sample pictures and get face encodings
        known_face_encodings = []
        known_face_names = []

        for person_name in self.authorized_users:
            folder_path = os.path.join(self.base_directory, person_name.lower().replace(" ", "_"))
            # load and encode faces from the images using preprocessing
            for image_file in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image_file)
                # preprocess the image
                if os.path.isfile(image_path):
                    processed_image = self.preprocess_image(image_path)
                    # if face was detected, add encoding to the list
                    if processed_image is not None:
                        person_face_encoding = fr.face_encodings(processed_image)
                        if person_face_encoding:  # Check if face was detected
                            known_face_encodings.append(person_face_encoding[0])
                            known_face_names.append(person_name)
        return known_face_names, known_face_encodings

    def face_recognition(self):
        ret, frame = self.stream.next_frame()
        # get the frame dimensions
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        self.net.setInput(blob)
        detections = self.net.forward()
        # create empty list for face names
        face_names = []

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # confidence threshold to hit before drawing the rectangle
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                # draw the rectangle around the face
                face = frame[startY:endY, startX:endX]
                face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face_encodings = fr.face_encodings(face_rgb)
                # if face was detected, compare it with known faces 
                name = "Unknown" # default name
                if face_encodings:
                    matches = fr.compare_faces(self.known_face_encodings, face_encodings[0]) # compare the face with known faces
                    face_distances = fr.face_distance(self.known_face_encodings, face_encodings[0]) # get the distance between the face and known faces
                    if face_distances.size > 0: # if there are known faces
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index] # get the name of the best match
                # append face to list
                face_names.append(name) 

                '''put green if authorized, red if unauthorized/unknown
                this can be expanded to include access to files or whatever based off the name
                for now, we will just print the name and whether they are authorized or not'''
                color = (0,0,0)
                if name in self.authorized_users: 
                    color = (0, 255, 0) 
                else:
                    color = (0, 0, 255)
                # determin the authorization status
                authorization_status ="Unauthorized"
                if name in self.authorized_users:
                    authorization_status = "Authorized"
                else:
                    authorization_status = "Unauthorized"                
                # put the confidence level and authorization status on top of the rectangle
                confidence_text = f"{confidence*100:.2f}% {authorization_status}"
                # draw the rectangle around the face
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)                
                # put the confidence level and authorization status on top of the rectangle
                label_size, _ = cv2.getTextSize(confidence_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                label_top = max(startY, label_size[1] + 10)
                cv2.rectangle(frame, (startX, label_top - label_size[1] - 10), (startX + label_size[0], label_top), color, cv2.FILLED)
                cv2.putText(frame, confidence_text, (startX, label_top - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # put the name of the person on the rectangle
                cv2.rectangle(frame, (startX, endY - 35), (endX, endY), color, cv2.FILLED)
                cv2.putText(frame, name, (startX + 6, endY - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        return frame    
    
    def track_objects(self, person, car, truck, plane, boat,
                      th_person, th_car, th_truck, th_plane, th_boat, 
                      cnt_th_people, cnt_th_car, cnt_th_truck, cnt_th_plane, cnt_th_boat):
        model = self.model
        #ret, frame = self.cap.read()
        ret, frame = self.stream.next_frame()
        self.count += 1
        # destroy windows if end of mp4
        if not ret:
            #self.cap.release()
            self.stream.frame_release()
            cv2.destroyAllWindows() # always do this       
        # init center points
        center_points_curr_frame = []
        # detect boxes w/ yolov8m
        detections = model(frame, classes=[0, 2, 4, 7, 8], verbose=False)[0]
        boxes_data = detections.boxes.data.tolist()

        for data in boxes_data:
            xmin, ymin, xmax, ymax = data[0:4]
            confidence = data[4] 
            class_ids = data[5]
        
            if (person == 1 and class_ids == 0.0) \
                or (car == 1 and class_ids == 2.0) \
                or (plane == 1 and class_ids == 4.0) \
                or (truck  == 1 and class_ids == 7.0) \
                or (boat == 1 and class_ids == 8.0):                
                # keep track of people detected: cnt_people
                # people_cnt_th - The value in the tkinter box for people count 
                # set color to green if threat is off.  Red for on.
                color = self.green
                if th_person == 1 and class_ids == 0.0:
                    color = self.red
                elif th_car == 1 and class_ids == 2.0:
                    color = self.red
                elif th_plane == 1 and class_ids == 4.0:
                    color = self.red
                elif th_truck == 1 and class_ids == 7.0:
                    color = self.red
                elif th_boat == 1 and class_ids == 8.0:
                    color = self.red
                
                # calculate the center points off the corners
                cx = int((xmin + xmax) / 2)
                cy = int((ymin + ymax) / 2)
                # append center points of each box
                center_points_curr_frame.append([cx, cy, class_ids]) 

                # draw boxes
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
                class_info = self.model.names[class_ids]
                # draws the name of the object and the confidence level next it
                cv2.putText(frame, f"{class_info}: {confidence:.2f}", (int(xmin), int(ymin-4)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.60, (250, 250, 0), 2) 

        # first two frames
        if self.count <= 2:
            for pt in center_points_curr_frame:
                for pt2 in self.center_points_prev_frame:
                    distance = math.hypot(pt2[0]- pt[0], pt2[1] - pt[1])

                    if distance < 55:
                        self.tracking_objects[track_id] = pt
                        track_id += 1

        else:
            tracking_objects_copy = self.tracking_objects.copy()
            center_points_curr_frame_copy = center_points_curr_frame.copy()

            for object_id, pt2 in tracking_objects_copy.items():
                object_exists = False
                for pt in center_points_curr_frame_copy:
                    distance = math.hypot(pt2[0]- pt[0], pt2[1] - pt[1])

                    # threashold 
                    if distance < 85:
                        self.tracking_objects[object_id] = pt
                        object_exists = True
                        if pt in center_points_curr_frame:
                            center_points_curr_frame.remove(pt)
                        continue

                # remove ids that are lost
                if not object_exists:
                    self.tracking_objects.pop(object_id)

            # add new id's
            for pt in center_points_curr_frame:
                self.tracking_objects[self.track_id] = pt
                #print(self.tracking_objects)
                
                match pt[2]:
                    case 0.0: 
                        if th_person == 1:
                            self.cnt_people += 1
                            if self.cnt_people > cnt_th_people:
                                self.print_message(frame, 'People Threshold Reached!!!!')
                    case 2.0: 
                        if th_car == 1:
                            self.cnt_cars += 1
                            if self.cnt_cars > cnt_th_car:
                                self.print_message(frame, 'Car Threshold Reached!!!!')
                    case 4.0: 
                        if th_plane == 1:
                            self.cnt_planes += 1
                            if self.cnt_planes > cnt_th_plane:
                                self.print_message(frame, 'Plane Threshold Reached!!!!')
                    case 7.0: 
                        if th_truck == 1:
                            self.cnt_trucks += 1
                            if self.cnt_trucks > cnt_th_truck:
                                self.print_message(frame, 'Truck Threshold Reached!!!!')
                    case 8.0: 
                        if th_boat == 1:
                            self.cnt_boats += 1
                            if self.cnt_boats > self.cnt_th_boat:
                                self.print_message(frame, 'Boat Threshold Reached!!!!')
                    case _:
                        print('Issue with case statement tracker.')
                
                self.track_id += 1

        # label boxes with ids
        #for object_id, pt in self.tracking_objects.items():
        #    cv2.circle(frame, pt[0:2], 5, (0, 0, 5),  -1)
        #    # draw a circle in center, place frame #
        #    cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2) 

        # resize frame
        #frame = cv2.resize(frame, (1920, 1080))
        
        # copy curr to prev
        # for first two frames 
        center_points_prev_frame = center_points_curr_frame.copy()

        return frame
    #cap.release()
    #cv2.destroyAllWindows() # always do this