import threading
import serial
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, clear_output
import PySimpleGUI as sg

arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)
r_max = 300
scope = 360
register_available = [None] * scope
register_taken = [None] * scope


def write(x):
    arduino.write(bytes(x, 'utf-8'))


def read(window, go_event):
    while go_event.isSet():
        data = arduino.readline().decode('utf-8').strip("\n").split(",")
        try:
            angle = data[0]
            distance = data[1]
            window.write_event_value("Working", (angle, distance))
        except:
            print("Data is not readable!")


def canvas_init():
    fig = plt.figure(figsize=(8, 8), facecolor='#3a3b3c', num="RADAR")
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor('#3a3b3c')
    ax.grid(color='0.9')
    ax.tick_params(axis='x', colors='0.9')
    ax.tick_params(axis='y', colors='0.9')
    ax.set_axisbelow(False)
    ax.set_ylim([0.0, r_max])
    ax.set_xlim([0.0, np.deg2rad(scope)])

    return fig, ax


def draw(fig, ax, angle, distance):
    rad = np.deg2rad(angle)

    if register_available[angle] is not None:
        register_available[angle].pop(0).remove()
        register_taken[angle].pop(0).remove()
    register_available[angle] = ax.plot([rad, rad], [0, distance], color='#528aae', linewidth=2)
    register_taken[angle] = ax.plot([rad, rad], [distance, r_max], color='#3a3b3c', linewidth=2)

    clear_output()
    plt.pause(0.01)


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
            try:
                if int(values['input']) > 360 or int(values['input']) < -360:
                    raise Exception()
                angle = int(5.68 * int(values['input']))
                gui_update(window, mode, True, True, False, True)

                if mode == "Move":
                    write("1," + str(angle))
                if mode == "Inspect":
                    write("2," + str(angle))
                    go_event.set()
                    read_thread = threading.Thread(target=read, args=(window, go_event), daemon=True)
                    read_thread.start()
            except:
                window["label"].Update("Wrong angle - make sure it is integer in range 0-360!", visible=True)
                print("Wrong angle - make sure it is integer in range 0-360!")

        elif event == "Working":
            angle, distance = values[event]
            if int(distance) > r_max:
                distance = r_max
            try:
                draw(fig, ax, int(float(angle) / 5.68), int(distance))
            except:
                print("sth went wrong - check data")

        elif event == "STOP":
            go_event.clear()
            write("0")
            gui_update(window, mode, False, False, False, False)

    window.close()
