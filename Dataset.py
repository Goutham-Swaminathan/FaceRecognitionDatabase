import os
import cv2
import Encoding
    

def Dataset(Name):
    
    cap = cv2.VideoCapture(1)
    count = 0
    text = 'Press S to save an image'
    color = (0,255,0)
    status = False
    Border = 10
    Run = Encoding.Check_Name(Name)
    Encoder_status = 0
    Primary_id = Encoding.Get_PID()
    while(Run):
        
        Ret,Frame = cap.read()
        
        font = cv2.FONT_HERSHEY_SIMPLEX

        Input_Key = cv2.waitKey(1)

        if Input_Key == ord('s'):
            
            Save_Frame = Frame.copy()
            Encoder_status= Encoding.Encoder(Save_Frame,Primary_id,Frame.shape)
            if Encoder_status == 1:
                text = 'Image saved'
                count = count + 1
                color = (0,255,0)
            elif Encoder_status == 2:
                text = 'Please move away from the camera'
                color = (0,0,255)
            elif Encoder_status == 3:
                text = 'Please move closer to the camera'
                color = (0,0,255)
            elif Encoder_status == 4:
                text = 'Stay in the center of the camera'
                color = (0,0,255)
            elif Encoder_status == 5:
                text = 'Too many faces found'
                color = (0,0,255)
            

        elif Input_Key == 27:
            Run = False
            
        if count == 5:
            Run = False



        cv2.putText(Frame, text, (int(Frame.shape[1]*0.5 - len(text)*7) , int(Frame.shape[0]*0.95)), font, 0.8, color, 2, cv2.LINE_AA)
        #cv2.putText(Frame, 'Press Q to save an image' , (10, 20), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(Frame, str(count), (int(Frame.shape[1]*0.96), 20), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        

        cv2.imshow('Dataset Generator',Frame)
        
    if Encoder_status == 1:
        Description = input('Enter Description for {} :'.format(Name))
        status = Encoding.Add_Database(Primary_id,Name,Description)
 
    cap.release()
    cv2.destroyAllWindows()

    return status
