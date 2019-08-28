import face_recognition
import pickle
import cv2
import os
import sqlite3
import numpy as np
import time

pwd = os.path.dirname(os.path.realpath(__file__))

def Make_Table():
        conn = sqlite3.connect(pwd + '\\Face_database.db')
        curr = conn.cursor()
        print('making table')
        curr.execute("create table Database(Id integer primary key,Name text, Description text)")
        curr.execute('insert into Database(Id,Name,Description) values(?,?,?) ',(0,'Unknown','No Data',))
        conn.commit()
        if conn:
                conn.close()
        
def Add_Database(Primary_id,Name,Description):
        conn = sqlite3.connect(pwd + '\\Face_database.db')
        curr = conn.cursor()
        print('Entering Record')
        curr.execute('insert into Database(Id,Name,Description) values(?,?,?) ',(Primary_id,Name,Description,))
        conn.commit()

        if conn:
                conn.close()
        return True
        

def Get_PID():
        conn = sqlite3.connect(pwd + '\\Face_database.db')
        curr = conn.cursor()
        curr.execute('SELECT * FROM  Database WHERE ID = (SELECT MAX(ID)  FROM Database)')
        Last_Record = curr.fetchall()
        if conn:
                conn.close()

        return Last_Record[0][0] + 1

        
        
def Check_Name(Name):
        conn = sqlite3.connect(pwd + '\\Face_database.db')
        curr = conn.cursor()
        curr.execute("SELECT * FROM  Database WHERE Name = ?",(Name,))
        Existing_Names = curr.fetchall()
        for Person in Existing_Names:
                print(Person[2])
                Check = input('Is this you?')
                if Check == 'y':
                        return False
        if conn:
                conn.close()
                
        return True

        
def Encoder(Frame,Primary_id,Shape):
        
        Box = face_recognition.face_locations(Frame,model='hog')
        
        if len(Box)>1:
                return 5
        if len(Box) == 0:
                return 4
        if (Box[0][0] < 30 or Box[0][1] > Shape[0] - 30 or Box[0][2] > Shape[1] - 20 or Box[0][3] < 30):
                return 4
        Face_Ratio = (Box[0][2]-Box[0][0])*(Box[0][1]-Box[0][3])/(Shape[0]*Shape[1])
        if Face_Ratio < 0.07:
                return 3
        if Face_Ratio > 0.15:
                return 2
        
        data = {}
        Encoding = face_recognition.face_encodings(Frame, Box)
        print(os.path.isfile('encoding.pickle'))
        if os.path.isfile('encoding.pickle'):
                print('appending')
                data = pickle.loads(open( pwd+'\\encoding.pickle', "rb").read())
                data["encodings"].append(Encoding[0])
                data["id"].append(Primary_id)
        else:
                print('Pickle does not exist')
                data["encodings"] = [Encoding[0]]
                data["id"] = [Primary_id]
        
        File = open(pwd+'\\encoding.pickle', "wb")
        File.write(pickle.dumps(data))
        File.close()
        
        return 1

def unlock():

    location = os.path.dirname(os.path.realpath(__file__))
    
    cap = cv2.VideoCapture(0)


    # load the known faces and embeddings
    print("Scanning For Face")
    data = pickle.loads(open(location+'\\encoding.pickle', "rb").read())

    run = True
    
    starttime = time.time()

    userid = 0
    
    while(run):
        
    # read image from the primary camera of the device
        ret,image = cap.read()
        font = cv2.FONT_HERSHEY_SIMPLEX

        inputkey = cv2.waitKey(1)
        names = []

        # detect the (x, y)-coordinates of the bounding boxes corresponding
        # to each face in the input image, then compute the facial embeddings
        # for each face
        # Depending on the computational capability you can use hog or cnn
        
        boxes = face_recognition.face_locations(image,
        model='hog')
        encodings = face_recognition.face_encodings(image, boxes)

        # initialize the list of names for each face detected
        

        # loop over the facial embeddings
        for encoding in encodings:
	# attempt to match each face in the input image to our known
	# encodings
            faceid = 0
            matches = face_recognition.compare_faces(data["encodings"],
		encoding,tolerance = 0.45)

	# check to see if we have found a match
            if True in matches:
		# find the indexes of all matched faces then initialize a
		# dictionary to count the total number of times each face
		# was matched
                    
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

		# loop over the matched indexes and maintain a count for
		# each recognized face face
                    for i in matchedIdxs:
                            faceid = data["id"][i]
                            counts[faceid] = counts.get(faceid, 1) + 1

		# determine the recognized face with the largest number of
		# votes (note: in the event of an unlikely tie Python will
		# select first entry in the dictionary)
                    userid_temp = max(counts, key=counts.get)
                    if userid != userid_temp:
                        starttime = time.time()
                    if (time.time()-starttime) > 1:
                        run = False
                    userid = userid_temp
            names.append(faceid)

    cap.release()
    cv2.destroyAllWindows()

    for (i,name) in enumerate(names):
        if name != 0:
            break
        
    return fetch_data(userid)

def fetch_data(pid):
    pwd = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(pwd + '\\Face_database.db')
    curr = conn.cursor()
    curr.execute("SELECT * FROM  Database WHERE Id = ?",(pid,))
    data = curr.fetchall()
    if conn:
        conn.close()
    return data



        
        
        
        
        
