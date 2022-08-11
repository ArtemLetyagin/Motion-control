from collections import deque
import numpy as np
from sklearn.preprocessing import StandardScaler
from skimage.draw import line_aa
from copy import deepcopy
import torch

class Finger():
    def __init__(self, length):
        self.l = length
        self.trace = deque()
        self.ss = StandardScaler()
    def append(self, x, y):
        self.trace.append([x, y])
        if(len(self.trace)>self.l):
            self.trace.popleft()
    def clear(self):
        self.trace.clear()
    def get_tensor(self):
        self.ss.fit(self.trace.copy())
        trace = self.ss.transform(self.trace.copy())
        return torch.tensor(trace).to(torch.float)#.view(self.l*2)
    def image(self, h, w, color):
        points = np.array(list(self.trace.copy()))
        zer = np.zeros((h, w))
        for x, y in points:
            zer[y, x] = color
        for i in range(len(self.trace)-1):
            rr, cc, val = line_aa(self.trace[i][1], self.trace[i][0], self.trace[i+1][1], self.trace[i+1][0])
            zer[rr, cc] = val*color
        return zer
    def get(self):
        return np.array(list(deepcopy(self.trace)))
class Fingers():
    def __init__(self, length):
        self.fingers = []
        self.l = length
        for i in range(5):
            self.fingers.append(Finger(length))
    def append(self, x):
        #x=[[x1,y1], [x2,y2], [x3,y3], [x4,y4], [x5,y5]]
        if len(x)==5:
            for i in range(5):
                self.fingers[i].append(x[i][0], x[i][1])
    def clear(self):
        for finger in self.fingers:
            finger.clear()
    def get_tensor(self):
        returner = torch.tensor([])
        for finger in self.fingers:
            returner = torch.cat((returner, finger.get_tensor()), axis=1)
        return returner
    def get_numpy(self):
        returner = []
        for finger in self.fingers:
            returner.append(np.reshape(finger.get_ss(), self.l*2))
        return np.array(returner)
    def image(self, h, w):
        zer = np.zeros((h, w))
        for color, finger in enumerate(self.fingers):
            zer+=finger.image(h, w, (color+1)*10)
        return zer
    def check(self):
        count = 0
        for i in range(5):
            if len(self.fingers[i].get())==self.l:
                count+=1
        if count==5:
            return True
        else:
            return False