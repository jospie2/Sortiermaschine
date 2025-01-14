import cv2
import time
import image_processing
import os
import numpy as np
import json
from numpy import asarray
from numpy import savetxt
bs = cv2.createBackgroundSubtractorMOG2()
training = True


crop = [100,480, 275,390]

red_iamges =  os.listdir("training_data/red")
yellow_iamges =  os.listdir("training_data/yellow")
blue_iamges =  os.listdir("training_data/blue")
empty_images = ["empty.jpg"]


def find_biggest_blob(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        biggest_contour = max(contours, key=cv2.contourArea)

        return biggest_contour

    else:
        return None

def get_points(image, blob_contour):
    M = cv2.moments(blob_contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        # Define points within the blob, distributed towards the center
        points = [(int(cx - 0.25 * (cx - min(blob_contour[:, :, 0].flatten()))), cy),
                  (int(cx + 0.25 * (max(blob_contour[:, :, 0].flatten()) - cx)), cy),
                  (cx, int(cy - 0.25 * (cy - min(blob_contour[:, :, 1].flatten())))),
                  (cx, int(cy + 0.25 * (max(blob_contour[:, :, 1].flatten()) - cy)))]
        values_at_points = []
        for point in points:
            x, y = point

            if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                values_at_points.append([value for value in image[y,x]])
                print(f"RGB value at ({x}, {y}): {image[y, x]}")
                cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
        print(values_at_points)
        return [image, values_at_points]
color: str = ""
for color_pointer in range(0,3):
    color_pointer = 2
    print(color_pointer)
    match color_pointer:
        case 0:
            current_images = red_iamges
            path = "training_data/red/"
            color = "red"
        case 1:
            current_images = yellow_iamges
            path = "training_data/yellow/"
            color = "yellow"
        case 2:
            current_images = blue_iamges
            path = "training_data/blue/"
            color = "blue"

    empty_image = "empty.jpg"
    for image_name in current_images:


        frame = cv2.imread(path + image_name)[crop[0]:crop[1], crop[2]:crop[3]]
        values = image_processing.magic(empty_image, frame, crop = crop, show_option= 1)
        print(values)
        #savetxt(color + '.csv', data, delimiter=',')
        existing_data = np.loadtxt(color+ '.csv', delimiter=',', dtype=int)


        new_array = np.array(values)
        print(len(existing_data))
        appended_data = new_array

        if not len(existing_data) == 0 and not len(new_array) == 0:
            appended_data = np.vstack((existing_data, new_array))
            
        # speichern
        np.savetxt(color+'.csv', appended_data, delimiter=',', fmt='%d')

        while not cv2.waitKey(1) & 0xFF == ord('a'):
            pass
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cv2.destroyAllWindows()
