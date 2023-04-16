import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3



#get data from sqlite by ID
def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile


def face_detection_video(link=None):
    faceDetect=cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
    if not link:
        cam=cv2.VideoCapture(0)
    else:
        cam=cv2.VideoCapture(link)
    rec=cv2.face.LBPHFaceRecognizer_create()
    rec.read("recognizer\\trainningData.yml")
    id=0
    #set text style
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    fontscale = 1
    fontcolor = (203,23,252)
    while(True):
        #camera read
        ret,img=cam.read()
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            profile=getProfile(id)
            #set text to window
            if(profile!=None):
                #cv2.PutText(cv2.fromarray(img),str(id),(x+y+h),font,(0,0,255),2);
                cv2.putText(img, "Name: " + str(profile[1]), (x,y+h+30), fontface, fontscale, fontcolor ,2)
                print("ID : " + str(profile[0]))
                print("Age: " + str(profile[2]))
                print("Gender: " + str(profile[3]))
            cv2.imshow('Face',img) 
    cam.release()
    cv2.destroyAllWindows()
