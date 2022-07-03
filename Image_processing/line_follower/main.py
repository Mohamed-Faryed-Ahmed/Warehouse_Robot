import numpy as np
import cv2
import line_classifier as LC
import time

import serial

#serial1 = serial.Serial('/dev/ttyACM0', 9600)
if __name__ == '__main__':
    serial1 = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    serial1.reset_input_buffer()

#serial1.write(b"ack\n")
        
#import qrDetector

##### loading learned model and get score #####

model = LC.load_model("./line_classifier/model")

def QR_detector ():
        detector=cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)
        #if data in stored:
       #         continue
        #stored.append(data)
        # if there is a bounding box, draw one, along with the data
        return(data)


def QR_det (data):
    if (data == 's'):
        serial1.write(b"S\n")
    if (data == 'N'):
        serial1.write(b"N\n")
    if (data == 'M'):
        serial1.write(b"M\n")
    if (data == 'L'):
        serial1.write(b"L\n")
    if (data == 'a'):
        serial1.write(b"A\n")
    if (data == 'b'):
        serial1.write(b"B\n")
    if (data == 'c'):
        serial1.write(b"C\n")
    if (data == 'x'):
        serial1.write(b"X\n")
    if (data == 'y'):
        serial1.write(b"Y\n")
    if (data == 'z'):
        serial1.write(b"Z\n")
    if (data == 'i'):
        serial1.write(b"I\n")
    if (data == 'j'):
        serial1.write(b"J\n")
    if (data == 'k'):
        serial1.write(b"K\n")

def Dir_Line(direct):
    if(direct == "lef1"):
       serial1.write(b"L1\n")
    if(direct == "left2"):
       serial1.write(b"L2\n")
    if(direct == "right1"):
       serial1.write(b"R1\n")
    if(direct == "right2"):
       serial1.write(b"R2\n")
    if(direct == "center"):
       serial1.write(b"C\n")
    if(direct == "horizontal"):
       serial1.write(b"H\n")
       
'''
def QR_detector (QR):
    # QR code detection object
    img=QR
    detector = 


    while True:
        data, bbox, _ = detector.detectAndDecode(img)
        #if data in stored:
       #         continue
        #stored.append(data)
        # if there is a bounding box, draw one, along with the data
        if(bbox is not None):
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                         0, 255), thickness=2)
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
            
            if data :
                print("data found: ", data)
        # display the image preview
        cv2.imshow("code detector", img)
        if(cv2.waitKey(1) == ord("q")):
            break
    # free camera object and exit
        return()
   ''' 

##### using model and calculating the time of processing #####

'''
image_path = "./raw_data/QR/100.jpg" # you can use any path for testing the model

img = cv2.imread(image_path , 0) # it must be loaded as gray scal image

e1 = cv2.getTickCount()
Input = LC.preprocessing(img)
predictions = model.predict([Input])
e2 = cv2.getTickCount()
time = (e2 - e1)/ cv2.getTickFrequency()

print("predection = " , LC.conv_list2str(predictions[0]))
print("time of processing = ",time," s")

'''

#### using live ####



camera = cv2.VideoCapture(0)
while (camera.isOpened):
    ret, frame = camera.read()
    cv2.imshow("camera", frame)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    Input = LC.preprocessing(img)
    predictions = model.predict([Input])
    if LC.conv_list2str(predictions[0])=='QR':
        data = QR_detector()
        print(data)
        QR_det(data)
    else:
        direct = LC.conv_list2str(predictions[0])
        print(direct)
        Dir_Line(direct)
    
    if cv2.waitKey(1) == ord('q'):
        break
    #time.sleep(0.5)
    
cv2.destroyAllWindows()
camera.release()


