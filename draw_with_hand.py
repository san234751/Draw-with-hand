import cv2
import hand_detection_module
import numpy as np
names=["Red","Yellow","Green","Blue"]
colors=[(0,0,255),(0,255,255),(0,255,0),(255,0,0),(0,0,0)]
video=cv2.VideoCapture(0)
cid,id,xp,yp=0,0,0,0
display=np.zeros((480,640,3),np.uint8)
detector=hand_detection_module.hand_detect(min_detection_confidence=0.80)
while True:
    succ,frame=video.read()
    frame=cv2.flip(frame,1)
    frame=detector.findHands(frame)
    cv2.putText(frame,"Red",(45,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)
    cv2.putText(frame,"Yellow",(130,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3)
    cv2.putText(frame,"Green",(260,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
    cv2.putText(frame,"Blue",(390,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.putText(frame,"Erase",(500,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)
    cv2.putText(frame,"color=",(410,150),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),3)
    cv2.putText(frame,f'{names[cid]}',(520,150),cv2.FONT_HERSHEY_COMPLEX,1,colors[cid],3)
    lmlist=detector.findPosition(frame,draw=False)
    if len(lmlist)!=0:
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        finger=detector.countfinger()
        if finger[1] and finger[2]:
            xp,yp=0,0
            cv2.rectangle(frame,(x1-35,y1-35),(x2+35,y2+35),colors[id],cv2.FILLED)
            if y1<60:
                if x1<120:
                    cid=0
                    id=0
                elif 130<x1<230:
                    cid=1
                    id=1
                elif 260<x1<360:
                    cid=2
                    id=2
                elif 390<x1<465:
                    cid=3 
                    id=3
                elif 500<x1<595:
                    id=4
        elif finger[1] and finger[2]==False:
            cv2.circle(frame,(x1,y1),20,colors[id],cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if colors[id]==(0,0,0):
                cv2.line(frame,(xp,yp),(x1,y1),colors[id],90)
                cv2.line(display,(xp,yp),(x1,y1),colors[id],90)
            else:
                cv2.line(frame,(xp,yp),(x1,y1),colors[id],15)
                cv2.line(display,(xp,yp),(x1,y1),colors[id],15)
            xp,yp=x1,y1
    gray=cv2.cvtColor(display,cv2.COLOR_BGR2GRAY)
    no,invert=cv2.threshold(gray,50,255,cv2.THRESH_BINARY_INV)
    invert=cv2.cvtColor(invert,cv2.COLOR_GRAY2BGR)
    frame=cv2.bitwise_and(frame,invert)
    frame=cv2.bitwise_or(frame,display)
    cv2.imshow("Video",frame)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()