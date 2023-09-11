import Detector as DT
import cv2
import os

configPath = "C:\\Users\\NO\\Yolo-Example\\Testing Directory\\yolo-obj.cfg"
modelPath = "C:\\Users\\NO\\Yolo-Example\\Testing Directory\\yolo-obj_last.weights"
classesPath = "C:\\Users\\NO\\Yolo-Example\\Testing Directory\\obj.names"
threshold = 0.2

detector = DT.DetectorClass(configPath, modelPath, classesPath)

# Read in the frame
frame = cv2.imread("C:\\Users\\NO\\Yolo-Example\\Testing Directory\\test.jpg")
frame = cv2.resize(frame, (640, 480))

with open(classesPath, 'r') as f:
    classesList = f.read().splitlines()

# Detect the objects
idxs, boxes, classIDs, confidences = detector.readFrame(False, True, frame, threshold)
if len(idxs) > 0:
    for i in idxs.flatten():
        detected = False
        # Extract the bounding box coordinates
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])
        # Draw a bounding box rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        label = str(classesList[classIDs[i] - 1])
        confidence = str(round(confidences[i], 2))
        cv2.putText(frame, f"{label} {confidence}", (x + 5, y + 15), color=(0, 255, 0), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5)


cv2.imshow("Frame", frame)
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
