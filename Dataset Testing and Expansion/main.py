from __future__ import with_statement
import cv2
import numpy as np
import os
import Detector as DT

# Paths to your model and classes
configPath = 'C:\\Users\\NO\\Yolo-Example\\Dataset Testing and Expansion\\yolo-obj.cfg'
modelPath = 'C:\\Users\\NO\\Yolo-Example\\Dataset Testing and Expansion\\yolo-obj_last.weights'
classesPath = 'C:\\Users\\NO\\Yolo-Example\\Dataset Testing and Expansion\\obj.names'

# Initialize the detector class
detector = DT.DetectorClass(configPath, modelPath, classesPath)

# Threshold for object detection
confidence_threshold = 0.5

# Path to images
image_folder = 'Dataset Testing and Expansion\input'

if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Output dataset folder
output_dataset_folder = 'Dataset Testing and Expansion\output'

if not os.path.exists(output_dataset_folder):
    os.makedirs(output_dataset_folder)

# Iterate through images
for image_name in os.listdir(image_folder):
    if image_name.endswith('.jpg') or image_name.endswith('.png'):
        image_path = os.path.join(image_folder, image_name)
        
        # Read the image
        frame = cv2.imread(image_path)
        frame = cv2.resize(frame, (640, 480))
        saved = False
        
        # Get detections using your DetectorClass
        idxs, boxes, classIDs, confidences = detector.readFrame(debugMode=False, ret=True, frame=frame, dafThreshold=confidence_threshold)
        
        if len(idxs) > 0:
            for i in idxs.flatten():
                detected = False
                # Extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                label = str(detector.classesList[classIDs[i] + 1])
                confidence = str(round(confidences[i], 2))

                framecopy = frame.copy()

                # Draw a bounding box rectangle
                cv2.rectangle(framecopy, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(framecopy, f"{label} {confidence}", (x + 5, y + 15), color=(0, 255, 0), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5)

                if w > 0 and h > 0:
                    # Show ROI to user and ask for input (Yes/No)
                    cv2.imshow("ROI", framecopy)
                    
                    key = cv2.waitKey(0)
                    if key == ord('y'):
                        
                        if saved == False:
                            saved = True
                            roi_filename = f"{detector.classesList[classIDs[i]]}_{image_name}"
                            roi_filepath = os.path.join(output_dataset_folder, roi_filename)
                            cv2.imwrite(roi_filepath, frame)

                        # Create YOLO annotation file
                        annotation_filename = f"{detector.classesList[classIDs[i]]}_{os.path.splitext(image_name)[0]}.txt"
                        annotation_filepath = os.path.join(output_dataset_folder, annotation_filename)
                        
                        with open(annotation_filepath, 'a') as annotation_file:
                            normalized_x = (x + w / 2) / frame.shape[1]
                            normalized_y = (y + h / 2) / frame.shape[0]
                            normalized_width = w / frame.shape[1]
                            normalized_height = h / frame.shape[0]
                            
                            annotation = f"{classIDs[i]} {normalized_x:.6f} {normalized_y:.6f} {normalized_width:.6f} {normalized_height:.6f}"
                            annotation_file.write(annotation)
                            annotation_file.write("\n")

                        
                    if key == ord('n'):
                        break
                    cv2.destroyAllWindows()