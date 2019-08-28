import sqlite3
import face_recognition
import pickle
import cv2
import os
import time


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
        model='cnn')
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
        
    return fetch_data(userid),boxes[i],image

def fetch_data(pid):
    pwd = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(pwd + '\\face_db.db')
    curr = conn.cursor()
    curr.execute("SELECT * FROM  Database WHERE Id = ?",(pid,))
    data = curr.fetchall()
    if conn:
        conn.close()
    return data

def main():

    data,boxes,image = unlock()
    text = ''
    j = 0
    starttime = time.time()
    print("Welcome Back: {} \nHere is your data: {}".format(data[0][1],data[0][2]))
    
    text = ' Name: ' + data[0][1] +'\n Last Seen: ' + data[0][2] + '\n Status: Armed'

    print(len(boxes))
    
    while(cv2.waitKey(1)!=27):
        
        if (time.time()-starttime) > 0.2:
            j= (j+1)%(len(text)+1)
            newImage = image.copy()
            cv2.rectangle(newImage, (boxes[3], boxes[0]), (boxes[1], boxes[2]), (0, 255, 0), 2)
            #y = boxes[2] + 30 if boxes[0] < 100 else boxes[0] - 200
            y = int((boxes[0]+boxes[2])/2)
            x = boxes[1] if boxes[3] < 240 else boxes[3] - 220
            for k, line in enumerate(text.split('\n')):
                cv2.putText(newImage, line[:j], (x, (y+(k * 30) - 30 )), cv2.FONT_HERSHEY_SIMPLEX , 0.75, (0, 0, 255), 2)
            cv2.imshow('Face',newImage)
            starttime = time.time()

        
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

        
    
