# Motion-control
![image](https://user-images.githubusercontent.com/89237314/185569686-482c8c65-fe32-423e-af74-693ed5d1d880.png)

This repository contains a simple guide for creating and training a model for controlling an audio player using hand gestures

### Files:

- **tutorial.ipynb** - contains instructions for creating your own data and training the model
- **finger.py** - contains classes for saving hand movements
- **LSTM.py** - contains LSTM model and Dataset class
- **tracer.py** - uses mediapipe. Tracks and saves the position of the fingers. Activates the audio player to control it with gestures

### Classes and methods
Create a **TracerData** object to detect your fingers and create samples. **timer** - time to record one sample, **num_frames** - number of past finger positions 

    data_motion = TracerData(timer=3, num_frames=20)
    
Use **record_trace()** method to record and save finger positions

    data_motion.record_trace()

Use **get_trace()** method to get the trace as a numpy array

    data_motion.get_trace()
    
Use **image()** method to plot saved trace

    data_motion.image()
    
Create a **TracerPlayer** object and pass the path to your playlist, the model and the number of frames to it

    play = TracerPlayer(playlist_path, model, 20)
    
Use **listen(time)** method to turn on the audio player and control it with your hand gestures

    play.listen(60)
    
Use **model.pth** to test how the model works with these movements
- play and stop
![play](https://user-images.githubusercontent.com/89237314/185776991-99ed7f54-ea7f-4da6-ae59-8fc2ad483107.gif)
- sound volume
![volume](https://user-images.githubusercontent.com/89237314/185777192-443d55f6-d28f-446e-81d9-6b06f1e36c9b.gif)
- switching to the next song
![next](https://user-images.githubusercontent.com/89237314/185777125-50ecb3be-a93c-4e6e-b703-128da298ec7f.gif)



