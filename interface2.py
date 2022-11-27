#the libraries 
import PySimpleGUI as sg 
from tkinter import *
import cv2 as cv
import os
import numpy as np




#the color of the background
sg.theme("DarkTeal")

#The menu that is found at the top after starting the interface
menu_def =  [
                ['File', ['Open', 'Save', 'Exit']],
                ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo']],
                ['Help', 'About...'] 
            ]


                
#the layout/design of the window
layout = [ 
            [sg.Text('Video Interface')], 
            [sg.Multiline(size=(80,10))],
            [sg.Button('Open'), sg.Button('Exit')]
        ]

#when window1 is opened the title of the interface and layout is displayed
window1=sg.Window('Video Interface', layout)

#window2 is inactive when window1 is open
window2_active = False

while True:
            event, values=window1.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event == 'Open':

                #when the open button is clicked then a popup will appear to prompt the use to open
                #a file
                text = sg.PopupGetFile('Please enter a file name')      
                sg.Popup('Results', text)

                #window1 will then close and window2 will open
                window2_active = True  
                window1.Hide()  

                #the layout for window2
                layout2 = [     
                   [sg.Button('<<')],
                   [sg.Button('Play')],
                   [sg.Button('Pause')],
                   [sg.Button('>>')],
                   ]

                #when window2 is opened the title of the interface and layout is displayed
                window2 = sg.Window('Window 2', layout2)            
                while True:
                    
                    #reads the YUV file and converts it RGB
                    width, height = 1920, 1080
                    file_size = os.path.getsize(text)
                    n_frames = file_size // (width*height*3 // 2)
                    f = open(text, 'rb')
                    
                    #getting the frame values
                    for i in range(n_frames):
                       yuv = np.frombuffer(f.read(width*height*3//2), dtype=np.uint8).reshape((height*3//2, width))
                       bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
                        #Displays the YUV file
                       cv.imshow('Video Interface', bgr)
                       
                       if cv.waitKey(1) & 0xFF == ord('q'):
                            cv.destroyAllWindows()
            else: 
                window1_active = True
                #window2.Hide()
                       #event2 = window2.read()    
                       #if event2 == '>>' :
                        #    for i in range(n_frames):
                         #       yuv = np.frombuffer(f.read(width*height*3//2), dtype=np.uint8).reshape((height*3//2, width))
                          #      bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
                           #     cv.waitKey(500)
                       #elif event2 == 'Play' :
                        #    for i in range(n_frames):
                         #       yuv = np.frombuffer(f.read(width*height*3//2), dtype=np.uint8).reshape((height*3//2, width))
                          #      bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
                           #     cv.imshow('Video Interface', bgr)
                            #    cv.waitKey(1)
                       #elif event2 == '<<' :
                        #    for i in range(n_frames - 1):
                         #       yuv = np.frombuffer(f.read(width*height*3//2), dtype=np.uint8).reshape((height*3//2, width))
                          #      bgr = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
                           #     cv.waitKey(500)
                       #elif event2 is None or event2 == 'Exit':  
                        #    window2.Close()  
                         #   window2_active = False  
                          #  window1.UnHide()  
                           # break
                    
                       
                            
                            

                    
                    
                        #When clicking on command+q window2 will close which is an alternative to going through the
                        #files menu
                        #the function waitkey() is for how long the video will play 
                
                    

        
           