# https://realpython.com/pysimplegui-python/

import PySimpleGUI as sg
import cv2
from preprocessing import hand_extractor
import numpy as np


"""
Demo program that displays a webcam using OpenCV
"""


def main():
    camera = cv2.VideoCapture(0)
    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)  # float width
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

    sg.theme('DarkAmber')

    # define the window layout
    layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Text("User:"), sg.Image(filename='resourses/gui_images/paper.png', key=''), sg.Text("Computer"),
               sg.Image(filename='', key=''),
               sg.Image(filename='', key='image')],
              [sg.Button("Start Game", size=(10, 1), font='Helvetica 14'),
               sg.Button('Start Camera', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Any 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       layout, size=(1000, 640), location=(width, height), resizable=True)

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #

    recording = False

    while True:
        event, values = window.read(timeout=20)
        # tmp = np.zeros((1024, 768, 3), np.uint_8)
        # hand_points_image, hand_image, x, y = hand_extractor(frame, width, height)
        # img[y1:y2, x1:x2] = tmp[y3:y4, x3:x4]

        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'Start Game':
            # обратный отчёт 3 2 1
            return

        elif event == 'Start Camera':
            recording = True

        elif event == 'Stop':
            recording = False
            img = np.full((width, height), 255)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)

        if recording:
            ret, frame = camera.read()
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            window['image'].update(data=imgbytes)


main()