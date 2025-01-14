import cv2
import numpy as np
from functools import cache

#groeßten Farbkleks finden und zurückgeben
def find_biggest_blob(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        biggest_contour = max(contours, key=cv2.contourArea)

        return biggest_contour

    else:
        return None

# Punkte finden und deren Farbwerte zurückgeben
def get_points(image, blob_contour):
    x,y = None,None
    cv2.imshow("getpoints",image)
    M = cv2.moments(blob_contour)
    values_at_points = []
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        # Punkte auf dem Lego finden 
        points = [(int(cx - 0.25 * (cx - min(blob_contour[:, :, 0].flatten()))), cy),
                  (int(cx + 0.25 * (max(blob_contour[:, :, 0].flatten()) - cx)), cy),
                  (cx, int(cy - 0.25 * (cy - min(blob_contour[:, :, 1].flatten())))),
                  (cx, int(cy + 0.25 * (max(blob_contour[:, :, 1].flatten()) - cy)))]

        for point in points:
            x, y = point

            if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                values_at_points.append([value for value in image[y,x]])
                cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
    return [image, values_at_points, [y,x]]


def get_data(empty_image_path, frame, contrast, crop, show_option = 0, last_frame = None):
    empty_image = last_frame #cv2.imread(empty_image_path)[crop[0]:crop[1], crop[2]:crop[3]]

    # beide in Scharzweiß umandeln
    empty_gray = cv2.cvtColor(empty_image, cv2.COLOR_BGR2GRAY)
    object_gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

    # Differenz der Bilder errechnen
    diff = cv2.absdiff(empty_gray, object_gray)

    # Schwellenwert anwenden
    _, thresholded = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    # Konturen finden
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Maske erstellen
    mask = np.zeros_like(empty_image)
    cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Die Maske auf das Bild anwenden
    result = cv2.bitwise_and(contrast, mask)


    # Ergebniss in rot gruen und Blau kanäle aufteilen
    blue, green, red = cv2.split(result)


    # mit Farbwerten schwellenwerte erstllen 
    _, red_mask = cv2.threshold(red, 200, 255, cv2.THRESH_BINARY)
    _, yellow_mask = cv2.threshold(np.uint8((red / 2) + (green / 2)), 200, 255, cv2.THRESH_BINARY)
    _, blue_mask = cv2.threshold(blue, 200, 255, cv2.THRESH_BINARY)
    # Groeßten Farbkleks finden 
    red_blob_contour = find_biggest_blob(red_mask)
    yellow_blob_contour = find_biggest_blob(yellow_mask)
    blue_blob_contour = find_biggest_blob(blue_mask)

    values = [[],[],[]]
    blob_len = [(len(red_blob_contour) if red_blob_contour is not None else 0), (len(yellow_blob_contour) if yellow_blob_contour is not None else 0) , (len(blue_blob_contour) if blue_blob_contour is not None else 0)] 
    index_of_biggest_blob = blob_len.index(max(blob_len))

    cords = [None, None]
    if True:
        if red_blob_contour is not None and index_of_biggest_blob == 0:

            image, values, cords = get_points(frame, red_blob_contour)
            cv2.drawContours(frame, [red_blob_contour], -1, 255, 0)

        elif yellow_blob_contour is not None and index_of_biggest_blob == 1:

            image, values, cords = get_points(frame, yellow_blob_contour)
            cv2.drawContours(frame, [yellow_blob_contour], -1, 255, 0)
            
        elif blue_blob_contour is not None and index_of_biggest_blob == 2:

            image, values, cords = get_points(frame, blue_blob_contour)
            cv2.drawContours(frame, [blue_blob_contour], -1, 255, 0)
            

    #Ergebnisse anzeigen
    cv2.imshow("orig", frame)
    cv2.imshow('Result', result)
    cv2.imshow('contrast', contrast)
    if show_option >= 0:
        pass
    if show_option == 1:
        cv2.imshow("red  ", red_mask)
        cv2.imshow("yellow  ", yellow_mask)
        cv2.imshow("blue  ", blue_mask)
    return [values, cords]


