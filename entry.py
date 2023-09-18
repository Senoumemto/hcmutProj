import graph as umegraph
import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define the layout of the GUI
maxTextLen = 10
layout = [
    [sg.Text("Input the circuit parameters:")],
    [
        sg.Text("R [orm]:"),
        sg.InputText(key="-R-", size=(maxTextLen, 1)),
        sg.Text("C [F]:"),
        sg.InputText(key="-C-", size=(maxTextLen, 1)),
        sg.Text("L [H]:"),
        sg.InputText(key="-L-", size=(maxTextLen, 1)),
    ],
    [
        sg.Text("V [V]:"),
        sg.InputText(key="-V-", size=(maxTextLen, 1)),
        sg.Text("tMax [s]:"),
        sg.InputText(key="-tLen-", size=(maxTextLen, 1), default_text="1.0"),
        sg.Text("tDist [s]:"),
        sg.InputText(key="-tDist-", size=(maxTextLen, 1), default_text="0.000001"),
    ],
    [sg.Button("Run"), sg.Button("Example")],
    [sg.Canvas(key="-CANVAS-")],
]

# Make graph targets
fig = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
iPlt = fig.add_subplot(1, 2, 1)  # Time vs current
vPlt = fig.add_subplot(1, 2, 2)  # Time vs voltage

# Create the GUI window and graph canvas
window = sg.Window("Calculater RCL", layout, finalize=True)
tkcanvas = FigureCanvasTkAgg(fig, window["-CANVAS-"].TKCanvas)


# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    elif event == "Run":
        params = umegraph.GetAndVerifyRLCV(values)
        # non real number etc.
        if params == None:
            sg.popup("Invalid value")
        else:
            # Update plotting
            iPlt.cla()
            iPlt.set_xlabel("Time [s]")
            iPlt.set_ylabel("Current [A]")

            vPlt.cla()
            vPlt.set_xlabel("Time [s]")
            vPlt.set_ylabel("Voltage [V]")
            umegraph.DrawGraph(vPlt, iPlt, params)
            vPlt.legend()
            iPlt.legend()

            # Update displaying
            tkcanvas.draw()
            tkcanvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    # Input example params
    if event == "Example":
        window["-R-"].update(100)
        window["-L-"].update(1e-3)
        window["-C-"].update(10e-6)
        window["-V-"].update(10)
        window["-tLen-"].update(10e-3)
        window["-tDist-"].update(1e-6)


# Close the window
window.close()
