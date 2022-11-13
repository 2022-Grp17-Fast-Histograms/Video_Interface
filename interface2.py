import PySimpleGUI as sg 
from tkinter import *
import cv2 as cv
import os
import numpy as np

sg.theme("DarkTeal")

menu_def =  [
                ['File', ['Open', 'Save', 'Exit']],
                ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo']],
                ['Help', 'About...'] 
            ]


                

layout = [ 
            [sg.Text('Video Interface')], 
            [sg.Multiline(size=(80,10))],
            [sg.Button('Open'), sg.Button('Exit')]
        ]

window1=sg.Window('Video Interface', layout)
window2_active = False
while True:
            event, values=window1.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event == 'Open':
                text = sg.PopupGetFile('Please enter a file name')      
                sg.Popup('Results', text)
                window2_active = True  
                window1.Hide()  
                layout2 = [[sg.Text('Video')],  
                    [sg.Button('Open')],   
                   [sg.Button('Exit')]]  

                window2 = sg.Window('Window 2', layout2) 
                width, height = 1920, 1080
                file_size = os.path.getsize(text)
                n_frames = file_size // (width*height*3 // 2)
                f = open(text, 'rb')
                for i in range(n_frames):
                    yuv = np.frombuffer(f.read(width*height*3//2), dtype=np.uint8).reshape((height*3//2, width))
                    bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
                    cv.imshow('Video Interface', bgr)
                    if cv.waitKey(1) & 0xFF == ord('q'):
                        cv.destroyAllWindows()
                    

            else: 
                window1_active = True
                window2.Hide()
           