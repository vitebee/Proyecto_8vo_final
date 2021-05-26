print("Loading - 0%")
import face_recognition
import cv2
import numpy as np
import RPi.GPIO as IO
import time
print("Loading - 20%")

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
print("Loading - 40%")

edy_image = face_recognition.load_image_file("edy.jpg")
edy_face_encoding = face_recognition.face_encodings(edy_image)[0]
print("Loading - 60%")

dad_image = face_recognition.load_image_file("dad.jpg")
dad_face_encoding = face_recognition.face_encodings(dad_image)[0]
print("Loading - 80%")

# Create arrays of known face encodings and their names
known_face_encodings = [
    dad_face_encoding,
    edy_face_encoding
]
known_face_names = [
    "Dad",
    "Edy Toba"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
IO.setwarnings(False)
process_this_frame = True
IO.setmode(IO.BOARD)
IO.setup(36, IO.IN)
IO.setup(38, IO.IN)
IO.setup(40, IO.IN)
IO.setup(8, IO.OUT)
IO.setup(10, IO.OUT)
button = IO.input(36)
buttonC = IO.input(38)
sensor = IO.input(40)
IO.output(8, 0)
IO.output(10,0)
ticks = 0
status = 0
contra = 0
time = 0
regreso = 0
password = "1998"
print("Loading - 100%")
while True:
    while status == 0:
        button = IO.input(36)
        if button == 0:
            status = 1

    while status == 1:
        # Grab a single frame of video
        ret, img = video_capture.read()
        frame = cv2.flip(img, -1) 
        
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Only process every other frame of video to save time
        if process_this_frame:
            
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    ticks = ticks + 1
                elif name == "Unknown":
                    ticks = 0
                face_names.append(name)
        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('p'):
            contra = input("password?")
        # Hit 'q' on the keyboard to quit!
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if ticks >= 20 or password == contra:
            IO.output(10, 1)
            sensor = IO.input(40)
            if sensor == 1:
                time = time + 1
        if sensor == 0:
            IO.output(10,0)
            IO.output(8,0)
            contra = "0"
            ticks = 0
            buttonC = IO.input(38)
        if buttonC == 0:
            regreso = 1
        if regreso == 1:
            if time > 0 :
                IO.output(8,0)
                time = time - 1
            elif time == 0:
                IO.output(8,0)
                status = 2
                break
            IO.output(8,1)
    if status == 2:
    # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        break
