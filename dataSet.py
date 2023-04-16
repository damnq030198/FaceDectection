import cv2
import sqlite3
import os
#SQL connection and Create database
def sql_connection():
    try:
        con = sqlite3.connect('FaceBase.db')
        return con
    except Error:
        print(Error)

#create table
def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE People (Id INTEGER PRIMARY KEY NOT NULL, Name TEXT NOT NULL, Age INTEGER, Gender TEXT)")
    con.commit()

#insert/update data to sqlite
def insertOrUpdate(profile):
    con = sql_connection()
    cmd="SELECT * FROM People WHERE ID="+str(profile[0])
    try:
    	cursor=con.execute(cmd)
    except:
    	sql_table(con)
    	cursor=con.execute(cmd)
    
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    
    #Update data
    if isRecordExist==1:
        con.execute('UPDATE People SET Name=?, Age=?, Gender=?  WHERE Id=?',(str(profile[1]),str(profile[2]),str(profile[3]),str(profile[0]))  )
    else:   #Insert data
        con.execute('INSERT INTO People(Id,Name,Age,Gender) Values(?,?,?,?)',(str(profile[0]),str(profile[1]),str(profile[2]),str(profile[3])))
    con.commit()
    con.close()

#Get data by id
def getAllById(id):
    con = sql_connection()
    cmd="SELECT * FROM People WHERE ID="+str(id)
    try:
        cursor=con.execute(cmd)
        profile = None
        for row in cursor:
            profile =row
        return profile
    except Exception as e:
        print(e)
        return id
    con.close()

#input label data
def inputdata():
    id=input('enter your id : ')
    profile = getAllById(id)
    while True:
        if profile:
            print("Id is exist. Name is "+profile[1])
            flag = input("You want to update data: ")
            if flag.lower().startswith("y"):
                name =input('enter your name : ')
                age =input('enter your age : ')
                gender =input('enter your gender : ')  
            else:
                return profile
        else:
            name =input('enter your name : ')
            age =input('enter your age : ')
            gender =input('enter your gender : ')
            break  
    profile = [id,name,age,gender]
    return profile

#create data
def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)


def setDatabyCam():
    profile = inputdata()
    insertOrUpdate(profile)
    sampleNum=0
    cam = cv2.VideoCapture(0)
    filename = cv2.data.haarcascades +'haarcascade_frontalface_default.xml'
    detector=cv2.CascadeClassifier(filename)
    while(True):
        #camera read
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            
            #incrementing sample number 
            sampleNum=sampleNum+1
            filepath = "dataSet/"+str(profile[0])
            createPath(filepath)
            filename = "/face."+profile[1] +'.'+ str(sampleNum) + ".jpg"
            #saving the captured face in the dataset folder
            cv2.imwrite(filepath+filename, gray[y:y+h,x:x+w])
            print(sampleNum)
            cv2.imshow('frame',img)
        #wait for 100 miliseconds 
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # break if the sample number is morethan 20
        elif sampleNum>15:
            break
    cam.release()
    cv2.destroyAllWindows()

# setDatabyCam()
def setDatabyImage():
    profile = inputdata()
    insertOrUpdate(profile)
    filepath = "dataSet/"+str(profile[0])
    createPath(filepath)
    list = os.listdir(filepath) # dir is your directory path
    sampleNum = len(list)
    if sampleNum > 15:
        return
    filename = "/face."+profile[1] +'.'+ str(sampleNum) + ".jpg"
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            #saving the captured face in the dataset folder
        cv2.imwrite(filepath+filename, gray[y:y+h,x:x+w])
        cv2.imshow('frame',img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# setDatabyCam()

