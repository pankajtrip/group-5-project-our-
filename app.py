from flask import *
import pandas as pd
import numpy as np
import cv2,os,csv,datetime,glob
from PIL import Image
import winsound

app=Flask(__name__)

#####################################################

def train_model():

 recognizer=cv2.face.LBPHFaceRecognizer_create()

 faces=[]
 ids=[]

 for file in os.listdir("TrainingImage"):

  img=Image.open(
  "TrainingImage/"+file
  ).convert("L")

  imgNp=np.array(img,"uint8")

  id=int(file.split("_")[0])

  faces.append(imgNp)
  ids.append(id)

 if len(faces)>0:

  recognizer.train(
  faces,
  np.array(ids)
  )

  recognizer.save(
  "TrainingImageLabel/Trainer.yml"
  )

#####################################################

@app.route("/")
def home():

 return render_template("index.html")

#####################################################

@app.route("/register",methods=["GET","POST"])
def register():

 if request.method=="POST":

  # auto create csv

  if not os.path.exists("employees.csv"):

   with open(
   "employees.csv",
   "w",
   newline=""
   ) as f:

    writer=csv.writer(f)

    writer.writerow([
    "id",
    "name",
    "semester",
    "year",
    "branch",
    "subject"
    ])

  data=[

  int(request.form["id"]),

  request.form["name"],

  request.form["semester"],

  request.form["year"],

  request.form["branch"],

  request.form["subject"]

  ]

  df=pd.read_csv("employees.csv")

  # duplicate id check

  if data[0] in df["id"].values:

   return render_template(
   "message.html",
   msg="ID already exists"
   )

  with open(
  "employees.csv",
  "a",
  newline=""
  ) as f:

   writer=csv.writer(f)

   writer.writerow(data)

  cam=cv2.VideoCapture(0)

  detector=cv2.CascadeClassifier(
  "haarcascade_frontalface_default.xml"
  )

  count=0

  while True:

   ret,img=cam.read()

   gray=cv2.cvtColor(
   img,
   cv2.COLOR_BGR2GRAY
   )

   faces=detector.detectMultiScale(
   gray,
   1.3,
   5
   )

   for(x,y,w,h) in faces:

    count+=1

    cv2.imwrite(

    "TrainingImage/"

    +str(data[0])

    +"_"

    +str(count)

    +".jpg",

    gray[y:y+h,x:x+w]

    )

    cv2.rectangle(

    img,

    (x,y),

    (x+w,y+h),

    (0,255,0),

    2

    )

    cv2.putText(

    img,

    str(count)+"/80",

    (20,40),

    cv2.FONT_HERSHEY_SIMPLEX,

    1,

    (0,0,255),

    2

    )

   cv2.imshow(
   "Capture Face",
   img
   )

   if count>=80:
    break

   if cv2.waitKey(1)==27:
    break

  cam.release()

  cv2.destroyAllWindows()

  train_model()

  return render_template(
  "message.html",
  msg="Image Capture Successfully"
  )

 return render_template(
 "register.html"
 )

#####################################################

@app.route("/start")
def start():

 model="TrainingImageLabel/Trainer.yml"

 if not os.path.exists(model):

  return render_template(
  "message.html",
  msg="Register Student First"
  )

 recognizer=cv2.face.LBPHFaceRecognizer_create()

 recognizer.read(model)

 detector=cv2.CascadeClassifier(
 "haarcascade_frontalface_default.xml"
 )

 df=pd.read_csv("employees.csv")

 cam=cv2.VideoCapture(0)

 today=str(
 datetime.date.today()
 )

 file="Attendance/"+today+".csv"

 marked=[]

 # load previous attendance

 if os.path.exists(file):

  old=pd.read_csv(file)

  marked=list(old["ID"])

 else:

  with open(
  file,
  "w",
  newline=""
  ) as f:

   writer=csv.writer(f)

   writer.writerow([

   "ID",
   "Name",
   "Sem",
   "Year",
   "Branch",
   "Subject",
   "Date",
   "Time"

   ])

 while True:

  ret,img=cam.read()

  gray=cv2.cvtColor(
  img,
  cv2.COLOR_BGR2GRAY
  )

  faces=detector.detectMultiScale(
  gray,
  1.3,
  5
  )

  for(x,y,w,h) in faces:

   id,conf=recognizer.predict(

   gray[y:y+h,x:x+w]

   )

   if conf<60:

    student=df.loc[
    df["id"]==id
    ].values

    if len(student)>0:

     name=student[0][1]

     label=str(id)+" "+name

     # first attendance

     if id not in marked:

      color=(0,255,0)

      marked.append(id)

      winsound.Beep(2000,400)

      with open(
      file,
      "a",
      newline=""
      ) as f:

       writer=csv.writer(f)

       writer.writerow([

       student[0][0],
       student[0][1],
       student[0][2],
       student[0][3],
       student[0][4],
       student[0][5],
       today,
       datetime.datetime.now().strftime("%H:%M")

       ])

     else:

      color=(255,0,0)

      label=str(id)+" "+name

    else:

     label="UNLOCK"

     color=(0,0,255)

   else:

    label="UNLOCK"

    color=(0,0,255)

   cv2.rectangle(

   img,

   (x,y),

   (x+w,y+h),

   color,

   2

   )

   cv2.putText(

   img,

   label,

   (x,y-10),

   cv2.FONT_HERSHEY_SIMPLEX,

   0.8,

   color,

   2

   )

  cv2.imshow(
  "Attendance Camera",
  img
  )

  if cv2.waitKey(1)==ord("q"):
   break

 cam.release()

 cv2.destroyAllWindows()

 return render_template(

 "message.html",

 msg="Attendance Saved Successfully"

 )

#####################################################

filtered=[]

@app.route(
"/dashboard",
methods=["GET","POST"]
)
def dashboard():

 global filtered

 data=[]

 search=request.form.get("search","")

 fdate=request.form.get("from_date","")

 tdate=request.form.get("to_date","")

 branch=request.form.get("branch","")

 files=glob.glob(
 "Attendance/*.csv"
 )

 for file in files:

  df=pd.read_csv(file)

  for i,row in df.iterrows():

   if search.lower() in str(row["Name"]).lower():

    if branch=="" or row["Branch"]==branch:

     if fdate=="" or row["Date"]>=fdate:

      if tdate=="" or row["Date"]<=tdate:

       data.append(list(row))

 filtered=data

 return render_template(

 "dashboard.html",

 data=data

 )

#####################################################

@app.route("/download")
def download():

 df=pd.DataFrame(

 filtered,

 columns=[

 "ID",
 "Name",
 "Sem",
 "Year",
 "Branch",
 "Subject",
 "Date",
 "Time"

 ]

 )

 df.to_excel(
 "filtered.xlsx",
 index=False
 )

 return send_file(

 "filtered.xlsx",

 as_attachment=True

 )

#####################################################

@app.route(
"/login",
methods=["GET","POST"]
)
def login():

 if request.method=="POST":

  if request.form["username"]=="admin" and request.form["password"]=="1234":

   return redirect("/dashboard")

 return render_template(
 "login.html"
 )

#####################################################

app.run(debug=True)