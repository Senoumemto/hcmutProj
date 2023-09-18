import matplotlib

matplotlib.use("TkAgg")  # Use the Tkinter backend (or 'QtAgg' for Qt)

import matplotlib.pyplot as plt
import lab

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def is_real_number(text):
    try:
        float(text)
        return True
    except ValueError:
        return False


def GetAndVerifyRLCV(values):
    # At first, verify them
    if (
        is_real_number(values["-R-"])
        and is_real_number(values["-L-"])
        and is_real_number(values["-C-"])
        and is_real_number(values["-tLen-"])
        and is_real_number(values["-tDist-"])
        and is_real_number(values["-tDist-"])
    ):
        R = float(values["-R-"])
        L = float(values["-L-"])
        C = float(values["-C-"])
        V = float(values["-V-"])
        tLen = float(values["-tLen-"])
        tDist = float(values["-tDist-"])
        return [R, L, C, V, tLen, tDist]
    else:
        return None


def DrawGraph(vPlt, iPlt, RLCV):
    val = lab.CalcRLCGraph(RLCV)
    iPlt.plot(val[0], val[1], marker="", linestyle="-", color="k", label="current [A]")
    vPlt.plot(val[0], val[2][0], marker="", linestyle="-", color="r", label="vR [V]")
    vPlt.plot(val[0], val[2][1], marker="", linestyle="-", color="g", label="vL [V]")
    vPlt.plot(val[0], val[2][2], marker="", linestyle="-", color="b", label="vC [V]")
