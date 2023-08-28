from __future__ import with_statement
import cv2
import numpy as np

# CODE WRITTEN BY JAMES ABSOLOM 2022 for Kernow Robotics #


class DetectorClass:

    def __init__(self, configPath, modelPath, classesPath):
        # Pass through variables
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        # Initialize the network and set paramaters
        self.net = cv2.dnn.readNetFromDarknet(self.configPath, self.modelPath)

        self.readClasses()

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()

        self.classesList.insert(0, '__Background__')

        print("[INFO] Loaded classes:" + str(self.classesList))

    def readFrame(self, debugMode, ret, frame, dafThreshold):

        if ret:
            blob = cv2.dnn.blobFromImage(frame, 1/255, (640, 480), (0, 0, 0),
                                         swapRB=True, crop=False)
            (H, W) = frame.shape[:2]
            self.net.setInput(blob)

            # Only runs if the code is being run in debug mode
            if debugMode:
                print("[INFO] Blobbed Shape:" + str(blob.shape))
                print("[INFO] Frame Shape:" + str(frame.shape))

            # Determine only the *output* layer names that we need from YOLO
            ln = self.net.getLayerNames()
            ln = [ln[i - 1] for i in self.net.getUnconnectedOutLayers()]
            outputs = self.net.forward(ln)

            # Initialize our lists of detected bounding boxes, confidences,
            # and class IDs, respectively
            boxes = []
            confidences = []
            classIDs = []

            # Loop over each of the layer outputs then loop over each of the
            # detections inside that layer
            for output in outputs:
                for detection in output:
                    # Extract the class ID and confidence (i.e., probability)
                    # of the current object detection
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    # Filter out weak predictions by ensuring the detected
                    # probability is greater than the minimum probability
                    if confidence > dafThreshold:
                        # Scale the bounding box coordinates back relative to
                        # the size of the image
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        # Use the center (x, y)-coordinates to derive the top
                        # and left corner of the bounding box
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        # Update our list of bounding box coordinates,
                        # confidences, and class IDs
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
            # Apply suppression to suppress weak, overlapping bounding boxes
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, dafThreshold, 0.5)
            return idxs, boxes