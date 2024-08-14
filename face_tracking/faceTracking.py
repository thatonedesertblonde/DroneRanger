import cv2
import numpy as np
import face_recognition as fr
import os

def preprocess_image(image_path):
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


# load the pre-trained model and weights
net = cv2.dnn.readNetFromCaffe('/app/droneranger/face_recg_models/deploy.prototxt', '/app/droneranger/face_recg_models/res10_300x300_ssd_iter_140000_fp16.caffemodel')

# open video
video_capture = cv2.VideoCapture('/app/droneranger/videos/test_1.mp4')

# get input video properties
frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


# define the codec(mp4) and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 24, (frame_width, frame_height)) #24 fps is smooth video

'''base directory of images of authorized users
to fit this for a security program, we would have to take pictures of the authorized users
when they are registering their face and store them in the authorized_users directory
under their name'''
base_directory = '/app/droneranger/authorized_users/'
authorized_users = ["Obama", "Trump", "Biden", "Will"]

# load sample pictures and get face encodings
known_face_encodings = []
known_face_names = []


for person_name in authorized_users:
    folder_path = os.path.join(base_directory, person_name.lower().replace(" ", "_"))

    # load and encode faces from the images using preprocessing
    for image_file in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_file)

        # preprocess the image
        if os.path.isfile(image_path):
            processed_image = preprocess_image(image_path)

            # if face was detected, add encoding to the list
            if processed_image is not None:
                person_face_encoding = fr.face_encodings(processed_image)
                if person_face_encoding:  # Check if face was detected
                    known_face_encodings.append(person_face_encoding[0])
                    known_face_names.append(person_name)

# loop through the video
while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # get the frame dimensions
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

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
                matches = fr.compare_faces(known_face_encodings, face_encodings[0]) # compare the face with known faces
                face_distances = fr.face_distance(known_face_encodings, face_encodings[0]) # get the distance between the face and known faces
                if face_distances.size > 0: # if there are known faces
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index] # get the name of the best match

            face_names.append(name) 

            '''put green if authorized, red if unauthorized/unknown
            this can be expanded to include access to files or whatever based off the name
            for now, we will just print the name and whether they are authorized or not'''
            color = (0,0,0)
            if name in authorized_users: 
                color = (0, 255, 0) 
            else:
                color = (0, 0, 255)

            # determin the authorization status
            authorization_status ="Unauthorized"
            if name in authorized_users:
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

     # save the frame
    out.write(frame)

    # show the video
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the video file
video_capture.release()

# save the video file 'output.mp4'
out.release()

# always do this
cv2.destroyAllWindows()