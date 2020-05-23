# Importing ML libs
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

# ML Initializations
sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier =load_model('Emotion_little_vgg.h5')
class_labels = ['Angry','Happy','Neutral','Sad','Surprise']

# Emotion Detection Function
def get_emotion():
    label='404'
    cap = cv2.VideoCapture(0)
    while label=='404':
        global sess
        global graph
        with graph.as_default():
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray,1.3,5)

            # if faces:
            for (x,y,w,h) in faces:
                # cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h,x:x+w]
                roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
                if np.sum([roi_gray])!=0:
                    roi = roi_gray.astype('float')/255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi,axis=0)
                    set_session(sess)
                    preds = classifier.predict(roi)[0]
                    label=class_labels[preds.argmax()]
                    # label_position = (x,y)
                    # cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
                    # cap.release()
                    # return label
                else:
                    # cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
                    label = '404'
        # cv2.imshow('Emotion Detector',frame)
    
    # time.sleep(15)
    cap.release() 
    # cv2.waitKey(1)   
    return label
