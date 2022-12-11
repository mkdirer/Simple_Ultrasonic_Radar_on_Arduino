import threading
import serial
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, clear_output
import PySimpleGUI as sg

arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)
r_max = 200
scope = 360
register_available = [None] * scope
register_taken = [None] * scope

def write(x):
    arduino.write(bytes(x, 'utf-8'))


def read(window, go_event):
    while go_event.isSet():
        angle = arduino.readline().decode('utf-8').strip("\n")
        distance = arduino.readline().decode('utf-8').strip("\n")
        window.write_event_value("Working", (angle, distance))


def canvas_init():
    fig = plt.figure(figsize=(8, 8), facecolor='#3a3b3c')
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor('#3a3b3c')
    ax.grid(color='0.9')
    ax.set_ylim([0.0, r_max])
    ax.set_xlim([0.0, np.deg2rad(scope)])

    return fig, ax


def draw(fig, ax, angle, distance):
    rad = np.deg2rad(angle)

    if register_available[angle] is not None:
        register_available[angle].pop(0).remove()
        register_taken[angle].pop(0).remove()
    register_available[angle] = ax.plot([rad, rad], [0, distance], color='#bcd2e8', linewidth=2)
    register_taken[angle] = ax.plot([rad, rad], [distance, r_max], color='#3a3b3c', linewidth=2)

    display(fig)
    clear_output(wait=True)
    plt.pause(0.1)


def gui_init():
    layout = [[sg.Text("Radar - choose mode:")], [sg.Button("Move")],
              [sg.Button("Inspect")],
              [sg.Text("", key="label", visible=False)],
              [sg.Input(size=(17, 1), key='input', do_not_clear=True, visible=False)],
              [sg.Button("GO", key="GO", visible=False)],
              [sg.Button("STOP", key="STOP", visible=False)],
              [sg.Button("Exit")]]
    window = sg.Window("Radar", layout)

    return window


def gui_update(window, mode, label, input, GO, stop):
    window["label"].Update(mode + " angle:", visible=label)
    window["input"].Update(visible=input)
    window["GO"].Update(visible=GO)
    window["STOP"].Update(visible=stop)


if __name__ == "__main__":
    window = gui_init()
    fig, ax = canvas_init()

    go_event = threading.Event()

    while True:

        event, values = window.read()

        if event == "Move" or event == "Inspect":
            mode = event
            gui_update(window, mode, True, True, True, False)

        elif event == "Exit" or event == sg.WIN_CLOSED:
            write("0")
            break

        elif event == "GO":
            angle = int(5.5 * int(values['input']))
            gui_update(window, mode, True, True, False, True)

            if mode == "Move":
                write("1," + str(angle))
            if mode == "Inspect":
                write("2," + str(angle))
                go_event.set()
                read_thread = threading.Thread(target=read, args=(window, go_event), daemon=True)
                read_thread.start()

        elif event == "Working":
            angle, distance = values[event]
            # print(angle)
            # print(distance)
            # print("\n")
            # # if int(distance.strip('\r')) > r_max or distance == '':
            # #     distance = r_max
            try:
                draw(fig, ax, int(float(angle) / 5.5), int(distance))
            except:
                print("sth went wrong - check data")
                print(int(float(angle) / 5.5))
                print(int(distance))

        elif event == "STOP":
            go_event.clear()
            write("0")
            gui_update(window, mode, False, False, False, False)

    window.close()
