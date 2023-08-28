import Detector as DT
import cv2

configPath = "yolo-obj.cfg"
modelPath = "yolo-obj_last.weights"
classesPath = "obj.names"
threshold = 0.7

detector = DT.DetectorClass(configPath, modelPath, classesPath)

# Read in the frame
frame = cv2.imread("test.jpg")

# Detect the objects
idxs, boxes = detector.readFrame(False, True, frame, threshold)
if len(idxs) > 0:
    for i in idxs.flatten():
        detected = False
        # Extract the bounding box coordinates
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])
        # Draw a bounding box rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Frame", frame)
if cv2.waitKey(1) & 0xFF == ord('q'):
    cv2.destroyAllWindows()

