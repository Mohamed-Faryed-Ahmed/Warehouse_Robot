def QR_detector (img):
        cv2.QRCodeDetector()
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
       