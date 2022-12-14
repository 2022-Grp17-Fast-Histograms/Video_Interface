#YUV Video Interface

#Copyright © 2022 2022-Grp17-Fast-Histograms

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
#documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
#the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
#to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
#the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
#THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
#TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# the libraries
import PySimpleGUI as sg
from tkinter import *
import cv2 as cv
import os
import numpy as np
import time
import threading

# Global Variables
width, height = 1920, 1080
frame_size = width * height * 3 // 2
current_frame = 0
stop = False

# Function to play frame by frame and convert YUV to RGB
def update(n_frames, f, window2):
    global current_frame
    global stop
    for i in range(n_frames - current_frame):
        if (stop):
            break
        f.seek(current_frame * frame_size)
        yuv = np.frombuffer(f.read(frame_size), dtype=np.uint8).reshape((height * 3 // 2, width))
        bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
        # converts to png file
        image = cv.imwrite('bgr.png', bgr)
        window2['video'].update(filename='bgr.png', visible=True, subsample=2)
        current_frame += 1
        time.sleep(1)

# Function to check the frame
def updateFrameLoop():
    global current_frame
    if (current_frame >= n_frames):
        current_frame = 0
    elif (current_frame < 0):
        current_frame = n_frames - 1

# Function to update the frame
def updateFrame(f, window2):
    updateFrameLoop()
    f.seek(current_frame * frame_size)
    yuv = np.frombuffer(f.read(frame_size), dtype=np.uint8).reshape((height * 3 // 2, width))
    bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
    # converts to png file
    image = cv.imwrite('bgr.png', bgr)
    window2['video'].update(filename='bgr.png', visible=True, subsample=2)




# the color of the background
sg.theme("DarkTeal")


# the layout/design of the window
layout = [
    [sg.Text('Video Interface', size=(40,0))],
    [sg.Multiline(size=(80, 10))],
    [sg.Button('Open'), sg.Button('Exit')]
]

# when window1 is opened the title of the interface and layout is displayed
window1 = sg.Window('Video Interface', layout)

# window2 is inactive when window1 is open
window2_active = False

# While window1 is open then the following will occur based on what the user clicks
while True:

    # Opens window1 and activates the buttons
    event, values = window1.read()

    # If the user closes Window1 or click the 'Exit' button the window closes
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    # If the user clicks the 'Open' button the following occurs
    elif event == 'Open':

        # When the open button is clicked then a popup will appear to prompt the use to open
        # a YUV file
        text = sg.PopupGetFile('Please enter a file name')
        sg.Popup('Results', text)

        # Window1 will then close and window2 will open
        window2_active = True
        window1.Hide()
        
        # Gets the file size 
        file_size = os.path.getsize(text)

        # Calculates the number of frames
        n_frames = file_size // (frame_size)

        # Opens the YUV file 
        f = open(text, 'rb')

        # Calculates the size of the frame and reshapes the array
        yuv = np.frombuffer(f.read(frame_size), dtype=np.uint8).reshape((height * 3 // 2, width))

        # Converts YUV to RGB
        bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)

        # Converts to png file
        image = cv.imwrite('bgr.png', bgr)

         # the layout/design of the window
        layout2 = [
            
            [sg.Image(filename='bgr.png', key='video', subsample=2)],
            [sg.Button('<<'),
             sg.Button('Play'),
             sg.Button('Pause'),
             sg.Button('>>')]
            
            
            ]
        
        # When window2 is opened the title of the interface and layout is displayed
        window2 = sg.Window('Window 2', layout2, finalize=True, element_justification='c')
        
         # While window2 is open then the following will occur based on what the user clicks
        while True:

            # Opens window2 and activates the buttons
            event2, values = window2.Read()
            
            # When the user clicks the button ">>" it skips to the next frame
            if event2 == '>>':
                current_frame += 1
                updateFrame(f, window2)

            # When the user clicks the button "Play" the video will go through the frames
            elif event2 == 'Play':
                stop = False
                threading.Thread(target=update, args=(n_frames, f, window2)).start()
                              
            # When the user clicks the button "Pause" the video will stop on a frame
            elif event2 == 'Pause':
                stop = True

            # When the user clicks the button "<<" it skips to the previous frame
            elif event2 == '<<':
                current_frame -= 1
                updateFrame(f, window2)
            
            # When the user exits window2 then window1 will open
            elif event2 is None:
                        window2.Close()  
                        window2_active = False  
                        window1.UnHide()  
                        break

                
                    

        
           