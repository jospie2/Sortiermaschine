import sort_driver
import time
driver = sort_driver.Serial_Driver("COM17")
time.sleep(4)
feeder = int(input("feeder number: "))
name_number = int(input("start: "))
# Beschleunigen
driver.change_band_data(state= 1, speed= 3000)
time.sleep(1)
driver.change_band_data(state= 1, speed= 5000)
time.sleep(1)
driver.change_band_data(state= 1, speed= 7000)

    
while True:
    if not input("Hat es geklappt? Sonst geb n ein!") == "n":
        print(name_number, str(time) + " ms")
        name_number +=1
    else:
        time = int(input("delay: "))
    driver.feed_it(feeder, time)


    