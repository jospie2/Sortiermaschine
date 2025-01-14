import cv2
import sort_driver
import time
driver = sort_driver.Serial_Driver("COM3")
time.sleep(4)
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
directory = "training_data/" + str(input("please_type_color"))
name_number = 0
driver.change_band_data(state= 1, speed= 5000)

# Bilder sammeln und einordnen
    
while True:
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('c'):#Bild aufnehmen
        cv2.imwrite(directory + "/image" + str(name_number) +".jpg", frame)
        print("success", name_number)
        name_number +=1
    if not ret:
       break
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
