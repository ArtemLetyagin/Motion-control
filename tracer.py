from finger import Fingers
import cv2
import time
import mediapipe as mp
import matplotlib.pyplot as plt
from win32com.client import Dispatch
import os
import numpy as np
import copy

class TracerData():
    def __init__(self, timer, num_frames):
        self.timer = timer
        self.num_frames = num_frames
        self.fingers = Fingers(num_frames)
        self.cap = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands(static_image_mode=False,
                         max_num_hands=1,
                         min_tracking_confidence=0.5,
                         min_detection_confidence=0.5)
        _, img = self.cap.read()
        self.h, self.w, _ = img.shape
    def record_trace(self):
        t = time.time()
        while True:
            _, img = self.cap.read()
            h, w, _ = img.shape
            img = cv2.flip(img, 1)
            result = self.hands.process(img)
            if result.multi_hand_landmarks:
                x = []
                for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):
                    #cv2.circle(img, (cx, cy), 3, (255, 255, 255))
                    if id in [4,8,12,16,20]:
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        x.append([cx, cy])
                        cv2.circle(img, (cx, cy), 5, (0, 255, 0))
                self.fingers.append(x)
            cv2.putText(img, f'Time: {time.time()-t:.2f}', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, 2)
            cv2.imshow("1",img)
            cv2.waitKey(1)
            if time.time()-t>self.timer:
                break
        cv2.destroyAllWindows()

    def image(self):
        plt.imshow(self.fingers.image(self.h, self.w), cmap='seismic')
        plt.show()

    def get_trace(self):
        if self.fingers.check()==False:
            print(f'Error: the path length is less than {self.num_frames}')
        else:
            return self.fingers.get_tensor().numpy()

    def clear(self):
        self.fingers.clear()


class Function():
    def __init__(self, model, path, length):
        self.length = length
        self.mp = Dispatch("WMPlayer.OCX", 0)
        self.model = copy.deepcopy(model)
        self.songs = os.listdir(path)
        for song in self.songs:
            tune = self.mp.newMedia(path+'/'+song)
            self.mp.currentPlaylist.appendItem(tune)
        self.lev = 0
        self.track_num = 0
        self.state = {'volume': self.mp.settings.volume,
                    'track': self.songs[self.track_num],
                    'mode': 'pause'}
    def do(self, fingers):
        pred = self.model(fingers.view(1,self.length,10)).detach().numpy()[0]
        ind = np.argmax(pred)
        val = pred[ind].item()
        if pred[3].item()<5:
            #up volume
            if(ind==0 and val>=5):
                self.mp.settings.volume+=10
                self.state['volume']+=10
            #down volume
            if(ind==1 and val>=5):
                self.mp.settings.volume-=10
                self.state['volume']-=10
            #next
            if(ind==2 and val>=5):
                self.track_num = (self.track_num+1)%5
                self.mp.controls.next()
                self.state['track'] = self.songs[self.track_num]
            #play/stop
            if(ind==4 and val>=5):
                if(self.lev==0):
                    self.mp.controls.play()
                    self.lev=1
                    self.state['mode'] = 'play'
                else:
                    self.mp.controls.pause()
                    self.lev=0
                    self.state['mode'] = 'pause'
    def get_state(self):
        return self.state.copy()
    def stop(self):
        self.mp.controls.pause()
        self.state['mode'] = 'pause'


class TracerPlayer():
    def __init__(self, playlist_path, model, length):
        #TEXT
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (10,30)
        self.bottomLeftCornerOfText1 = (10,60)
        self.bottomLeftCornerOfText2 = (10,90)
        self.fontScale = 1
        self.fontColor = (255,255,255)
        self.fontColor_red = (0, 0, 255)
        self.thickness = 1
        self.lineType = 2
        #FINGERS
        self.fingers = Fingers(length)
        self.cap = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands(static_image_mode=False,
                         max_num_hands=1,
                         min_tracking_confidence=0.5,
                         min_detection_confidence=0.5)
        _, img = self.cap.read()
        self.h, self.w, _ = img.shape
        #FUNCTION
        self.function = Function(model, playlist_path, length)

    def listen(self, timer):
        track_num=0 
        t = time.time()

        while True:
            _, img = self.cap.read()
            h, w, _ = img.shape
            img = cv2.flip(img, 1)
            result = self.hands.process(img)
            if result.multi_hand_landmarks:
                x = []
                for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):
                    #cv2.circle(img, (cx, cy), 3, (255, 255, 255))
                    if id in [4,8,12,16,20]:
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        x.append([cx, cy])
                        cv2.circle(img, (cx, cy), 5, (0, 255, 0))
                self.fingers.append(x)
            if self.fingers.check():
                #do
                self.function.do(self.fingers.get_tensor())
                self.fingers.clear()
            state = self.function.get_state()
            cv2.putText(img, 'Volume: {}'.format(state['volume']), self.bottomLeftCornerOfText, self.font, self.fontScale, self.fontColor_red, self.thickness, self.lineType)
            cv2.putText(img, 'Mode: {}'.format(state['mode']), self.bottomLeftCornerOfText1, self.font, self.fontScale, self.fontColor_red, self.thickness, self.lineType)
            cv2.putText(img, 'Song: {}'.format(state['track']), self.bottomLeftCornerOfText2, self.font, self.fontScale, self.fontColor_red, self.thickness, self.lineType)

            cv2.imshow("1", img)
            cv2.waitKey(1)
            if time.time()-t>timer:
                break
        cv2.destroyAllWindows()
        self.function.stop()
        

                



