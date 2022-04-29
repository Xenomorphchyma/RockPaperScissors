# https://realpython.com/pysimplegui-python/
# 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
import io

import PySimpleGUI as sg
import cv2
from matplotlib import transforms

import random

from preprocessing import hand_extractor
import numpy as np
from threading import Event
from time import sleep

import RPS


def main():
    camera = cv2.VideoCapture(0)
    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)  # float width
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    sg.theme('DarkAmber')

    # define the window layout

    layout = [[sg.Text('RPS Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Text("User:"), sg.Image(filename='resourses/gui_images/background.png', key='image', size=(256, 256)),
               sg.Text(text="Computer"),
               sg.Image(filename='resourses/gui_images/background.png', key='-computerkey-', visible=True, size=(256, 256))],
              [sg.Button("Start Game", size=(10, 1), font='Helvetica 14'),
               sg.Button('Start Camera', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Any 14', ),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ],
              [sg.Text('Сложность:', size=(15, 1), justification='center', font='Helvetica 20'), sg.Text(text='Равная', key='-settings-', font='Helvetica 20',)],
              [sg.Text(key="pobed", size=(30, 1), justification='center', font='Helvetica 20')]]
    # filename = 'resourses/gui_images/paper.png',

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       layout, size=(1000, 640), location=(width, height), resizable=True)



    # ---===--- Event LOOP Read and display frames, operate the GUI --- #

    recording = False
    a = 1

    # test_transform = transforms.Compose([taransforms.ToPILImage(), transforms.ToTensor()])
    # test_transform(hand_points_image).unsqueeze(0)
    # test_transform(hand_image).unsqueeze(0)
    # Работа с изображением и изображением с точками - ответ от нейронки в виде цифры(сделать)

    while True:
        event, values = window.read(timeout=20)
        ret, frame = camera.read()
        # hand_points_image, hand_image, x, y = hand_extractor(frame, width, height)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'Start Game':
            try:
                recording = True

            except ValueError as e:
                window['pobed'].update('Подключите камеру')
                recording = False
                continue
            # if recording == False:
            RPS.settings = 'y'
            window['-settings-'].update('Непобедимо')
            window.refresh()
            window['-computerkey-'].update(filename='resourses/gui_images/3.png', size=(256, 256))
            window.refresh()
            sleep(1)
            window['-computerkey-'].update(filename='resourses/gui_images/2.png', size=(256, 256))
            window.refresh()
            sleep(1)
            window['-computerkey-'].update(filename='resourses/gui_images/1.png', size=(256, 256))
            window.refresh()
            Event().wait(1.0)
            a = 0

            recording = False
            # tmp = np.zeros((1024, 768, 3), np.uint_8)
            # img[y1:y2, x1:x2] = tmp[y3:y4, x3:x4]
            # hand_points_image, hand_image, x, y = hand_extractor(frame, width, height)


        elif event == 'Start Camera':
            recording = True

        elif event == 'Stop':
            # RPS.settings = 'y'
            # window['-settings-'].update('Непобедимо')
            # window.refresh()
            # window['-computerkey-'].update(filename='resourses/gui_images/3.png', size=(256, 256))
            # window.refresh()
            # sleep(1)
            # window['-computerkey-'].update(filename='resourses/gui_images/2.png', size=(256, 256))
            # window.refresh()
            # sleep(1)
            # window['-computerkey-'].update(filename='resourses/gui_images/1.png', size=(256, 256))
            # window.refresh()
            # Event().wait(1.0)
            # a = 0

            recording = False

        if recording:
            try:
                hand_points_image, hand_image, _, _ = hand_extractor(frame, width, height)
                imgbytes = cv2.imencode('.png', hand_image)[1].tobytes()  # ditto
                window['image'].update(data=imgbytes)
            except FileNotFoundError:
                window['pobed'].update('Подключите камеру')
        if a == 0:
            try:
                # получает значение и сразу ответ
                RPS.user_action = RPS.get_user_selection()
                recording = False
                # вывод картинки с ответом игрока
                b = RPS.user_action
                if RPS.user_action == 0:
                    window['image'].update(filename='resourses/gui_images/rock.png', size=(256, 256))
                elif RPS.user_action == 2:
                    window['image'].update(filename='resourses/gui_images/scissors.png', size=(256, 256))
                else:
                    window['image'].update(filename='resourses/gui_images/paper.png', size=(256, 256))
                window.refresh()
            except ValueError as e:
                RPS.range_str = f"[0, {len(RPS.Action) - 1}]"
                print(f"Не правильное значение, выберите число между {RPS.range_str}")
                continue
            RPS.computer_action = RPS.get_computer_selection()
            # вывод картинки с ответом компьютера
            z = int(RPS.determine_winner(RPS.user_action, RPS.computer_action))
            if z == 0:
                window['-computerkey-'].update(filename='resourses/gui_images/rock.png', size=(256, 256))
            elif z == 2:
                window['-computerkey-'].update(filename='resourses/gui_images/scissors.png', size=(256, 256))
            else:
                window['-computerkey-'].update(filename='resourses/gui_images/paper.png', size=(256, 256))
            if b > z:
                window['pobed'].update('Победа')
            elif b == z:
                window['pobed'].update('Ничья')
            else:
                window['pobed'].update('Поражение')
            window.refresh()
            a = 1


main()

# https://dzone.com/articles/pysimplegui-how-to-draw-shapes-on-an-image-with-a
# def save_image(values):
#     save_filename = sg.popup_get_file(
#         "File", file_types=file_types, save_as=True, no_window=True
#     )
#     if save_filename == values["-FILENAME-"]:
#         sg.popup_error(
#             "You are not allowed to overwrite the original image!")
#     else:
#         if save_filename:
#             shutil.copy(tmp_file, save_filename)
#             sg.popup(f"Saved: {save_filename}")
